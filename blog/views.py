from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.core.paginator import Paginator, EmptyPage #实现分页功能
from blog.models import Article
# from datetime import datetime
import markdown

# Create your views here.

def home(request,id='1'):
    id=int(id)
    post_list = Article.objects.all()

    paginator = Paginator(post_list, 5)

    try:
        pages = paginator.page(id)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        pages = paginator.page(paginator.num_pages)

    posts = pages.object_list


    for post in posts:
        post.content = markdown.markdown(post.content, extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
        ])
    return render(request, 'blog/home.html', {'post_list': posts, 'pages': pages})

def Detail(request,id):
    try:
        post = Article.objects.get(id=str(id))
    except Article.DoesNotExist:
        raise Http404
    post.content = markdown.markdown(post.content, extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
    ])
    return render(request, 'blog/post.html', {'post':post})
