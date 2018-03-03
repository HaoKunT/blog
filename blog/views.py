from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage #实现分页功能
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from blog.models import Article
from .forms import UserForm
import markdown
import codecs

# Create your views here.




# 判断是否登录
def isLogin(request):
    if request.user.is_authenticated:
        return {'isLogin': True, 'username': request.user.username}
    else:
        return {'isLogin': False}



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
    context = isLogin(request)
    context['post_list'] = posts
    context['pages'] = pages
    return render(request, 'blog/home.html', context)

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
    context = isLogin(request)
    context['post'] = post
    return render(request, 'blog/post.html', context)

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
        context = isLogin(request)
    context['content'] = content
    return  render(request, 'blog/aboutme.html', context)

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
    context = isLogin(request)
    context['post_list'] = posts
    context['pages'] = pages
    context['request'] = request
    return render(request, 'blog/search.html', {'post_list': posts, 'pages': pages, 'request': request})

# 返回登录界面
def signinhtml(request):
    context = isLogin(request)
    if context['isLogin']:
        return HttpResponseRedirect("/blog/home")
    context.update({'wrong': False})
    return render(request, "blog/signin.html", context)

# 返回注册界面
def signuphtml(request):
    localcontext = {
        'userexists': False,
        'wrong': False
    }
    context = isLogin(request)
    if context['isLogin']:
        return HttpResponseRedirect("/blog/home")
    context.update(localcontext)
    return render(request, "blog/signup.html", context)

# 登录
def signin(request):
    context = isLogin(request)
    if context['isLogin']:
        return HttpResponseRedirect("/blog/home")
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            # 获取表单用户密码
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # 获取的表单数据与数据库进行比较
            user = authenticate(username=username, password=password)
            if user:
                # 比较成功，跳转index
                login(request, user)
                request.session['username'] = username
                return HttpResponseRedirect("/blog/home")
            else:
                # 比较失败，还在login
                context.update({'wrong': True})
                return render(request, 'blog/signin.html', context)
        else:
            context.update({'wrong': True})
    else:
        return HttpResponseRedirect('/blog/sign/signin')
    return render(request, 'blog/signin.html', context)

# 注册
def signup(request):
    context = isLogin(request)
    if context['isLogin']:
        return HttpResponseRedirect("/blog/home")
    localcontext = {
        'userexists': False,
        'wrong': False
    }
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            try:
                user = User.objects.get(username= username)
                localcontext['userexists'] = True
                context.update(localcontext)
                return render(request, 'blog/signup.html', context)
            except:
                user = User.objects.create_user(username=username, password=password)
                user.save()
                group = Group.objects.get(name="blog")
                user.groups.add(group)

                # 添加session
                request.session['username'] = username

                # 重定向到home
                return HttpResponseRedirect("/blog/home")
        else:
            localcontext['wrong'] = True
    else:
        return HttpResponseRedirect('/blog/sign/signup')
    context.update(localcontext)
    return render(request, 'blog/signup.html', context)

# 登出
def logout_view(request):
    #清理cookie里保存username
    logout(request)
    return HttpResponseRedirect('/blog/home')