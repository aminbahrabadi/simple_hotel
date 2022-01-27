from django import forms
from .models import Room, Reserve


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['name', 'number_of_seats', 'time_of_availability']


class ReserveForm(forms.ModelForm):
    class Meta:
        model = Reserve
        fields = ['reserve_from', 'reserve_to']
