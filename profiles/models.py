from django.db import models
from django.contrib.auth.models import User
from multiselectfield import MultiSelectField
from django.db.models.signals import post_save


MEDIUM = (
    ("HARDBACK", "Hardback"),
    ("PAPERBACK", "Paperback"),
    ("EBOOK", "E-Book"),
    ("AUDIO", "Audiobook")
    )
YES_NO = ((0, "No"), (1, "Yes"))


class Profile(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255, blank=True)
    age = models.CharField(max_length=2, blank=True)
    medium = MultiSelectField(choices=MEDIUM, default=None, max_length=9)
    favourite_quote = models.TextField(blank=True)
    image = models.ImageField(
        upload_to='images/', default='../default_profile_qdjgyp'
    )
    visibility = models.IntegerField(choices=YES_NO, default=1)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.owner}'s profile"


def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(owner=instance)


post_save.connect(create_profile, sender=User)
