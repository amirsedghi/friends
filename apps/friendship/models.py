from __future__ import unicode_literals

from django.db import models

# Create your models here.


class User(models.Model):
    name = models.CharField(max_length = 255)
    alias = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    date_of_birth = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class Friend(models.Model):
    friends = models.ForeignKey(User, related_name = 'thefriends', on_delete = models.CASCADE)
    friend_of = models.ForeignKey(User, related_name = 'the_friend_of', on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
