from comments.models import Comment
from django.contrib import admin


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass
