
from rest_framework.views import APIView
from rest_framework.response import Response
from access.models import AccessRule, Role, BiznessElement
from access.services import has_permission

class AccessRuleView(APIView):
    def get(self, request):
        if not request.user:
            return Response(status=401)
        if not has_permission(request.user, 'access_rules', 'read'):
            return Response(status=403)
        rules = AccessRule.objects.all()
        return Response([{
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
        } for r in rules])

    def post(self, request):
        if not request.user:
            return Response(status=401)
        if not has_permission(request.user, 'access_rules', 'create'):
            return Response(status=403)
        data = request.data
        role = Role.objects.get(name=data['role'])
        element = BiznessElement.objects.get(code=data['element'])
        rule = AccessRule.objects.create(
            role=role,
            element=element,
            read_permission=data.get('read', False),
            read_all_permission=data.get('read_all', False),
            create_permission=data.get('create', False),
            update_permission=data.get('update', False),
            update_all_permission=data.get('update_all', False),
            delete_permission=data.get('delete', False),
            delete_all_permission=data.get('delete_all', False)
        )
        return Response({'id': rule.id})

    def patch(self, request, rule_id):
        if not request.user:
            return Response(status=401)
        if not has_permission(request.user, 'access_rules', 'update'):
            return Response(status=403)
        rule = AccessRule.objects.get(id=rule_id)
        for field in ['read_permission', 'read_all_permission', 'create_permission',
                      'update_permission', 'update_all_permission',
                      'delete_permission', 'delete_all_permission']:
            if field in request.data:
                setattr(rule, field, request.data[field])
        rule.save()
        return Response(status=200)

    def delete(self, request, rule_id):
        if not request.user:
            return Response(status=401)
        if not has_permission(request.user, 'access_rules', 'delete'):
            return Response(status=403)
        rule = AccessRule.objects.get(id=rule_id)
        rule.delete()
        return Response(status=204)



class OrdersView(APIView):
    def get(self, request):
        if not request.user:
            return Response(status=401)

        if not has_permission(request.user, 'orders', 'read'):
            return Response(status=403)

        return Response([
            {'id': 1, 'owner': 'user1'},
            {'id': 2, 'owner': 'user2'}
        ])
