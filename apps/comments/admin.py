from django.contrib import admin

from apps.comments.models import Comments, Reply_to_comments


class CommentsAdmin(admin.ModelAdmin):
    list_display = ('comment', 'moderated')


class Reply_to_commentsAdmin(admin.ModelAdmin):
    list_display = ('reply',)


admin.site.register(Comments, CommentsAdmin)

admin.site.register(Reply_to_comments, Reply_to_commentsAdmin)
