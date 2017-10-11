from django.db import models
from django.contrib.auth.models import User

class Board(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name

class Thread(models.Model):
    name = models.CharField(max_length=255)
    board = models.ForeignKey(Board)
    
    def __str__(self):
        return self.name

class Post(models.Model):
    name = models.CharField(max_length=255)
    thread = models.ForeignKey(Thread)
    readers = models.ManyToManyField(User)
    
    def __str__(self):
        return self.name
