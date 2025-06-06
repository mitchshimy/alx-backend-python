# chats/middleware.py
from datetime import datetime, time
from django.http import HttpResponseForbidden

class RolepermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.allowed_roles = {'admin', 'moderator'}

    def __call__(self, request):
        # Check if path requires role-based permission (customize as needed)
        # For example, protect chat admin routes:
        if request.path.startswith('/api/chats/admin/') or request.path.startswith('/chats/admin/'):
            user = getattr(request, 'user', None)
            
            # If no authenticated user or user role not allowed
            if not user or not user.is_authenticated:
                return HttpResponseForbidden("Authentication required.")
            
            # Assuming the user object has a 'role' attribute:
            user_role = getattr(user, 'role', None)
            if user_role not in self.allowed_roles:
                return HttpResponseForbidden("You do not have permission to access this resource.")

        return self.get_response(request)