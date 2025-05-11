from django.contrib.auth.backends import BaseBackend
from authentication.models import BlogUser

class BlogUserBackend(BaseBackend):
    def authenticate(self, request, email, password):
        if not email or not password:
            return None
        
        try:
            user = BlogUser.objects.get(email = email)
        except:
            return None
        if user.check_password(password):
            return user
        else:
            return None
    
    def get_user(self, user_id):
        try:
            user = BlogUser.objects.get(id = id)
        except:
            return None
        return user