from django.contrib import admin

from apps.jsonbench.models import Board, Thread, Post, ForumUser

admin.site.register(Board)
admin.site.register(Thread)
admin.site.register(Post)
admin.site.register(ForumUser)
