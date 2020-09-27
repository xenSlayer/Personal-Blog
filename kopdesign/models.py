from django.db import models
from django.utils import timezone


class HomePosts(models.Model):
    content = models.TextField()
    linkToImg = models.URLField()
    datetime = models.DateTimeField(default=timezone.now)
    url = models.URLField(default=None)

    def __str__(self):
        return self.content
