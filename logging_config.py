import logging
import threading



local = threading.local()



class LoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.logger = logging.getLogger('django.request')

    def __call__(self, request):
        username = 'AnonymousUser'
        if request.user.is_authenticated:
            username = request.user.user  # Ensure user model has a user field
        
        self.logger.info(f"Request from user '{username}': {request.method} {request.get_full_path()}")
        
        response = self.get_response(request)
        
        self.logger.info(f"Response for user '{username}': {response.status_code}")
        # print(response, username,"++____________________________")
        setattr(local, 'user', username)
        return response

class LoggedInUsernameFilter(logging.Filter):
    def filter(self, record):
        username = getattr(local, 'user', None)
        if username:
            record.username = username
        else:
            record.username = '-'
        return True
