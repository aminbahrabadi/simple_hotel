from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from .constants import roles

User = get_user_model()


class Role(models.Model):
    name = models.CharField(max_length=255, null=True, blank=False)

    def __str__(self):
        return self.name


class Profile(models.Model):
    """
        Profile model
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='User',
                                related_name='profile')
    roles = models.ManyToManyField(Role, blank=True, verbose_name='Roles')

    def save(self, *args, **kwargs):
        if self.user.is_superuser:
            admin_role, _ = Role.objects.get_or_create(name=roles.get('admin'))
            self.roles.add(admin_role)

        return super(Profile, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
        Create profile based on User model.
    """
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
        Save user's profile.
    """
    instance.profile.save()
