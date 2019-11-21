from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import random

class Post(models.Model):
    objects = models.Manager()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    content = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    postkey = models.CharField(max_length=50)

