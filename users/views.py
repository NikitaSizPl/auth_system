from rest_framework.views import APIView
from rest_framework.response import Response
from users.models import AppUser
from users.security import hash_password, check_password, generate_token
from access.services import has_permission
from rest_framework.permissions import IsAuthenticated

class RegisterView(APIView):
    def post(self, request):
        data = request.data
        if data['password'] != data['password_repeat']:
            return Response({'error': 'Passwords do not match'}, status=400)

        from access.models import Role
        role = Role.objects.get(name='user')
        user = AppUser.objects.create(
            email=data['email'],
            password=hash_password(data['password']),
            first_name=data['first_name'],
            last_name=data['last_name'],
            role=role
        )
        return Response({'id': user.id})


class LoginView(APIView):
    def post(self, request):
        data = request.data
        user = AppUser.objects.filter(email=data['email'], is_active=True).first()
        if not user or not check_password(data['password'], user.password):
            return Response(status=401)
        token = generate_token(user.id)
        return Response({'access_token': token})


class LogoutView(APIView):
    def post(self, request):
        return Response(status=204)


class ProfileView(APIView):
    def get(self, request):
        if not request.user:
            return Response(status=401)
        u = request.user
        return Response({
            'id': u.id,
            'email': u.email,
            'first_name': u.first_name,
            'last_name': u.last_name,
            'role': u.role.name
        })

    def patch(self, request):
        if not request.user:
            return Response(status=401)
        for field in ['first_name', 'last_name', 'email']:
            if field in request.data:
                setattr(request.user, field, request.data[field])
        if 'password' in request.data:
            request.user.password = hash_password(request.data['password'])
        request.user.save()
        return Response(status=200)

    def delete(self, request):
        if not request.user:
            return Response(status=401)
        request.user.is_active = False
        request.user.save()
        return Response(status=204)


class UserListView(APIView):
    
    def get(self, request):
        if not request.user:
            return Response(status=401)
        if not has_permission(request.user, 'users', 'read'):
            return Response(status=403)
        users = AppUser.objects.filter(is_active=True)
        return Response([{
            'id': u.id,
            'email': u.email,
            'first_name': u.first_name,
            'last_name': u.last_name,
            'role': u.role.name
        } for u in users])
