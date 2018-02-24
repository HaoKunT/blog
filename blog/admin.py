from django.contrib import admin
from blog.models import Article
from markdownx.admin import MarkdownxModelAdmin

# Register your models here.

class ArticleAdmin(MarkdownxModelAdmin):
    list_display = ('title', 'category', 'pub_date', 'update_time')


admin.site.register(Article,ArticleAdmin)