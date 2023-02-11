from django.db import models
from django.contrib.auth.models import User
from posts.models import BasePost


class Like(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(BasePost, related_name="likes", on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['owner', 'post']

    def __str__(self):
        return f"{self.owner} {self.post}"
