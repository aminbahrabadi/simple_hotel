from django.utils import timezone
from django.views.generic import DetailView, CreateView, ListView, UpdateView, RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.urls import reverse_lazy

from accounts.constants import roles
from mixins.mixins import PermissionRequiredMixin
from .models import Room, Reserve
from .forms import RoomForm, ReserveForm
from .functions import room_is_available


class RoomCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    roles_required = [roles.get('room_manager')]
    template_name = 'rooms/room_create_update.html'
    form_class = RoomForm

    def get_success_url(self):
        messages.success(self.request, 'Room is Successfully Created!')
        return reverse_lazy('rooms:room_create')


class RoomReserveCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    roles_required = [roles.get('room_user')]
    template_name = 'rooms/room_reserve_create_update.html'
    form_class = ReserveForm

    def form_valid(self, form):
        reserve = form.save(commit=False)
        room_id = self.kwargs.get('room_id')
        room = get_object_or_404(Room, id=room_id)
        now = timezone.now()

        if reserve.reserve_from < now:
            messages.error(self.request, 'Your reservation start time can not be before now!')
            return self.form_invalid(form)

        if reserve.reserve_from < room.time_of_availability:
            messages.error(self.request, 'Room is not available at this time!')
            return self.form_invalid(form)

        if not room_is_available(room, reserve.reserve_from, reserve.reserve_to):
            messages.error(self.request, 'Room is not Available in time range you have chosen!!')
            return self.form_invalid(form)

        reserve.reserved_by = self.request.user
        reserve.room_id = room_id

        return super(RoomReserveCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(RoomReserveCreateView, self).get_context_data(**kwargs)
        room_id = self.kwargs.get('room_id')
        context['room_id'] = room_id
        context['room'] = get_object_or_404(Room, id=room_id)
        return context

    def get_success_url(self):
        room_id = self.kwargs.get('room_id')
        messages.success(self.request, 'Room is Successfully Reserved!')
        return reverse_lazy('rooms:room_reserve_create', kwargs={'room_id': room_id})


class RoomReserveUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    roles_required = [roles.get('room_user')]
    template_name = 'rooms/room_reserve_create_update.html'
    form_class = ReserveForm

    def get_object(self, queryset=None):
        reserve_id = self.kwargs.get('reserve_id')
        now = timezone.now()
        reserve = get_object_or_404(Reserve, id=reserve_id,
                                    reserved_by_id=self.request.user.id,
                                    reserve_from__gt=now)
        return reserve

    def form_valid(self, form):
        reserve = form.save(commit=False)
        room = self.object.room
        now = timezone.now()

        if reserve.reserve_from < now:
            messages.error(self.request, 'Your reservation start time can not be before now!')
            return self.form_invalid(form)

        if reserve.reserve_from < room.time_of_availability:
            messages.error(self.request, 'Room is not available at this time!')
            return self.form_invalid(form)

        if not room_is_available(room, reserve.reserve_from, reserve.reserve_to, reserve.id):
            messages.error(self.request, 'Room is not Available in time range you have chosen!!')
            return self.form_invalid(form)

        return super(RoomReserveUpdateView, self).form_valid(form)

    def get_success_url(self):
        reserve_id = self.kwargs.get('reserve_id')
        messages.success(self.request, 'Reserve is Successfully Edited!')
        return reverse_lazy('rooms:room_reserve_edit', kwargs={'reserve_id': reserve_id})


class RoomDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    roles_required = [roles.get('room_user')]
    template_name = 'rooms/room_detail.html'
    context_object_name = 'room'

    def get_object(self, queryset=None):
        room_id = self.kwargs.get('room_id')
        room = get_object_or_404(Room, id=room_id)
        return room


class RoomReserveCancelRedirectView(LoginRequiredMixin, PermissionRequiredMixin, RedirectView):
    roles_required = [roles.get('room_manager')]

    def get(self, request, *args, **kwargs):
        reserve_id = self.kwargs.get('reserve_id')
        reserve = get_object_or_404(Reserve, id=reserve_id)
        reserve.delete()
        return super(RoomReserveCancelRedirectView, self).get(request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        room_id = self.kwargs.get('room_id')
        messages.success(self.request, 'Reserve is Successfully Canceled!')
        return reverse_lazy('rooms:room_detail', kwargs={'room_id': room_id})
