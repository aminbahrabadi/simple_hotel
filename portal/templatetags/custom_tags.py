from django import template
from django.shortcuts import get_object_or_404
from django.utils import timezone

from accounts.constants import roles
from rooms.models import Reserve

register = template.Library()


@register.filter()
def can_edit(reserve_id, user):
    now = timezone.now()
    reserve = Reserve.objects.get(id=reserve_id)
    if reserve.reserved_by == user and reserve.reserve_from > now:
        return True

    return False


@register.filter()
def can_cancel(user):
    if user.profile.roles.filter(name__in=[roles.get('room_manager')]).exists():
        return True

    return False
