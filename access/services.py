from access.models import AccessRule


def has_permission(user, element_code, action, is_owner=False):
    if not user:
        return False

    rule = AccessRule.objects.filter(
        role=user.role,
        element__code=element_code
    ).first()

    if not rule:
        return False

    if action == 'read':
        return rule.read_all_permission or (rule.read_permission and is_owner)

    if action == 'create':
        return rule.create_permission

    if action == 'update':
        return rule.update_all_permission or (rule.update_permission and is_owner)

    if action == 'delete':
        return rule.delete_all_permission or (rule.delete_permission and is_owner)

    return False
