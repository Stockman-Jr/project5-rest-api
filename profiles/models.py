from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class TrainerProfile(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255, blank=True)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(
        upload_to='profile_avatars/', default='../mew_avatar_z7mnbd'
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.owner}'s trainer profile"


def create_profile(sender, instance, created, **kwargs):
    if created:
        TrainerProfile.objects.create(owner=instance)


post_save.connect(create_profile, sender=User)
