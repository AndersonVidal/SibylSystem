from django.contrib.auth import get_user_model

User = get_user_model()


def create_user(username="testuser", password="testpass123", **kwargs):
    return User.objects.create_user(username=username, password=password, **kwargs)
