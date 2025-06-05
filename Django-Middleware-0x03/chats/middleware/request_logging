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
