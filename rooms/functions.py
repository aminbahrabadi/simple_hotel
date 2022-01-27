from django.utils import timezone
from django.db.models import Q


def room_is_available(room, from_time, to_time, reserve_id=None):
    now = timezone.now()
    filters = Q(reserve_from__gte=now)

    if reserve_id is not None:
        filters &= ~Q(id=reserve_id)

    for item in room.reserve_set.filter(filters):
        if (item.reserve_from <= from_time <= item.reserve_to) or \
                (item.reserve_from <= to_time <= item.reserve_to) or \
                (from_time <= item.reserve_from <= to_time) or \
                (from_time <= item.reserve_to <= to_time):
            return False

    return True
