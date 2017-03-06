from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Article(models.Model):
    article_id = models.IntegerField(primary_key=True)
    title = models.TextField()
    url = models.URLField()
    publisher = models.TextField()


class Feed(models.Model):
    feedname = models.CharField(primary_key=True, max_length=200)
    articles = models.ManyToManyField(Article)


class UserInfo(models.Model):
    username = models.CharField(primary_key=True, max_length=200)
    feeds = models.ManyToManyField(Feed)