from django.db import models


class User(models.Model):
    """User model with intentional vulnerabilities"""
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)  # Plain text password (vulnerability)
    email = models.EmailField()
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class Comment(models.Model):
    """Comment model for demonstrating XSS vulnerabilities"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()  # No sanitization
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username}"
