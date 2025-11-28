"""
Intentionally vulnerable views for security testing.
DO NOT USE IN PRODUCTION.
"""
from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection
from .models import User, Comment


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
