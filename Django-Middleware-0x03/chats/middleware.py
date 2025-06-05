# chats/middleware.py
from datetime import datetime, time
from django.http import HttpResponseForbidden

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get the user or default to 'Anonymous'
        user = request.user if request.user.is_authenticated else 'Anonymous'

        # Log info to file
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}\n"
        with open('requests.log', 'a') as log_file:
            log_file.write(log_message)

        response = self.get_response(request)
        return response

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.start_time = time(18, 0)  # 6 PM
        self.end_time = time(21, 0)    # 9 PM

    def __call__(self, request):
        # Restrict only chat-related paths
        if request.path.startswith('/api/chats/') or request.path.startswith('/chats/'):
            now = datetime.now().time()
            if not (self.start_time <= now <= self.end_time):
                return HttpResponseForbidden("Access to the chat is restricted to 6PM-9PM only.")
        
        return self.get_response(request)
    

class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.message_limit = 5          # max messages
        self.time_window = 60           # time window in seconds (1 minute)
        self.ip_message_log = {}        # stores {ip: [(timestamp), ...]}

    def __call__(self, request):
        # We only limit POST requests to chat endpoints
        if request.method == "POST" and (request.path.startswith('/api/chats/') or request.path.startswith('/chats/')):
            ip = self.get_client_ip(request)
            now = time.time()

            # Initialize list if IP not tracked
            if ip not in self.ip_message_log:
                self.ip_message_log[ip] = []

            # Clean old timestamps outside the time window
            self.ip_message_log[ip] = [t for t in self.ip_message_log[ip] if now - t < self.time_window]

            if len(self.ip_message_log[ip]) >= self.message_limit:
                return HttpResponseForbidden("Message limit exceeded: max 5 messages per minute allowed.")

            # Log this message timestamp
            self.ip_message_log[ip].append(now)

        return self.get_response(request)

    def get_client_ip(self, request):
        # Try X-Forwarded-For first (in case of proxies)
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
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