def has_required_role(user, roles_required):
    if user.is_superuser:
        return True

    user_roles = user.profile.roles.all()

    if roles_required:
        if user_roles.filter(name__in=roles_required).exists():
            return True

    return False
