from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='oser')
    image = models.ImageField(default='default.jpg', upload_to='profile/', blank=False)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

    def __str__(self):
        return f'{self.user.username}(s) profile'

    def get_absolute_url(self):
        return reverse('profile', kwargs={'profile': self.user})
    

class UserPost(models.Model):
    content = models.TextField(blank=True)
    Image = models.ImageField(default=None, blank=False, upload_to='users_post/')
    tags = models.CharField(max_length=100, blank=False)
    datetime = models.DateTimeField(default=timezone.now)
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='likes', blank=True)

    def __str__(self):
        return self.tags

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

    def total_likes(self):
        return self.likes.count()


class Comment(models.Model):
    comment = models.TextField(default=None, blank=True)
    post = models.ForeignKey(UserPost, on_delete=models.CASCADE, default=None)
    username = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    datetime = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.comment

    def get_absolute_url(self):
        return reverse('comments', kwargs={'pk': self.post.pk})


class Friend(models.Model):
    users = models.ManyToManyField(User)
    current_user = models.ForeignKey(User, related_name='owner', null=True, on_delete=models.CASCADE)

    @classmethod
    def make_friend(cls, current_user, new_friend):
        friend, created = cls.objects.get_or_create(current_user=current_user)
        friend.users.add(new_friend)

    @classmethod
    def lose_friend(cls, current_user, new_friend):
        friend, created = cls.objects.get_or_create(
            current_user=current_user
        )
        friend.users.remove(new_friend)

    def following_count(self):
        return self.users.count()
