from django.contrib import admin
from .models import Profile, UserPost, Comment, Friend

admin.site.register(Profile)
admin.site.register(UserPost)
admin.site.register(Comment)
admin.site.register(Friend)
