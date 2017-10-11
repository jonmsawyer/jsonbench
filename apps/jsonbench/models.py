from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

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
    
    def __str__(self):
        return self.name

class ForumUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    posts_read = models.TextField(blank=True, null=True)

    def __str__(self):
        return '{} (posts read:{})'.format(self.user.username, self.posts_read)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        ForumUser.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.forumuser.save()
