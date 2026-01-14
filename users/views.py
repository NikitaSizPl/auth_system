from rest_framework.views import APIView
from rest_framework.response import Response
from users.models import AppUser
from users.security import hash_password, check_password, generate_token
from access.models import Role
from .permissions import HasAccess

# {
# "email":"test@gmail.com",
# "password":"test123",
# "password_repeat":"test123",
# "first_name":"test",
# "last_name":"test",
# "role":"user"
# }


# Образ создания пользователя
class RegisterView(APIView):
    def post(self, request):
        data = request.data
        if data['password'] != data['password_repeat']:
            return Response({'error': 'Passwords do not match'}, status=400)

        role = Role.objects.get(name='user')
        user = AppUser.objects.create(
            email=data['email'],
            password=hash_password(data['password']),
            first_name=data['first_name'],
            last_name=data['last_name'],
            role=role
        )
        return Response({'id': user.id})


# образ авторизации
class LoginView(APIView):
    def post(self, request):
        data = request.data
        user = AppUser.objects.filter(email=data['email'], is_active=True).first()
        if not user or not check_password(data['password'], user.password):
            return Response(status=401)
        token = generate_token(user.id)
        return Response({'access_token': token})


# Выход
class LogoutView(APIView):
    def post(self, request):
        return Response(status=204)


# Профиль пользователя
class ProfileView(APIView):
    def get(self, request):
        u = request.user
        return Response({
            'id': u.id,
            'email': u.email,
            'first_name': u.first_name,
            'last_name': u.last_name,
            'role': getattr(u.role, 'name', None)  
        })

    def patch(self, request):
        if not request.user.is_authenticated:
            return Response(status=401)
        for field in ['first_name', 'last_name', 'email']:
            if field in request.data:
                setattr(request.user, field, request.data[field])
        if 'password' in request.data:
            request.user.password = hash_password(request.data['password'])
        request.user.save()
        return Response(status=200)

    def delete(self, request):
        if not request.user.is_authenticated:
            return Response(status=401)
        request.user.is_active = False
        request.user.save()
        return Response(status=204)


# Все пользователи
class UserListView(APIView):
    permission_classes = [HasAccess]
    resource_name = 'users'

    def get(self, request):
        users = AppUser.objects.filter(is_active=True)
        return Response([
            {
                'id': u.id,
                'email': u.email,
                'first_name': u.first_name,
                'last_name': u.last_name,
                'role': u.role.name
            }
            for u in users
        ])
    
    