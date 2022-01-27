from django.contrib import messages
from django.views.generic import TemplateView, RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from accounts.constants import roles
from mixins.mixins import PermissionRequiredMixin
from rooms.models import Room
from accounts.models import Role


class PortalIndexTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'portal/portal_index.html'

    def get_context_data(self, **kwargs):
        context = super(PortalIndexTemplateView, self).get_context_data(**kwargs)

        context['rooms'] = Room.objects.all()

        return context


class DashboardTemplateView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    roles_required = [roles.get('admin'), roles.get('room_manager')]
    template_name = 'portal/admin_index.html'


class CreateRulesRedirectView(LoginRequiredMixin, PermissionRequiredMixin, RedirectView):
    roles_required = [roles.get('admin')]

    def get(self, request, *args, **kwargs):
        for _, role_name in roles.items():
            if not Role.objects.filter(name=role_name).exists():
                Role.objects.create(
                    name=role_name
                )
        return super(CreateRulesRedirectView, self).get(request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        messages.success(self.request, 'Roles are Successfully Created!')
        return reverse_lazy('portal:portal_index')
