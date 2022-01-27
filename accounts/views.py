from django.views.generic import FormView
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import AuthenticationForm
from django.utils.http import url_has_allowed_host_and_scheme
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login

from mixins.mixins import PermissionRequiredMixin
from .constants import roles
from .forms import UserCreateForm

User = get_user_model()


class UserLoginView(LoginView):
    template_name = 'accounts/login.html'
    success_url = reverse_lazy('portal:dashboard_index')
    form_class = AuthenticationForm
    redirect_field_name = REDIRECT_FIELD_NAME

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('portal:dashboard_index'))

        return super(UserLoginView, self).get(request, *args, **kwargs)

    @method_decorator(sensitive_post_parameters('password'))
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):

        # Sets a test cookie to make sure the user has cookies enabled
        request.session.set_test_cookie()

        return super(UserLoginView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        auth_login(self.request, form.get_user())

        # If the test cookie worked, go ahead and
        # delete it since its no longer needed
        if self.request.session.test_cookie_worked():
            self.request.session.delete_test_cookie()

        return super(UserLoginView, self).form_valid(form)

    def get_success_url(self):
        redirect_to = self.request.GET.get(self.redirect_field_name)
        if not url_has_allowed_host_and_scheme(url=redirect_to, allowed_hosts=self.request.get_host()):
            redirect_to = self.success_url
        messages.success(self.request, 'Welcome {}!'.format(self.request.user.username))
        return redirect_to


class UserLogoutView(LoginRequiredMixin, LogoutView):
    def get_next_page(self):
        messages.success(self.request, 'You have logged out!')
        return reverse_lazy('accounts:login')


class UserCreateView(LoginRequiredMixin, PermissionRequiredMixin, FormView):
    roles_required = [roles.get('admin')]
    template_name = 'accounts/user_create.html'
    form_class = UserCreateForm

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        email = form.cleaned_data.get('email')
        first_name = form.cleaned_data.get('first_name')
        last_name = form.cleaned_data.get('last_name')
        password = form.cleaned_data.get('password')
        role = form.cleaned_data.get('role')

        user = User.objects.create(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name
        )
        user.set_password(password)
        user.save()
        user.profile.roles.add(*role)
        user.profile.save()

        return super(UserCreateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, 'User is Successfully Created!')
        return reverse_lazy('accounts:user_create')
