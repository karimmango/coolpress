# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from enum import Enum

from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class CoolUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    github_link = models.CharField(max_length=400, null=True, blank=True)
    github_repo = models.IntegerField(null=True, blank=True)
    gravatar_link = models.CharField(max_length=400, null=True, blank=True)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} ({self.user.username})'


class Category(models.Model):
    title = models.CharField(max_length=50)
    slug = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.slug}'


class PostStatus(Enum):
    DRAFT = 'DRAFT'
    PUBLISHED = 'PUBLISHED'


POST_LABELED_STATUS = [
    (PostStatus.DRAFT.value, 'Draft'),
    (PostStatus.PUBLISHED.value, 'Published post'),
]


class Post(models.Model):
    title = models.CharField(max_length=150)
    author_id = models.ForeignKey(CoolUser, on_delete=models.CASCADE)
    body = models.TextField()
    image_link = models.CharField(max_length=400, null=True, blank=True)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    last_update = models.DateTimeField(auto_now=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=32,
        choices=POST_LABELED_STATUS,
        default=PostStatus.DRAFT,)

    def __str__(self):
        return f'{self.title} - by {self.author.user.username}'



