"""
Intentionally vulnerable views for security testing.
DO NOT USE IN PRODUCTION.
"""
from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection
from .models import User, Comment
from .utils import process_image, load_yaml_config, make_api_request
import tempfile
import os


def index(request):
    """Home page"""
    return render(request, 'vulnapp/index.html')


def search_user(request):
    """
    SQL Injection vulnerability - using raw SQL with unsanitized input
    Example: /search/?username=admin' OR '1'='1
    """
    username = request.GET.get('username', '')

    # VULNERABLE: Direct SQL injection
    with connection.cursor() as cursor:
        query = f"SELECT * FROM vulnapp_user WHERE username = '{username}'"
        cursor.execute(query)
        rows = cursor.fetchall()

    users = [{'id': row[0], 'username': row[1], 'email': row[3]} for row in rows]
    return render(request, 'vulnapp/search.html', {'users': users, 'query': username})


def add_comment(request):
    """
    XSS vulnerability - no sanitization of user input
    CSRF protection is disabled in settings
    """
    if request.method == 'POST':
        user_id = request.POST.get('user_id', 1)
        content = request.POST.get('content', '')

        # VULNERABLE: No sanitization, stores raw HTML/JavaScript
        user = User.objects.get(id=user_id)
        Comment.objects.create(user=user, content=content)

    comments = Comment.objects.all()
    return render(request, 'vulnapp/comments.html', {'comments': comments})


def login(request):
    """
    Authentication bypass vulnerability - weak authentication logic
    """
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        # VULNERABLE: Plain text password comparison, timing attack possible
        try:
            user = User.objects.get(username=username, password=password)
            return HttpResponse(f"Welcome {user.username}! Admin: {user.is_admin}")
        except User.DoesNotExist:
            return HttpResponse("Invalid credentials")

    return render(request, 'vulnapp/login.html')


def user_profile(request):
    """
    Path traversal vulnerability
    Example: /profile/?file=../../../etc/passwd
    """
    filename = request.GET.get('file', 'profile.txt')

    # VULNERABLE: No path sanitization
    try:
        with open(f'/tmp/{filename}', 'r') as f:
            content = f.read()
        return HttpResponse(f"<pre>{content}</pre>")
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}")


def upload_image(request):
    """
    Image upload with Pillow processing vulnerability
    Uses Pillow 9.3.0 (CVE-2023-50447)
    """
    if request.method == 'POST' and request.FILES.get('image'):
        uploaded_file = request.FILES['image']

        # Save to temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.tmp') as tmp:
            for chunk in uploaded_file.chunks():
                tmp.write(chunk)
            tmp_path = tmp.name

        try:
            # VULNERABLE: Process image with vulnerable Pillow version
            metadata = process_image(tmp_path)
            return HttpResponse(f"<pre>Image Metadata:\n{metadata}</pre>")
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

    return HttpResponse("""
        <h1>Upload Image (Pillow CVE-2023-50447)</h1>
        <form method="POST" enctype="multipart/form-data">
            <input type="file" name="image" accept="image/*">
            <button type="submit">Upload</button>
        </form>
        <p><a href="/">← Back</a></p>
    """)


def load_config(request):
    """
    YAML config loading vulnerability
    Uses PyYAML 5.3.1 (CVE-2020-14343)
    """
    if request.method == 'POST':
        yaml_content = request.POST.get('config', '')

        # VULNERABLE: Unsafe YAML loading
        try:
            config = load_yaml_config(yaml_content)
            return HttpResponse(f"<pre>Loaded config:\n{config}</pre>")
        except Exception as e:
            return HttpResponse(f"<pre>Error: {e}</pre>")

    return HttpResponse("""
        <h1>Load YAML Config (PyYAML CVE-2020-14343)</h1>
        <p>⚠️ Vulnerable to arbitrary code execution!</p>
        <form method="POST">
            <textarea name="config" rows="10" cols="50">
database:
  host: localhost
  port: 5432
            </textarea><br>
            <button type="submit">Load Config</button>
        </form>
        <p><a href="/">← Back</a></p>
    """)


def proxy_request(request):
    """
    SSRF vulnerability via requests library
    Uses requests 2.25.0 (CVE-2021-33503)
    """
    url = request.GET.get('url', '')

    if url:
        # VULNERABLE: SSRF via requests with redirect vulnerability
        result = make_api_request(url)
        return HttpResponse(f"<pre>Response:\n{result}</pre>")

    return HttpResponse("""
        <h1>Proxy Request (Requests CVE-2021-33503)</h1>
        <p>⚠️ Vulnerable to SSRF attacks!</p>
        <form method="GET">
            <input type="text" name="url" value="https://api.github.com/zen" size="50">
            <button type="submit">Fetch</button>
        </form>
        <p><a href="/">← Back</a></p>
    """)

