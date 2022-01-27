from django.contrib import admin
from .models import Room, Reserve


class ReserveAdmin(admin.ModelAdmin):
    list_display = ['room', 'reserve_from', 'reserve_to']


admin.site.register(Room)
admin.site.register(Reserve, ReserveAdmin)
