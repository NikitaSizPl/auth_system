import jwt
from django.utils.deprecation import MiddlewareMixin
from users.models import AppUser
from users.security import JWT_SECRET, JWT_ALGORITHM


class AuthMiddleware(MiddlewareMixin):

    def process_request(self, request):
        request.user = None

        auth = request.headers.get('Authorization')
        if not auth or not auth.startswith('Bearer '):
            return

        token = auth.split()[1]
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            user = AppUser.objects.filter(
                id=payload['user_id'],
                is_active=True
            ).first()
            request.user = user
        except jwt.ExpiredSignatureError:
            pass
        except jwt.InvalidTokenError:
            pass
