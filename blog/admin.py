from django.contrib import admin
from blog.models import Article, Comment
from markdownx.admin import MarkdownxModelAdmin

# Register your models here.

class ArticleAdmin(MarkdownxModelAdmin):
    list_display = ('title', 'blog_user', 'category', 'pub_date', 'update_time')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('comment_user', 'content', 'article', 'com_time')


admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment, CommentAdmin)