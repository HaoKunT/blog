from django.db import models
from markdownx.models import MarkdownxField

# Create your models here.

class Article(models.Model):
    title = models.CharField("博客标题", max_length=100)
    category = models.CharField("博客标签", max_length=50, blank=True)
    pub_date = models.DateTimeField("发布日期", auto_now_add=True, editable=True)
    update_time = models.DateTimeField("更新日期", auto_now=True, editable=True)
    content = MarkdownxField(blank=True, null=True)

    def __unicode__(self):
        return  self.title

    class Meta:
        ordering = ['-pub_date']
        verbose_name = "文章"
        verbose_name_plural = "文章"
    