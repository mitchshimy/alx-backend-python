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