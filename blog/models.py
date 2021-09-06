from django.db import models

from django.db import models
from Friend.models import User
from taggit.manager import TaggableManager

from django.utils import timezone
from django.urls import reverse


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField(max_length=1000)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    tags = TaggableManager()


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post-detail', kwargs={'pk': self.pk})


class Reply(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    answer = models.CharField(max_length=2000)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    likes = models.IntegerField()
    dislikes = models.IntegerField()

    def __str__(self):
        return (self.post.title, self.author)
