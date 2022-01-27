from django.core.exceptions import PermissionDenied


class PermissionRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)

        user_roles = request.user.profile.roles.all()
        roles = self.roles_required

        if roles:
            if user_roles.filter(name__in=roles).exists():
                return super().dispatch(request, *args, **kwargs)

        raise PermissionDenied
