from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from access.models import AccessRule, Role, BusinessElement
from access.services import has_permission
from django.shortcuts import get_object_or_404


class AccessRuleView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Проверка прав через твою функцию
        if not has_permission(request.user, 'access_rules', 'read'):
            return Response(status=403)

        rules = AccessRule.objects.select_related('role', 'element').all()

        data = [{
            'id': r.id,
            'role': r.role.name,
            'element': r.element.code,
            'read': r.read_permission,
            'read_all': r.read_all_permission,
            'create': r.create_permission,
            'update': r.update_permission,
            'update_all': r.update_all_permission,
            'delete': r.delete_permission,
            'delete_all': r.delete_all_permission
        } for r in rules]

        return Response(data)

    def post(self, request):
        if not has_permission(request.user, 'access_rules', 'create'):
            return Response(status=403)

        data = request.data
        try:
            role = Role.objects.get(name=data['role'])
        except Role.DoesNotExist:
            return Response({'error': 'Role not found'}, status=404)

        try:
            element = BusinessElement.objects.get(code=data['element'])
        except BusinessElement.DoesNotExist:
            return Response({'error': 'Element not found'}, status=404)

        rule = AccessRule.objects.create(
            role=role,
            element=element,
            read_permission=bool(data.get('read', False)),
            read_all_permission=bool(data.get('read_all', False)),
            create_permission=bool(data.get('create', False)),
            update_permission=bool(data.get('update', False)),
            update_all_permission=bool(data.get('update_all', False)),
            delete_permission=bool(data.get('delete', False)),
            delete_all_permission=bool(data.get('delete_all', False))
        )

        return Response({'id': rule.id}, status=201)

    def patch(self, request, rule_id):
        if not has_permission(request.user, 'access_rules', 'update'):
            return Response(status=403)

        rule = get_object_or_404(AccessRule, id=rule_id)

        for field in [
            'read_permission', 'read_all_permission', 'create_permission',
            'update_permission', 'update_all_permission',
            'delete_permission', 'delete_all_permission'
        ]:
            if field in request.data:
                setattr(rule, field, bool(request.data[field]))

        rule.save()
        return Response(status=200)

    def delete(self, request, rule_id):
        if not has_permission(request.user, 'access_rules', 'delete'):
            return Response(status=403)

        rule = get_object_or_404(AccessRule, id=rule_id)
        rule.delete()
        return Response(status=204)


class OrdersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not request.user:
            return Response(status=401)

        if not has_permission(request.user, 'orders', 'read'):
            return Response(status=403)

        orders = [
            {'id': 1, 'owner': 'user1'},
            {'id': 2, 'owner': 'user2'}
        ]
        # orders = Order.objects.select_related('owner').all()
        # orders = [{'id': o.id, 'owner': o.owner.username} for o in orders]

        return Response(orders)
