from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage #实现分页功能
from blog.models import Article
# from datetime import datetime
import markdown
import codecs

# Create your views here.

# 博客主页
def home(request,id='1'):
    # 第一部分用来处理页码跳转
    if 'jumpto' in request.GET:
        return HttpResponseRedirect('/blog/home/{}/'.format(request.GET['jumpto']))

    # 第二部分用来正常处理
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
            'markdown.extensions.sane_lists',
            'markdown.extensions.nl2br',
        ])
    return render(request, 'blog/home.html', {'post_list': posts, 'pages': pages})

# 博客文章
def Detail(request,id):
    try:
        post = Article.objects.get(id=str(id))
    except Article.DoesNotExist:
        raise Http404
    post.content = markdown.markdown(post.content, extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
        'markdown.extensions.sane_lists',
        'markdown.extensions.nl2br',
    ])
    return render(request, 'blog/post.html', {'post':post})

# 关于部分
def aboutme(request):
    with codecs.open('custom_file/aboutme.md', encoding='utf-8') as f:
        content = f.read()
        content = markdown.markdown(content, extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
            'markdown.extensions.sane_lists',
            'markdown.extensions.nl2br',
        ])
    return  render(request, 'blog/aboutme.html', {'content' : content})

# 搜索部分
def search(request,id="1"):
    searchcategory = request.GET['category']
    searchcontent = request.GET['content']
    searchtitle = request.GET['title']

    # 第一部分用来处理页码跳转
    if 'jumpto' in request.GET:
        return HttpResponseRedirect('/blog/search/{}/?title={}&content={}&category={}'.format(request.GET['jumpto'],
                                                                                              searchtitle,
                                                                                              searchcontent,
                                                                                              searchcategory))

    # 第二部分用来正常处理
    id = int(id)
    # searchcategory = None
    # searchcontent = None
    # searchtitle = None



    post_list = Article.objects.all()

    for item in ['content', 'category', 'title']:
        res = eval("search{} == ''".format(item))
        if not res:
            post_list = eval("post_list.filter({}__icontains=search{})".format(item, item))

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
            'markdown.extensions.sane_lists',
            'markdown.extensions.nl2br',
        ])
    return render(request, 'blog/search.html', {'post_list': posts, 'pages': pages, 'request': request})
