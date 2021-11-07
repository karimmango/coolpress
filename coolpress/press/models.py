from datetime import datetime, timedelta, timezone
from enum import Enum

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

from .user_management import get_gravatar_link, get_github_repositories, get_github_followers, get_github_following

class CoolUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    github_profile = models.CharField(max_length=150, null=True, blank=True)
    gh_repositories = models.IntegerField(null=True, blank=True)
    gravatar_link = models.CharField(max_length=400, null=True, blank=True)
    gh_followers = models.IntegerField(null=True, blank=True)
    gh_following = models.IntegerField(null=True, blank=True)
    last_followers_check = models.DateTimeField(null=True, blank=True)


    def __str__(self):
        user = self.user
        return f'{user.first_name} {user.last_name} ({user.username})'

    def save(self, *args, **kwargs):
        super(CoolUser, self).save(*args, **kwargs)

        if self.user.email:
            email = self.user.email
            gravatar_link = get_gravatar_link(email)
            if gravatar_link != self.gravatar_link:
                self.gravatar_link = gravatar_link
                self.save()

        date_now = datetime.now()
        date_now += timedelta(days=1)
        date_diff = self.last_followers_check
        date_diff += timedelta(days=1)

        gh_following = None
        gh_followers = None
        gh_repositories = None
        if self.github_profile and (not self.last_followers_check or date_now > date_diff):
            gh_repositories = get_github_repositories(self.github_profile)
            gh_following = get_github_following(self.github_profile)
            gh_followers = get_github_followers(self.github_profile)
            self.last_followers_check = timezone.now()
            self.save()
        if gh_repositories != self.gh_repositories:
            self.gh_repositories = gh_repositories
            self.save()
        if gh_followers != self.gh_followers:
            self.gh_followers = gh_followers
            self.save()
        if gh_following != self.gh_following:
            self.gh_following = gh_following
            self.save()

class Category(models.Model):
    class Meta:
        verbose_name_plural = "categories"

    label = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    def get_absolute_url(self):
        return reverse('category-detail', kwargs={'pk': self.pk})

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
    title = models.CharField(max_length=400)
    body = models.TextField()
    image_link = models.CharField(max_length=400, null=True, blank=True)

    word_cloud_link = models.CharField(max_length=400, null=True, blank=True)

    source_link = models.CharField(max_length=400, null=True, blank=True)
    source_label = models.CharField(max_length=400, null=True, blank=True)

    status = models.CharField(
        max_length=32,
        choices=POST_LABELED_STATUS,
        default=PostStatus.DRAFT,
    )

    author = models.ForeignKey(CoolUser, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    creation_date = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title} - by {self.author.user.username}'