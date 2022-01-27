from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Room(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255, null=True, blank=False, verbose_name='Name')
    number_of_seats = models.PositiveIntegerField(default=0, verbose_name='Number of Seats')
    time_of_availability = models.DateTimeField(null=True, blank=False,
                                                verbose_name='Time of Availability')

    class Meta:
        verbose_name = 'Room'
        verbose_name_plural = 'Rooms'
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class Reserve(models.Model):
    reserved_by = models.ForeignKey(User, null=True, blank=False, on_delete=models.CASCADE,
                                    verbose_name='Reserver')
    room = models.ForeignKey(Room, null=True, blank=False, on_delete=models.CASCADE,
                             verbose_name='Room')
    reserve_from = models.DateTimeField(null=True, blank=False, verbose_name='Reserve from')
    reserve_to = models.DateTimeField(null=True, blank=False, verbose_name='Reserve to')

    class Meta:
        ordering = ['-reserve_from']

    def __str__(self):
        return str(self.id)
