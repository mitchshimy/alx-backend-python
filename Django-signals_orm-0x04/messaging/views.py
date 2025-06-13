# django_chat/views.py

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
def delete_user(request):
    user = request.user
    logout(request)
    user.delete()
    return redirect("home")  # Replace with your actual landing page
