from comments.models import Comment
from django.contrib import admin
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory


class TreePostContentsAdmin(TreeAdmin):
    form = movenodeform_factory(Comment)


admin.site.register(Comment, TreePostContentsAdmin)
