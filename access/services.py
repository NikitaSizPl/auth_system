from access.models import AccessRule

ADMIN_ROLE_NAME = "admin"

def has_permission(user, element_code, action, is_owner=None):
    if not user or not user.is_authenticated:
        return False

    user_role = getattr(user, "role", None)

    if user_role and getattr(user_role, "name", None) == ADMIN_ROLE_NAME:
        return True

    if isinstance(user_role, str) and user_role == ADMIN_ROLE_NAME:
        return True

    if not user_role:
        return False

    rule = AccessRule.objects.filter(
        role=user_role,
        element__code=element_code
    ).first()

    if not rule:
        return False

    if action == 'read':
        if is_owner is None:
            return rule.read_all_permission or rule.read_permission
        return rule.read_all_permission or (rule.read_permission and bool(is_owner))

    if action == 'create':
        return rule.create_permission

    if action == 'update':
        if is_owner is None:
            return rule.update_all_permission or rule.update_permission
        return rule.update_all_permission or (rule.update_permission and bool(is_owner))

    if action == 'delete':
        if is_owner is None:
            return rule.delete_all_permission or rule.delete_permission
        return rule.delete_all_permission or (rule.delete_permission and bool(is_owner))

    return False
