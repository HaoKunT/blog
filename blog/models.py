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

class Comment(models.Model):
    content = models.CharField("评论内容", max_length=1024)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    com_time = models.DateTimeField("评论日期", auto_now_add=True, editable=True)
    par_comment = models.ForeignKey('self', on_delete=models.CASCADE)

    def __unicode__(self):
        return self.content

    class Meta:
        ordering = ['-com_time']
        verbose_name = "评论"
        verbose_name_plural = "评论"