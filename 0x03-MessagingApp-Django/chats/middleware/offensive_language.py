# chats/middleware.py
from datetime import datetime, time
from django.http import HttpResponseForbidden
    

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
    