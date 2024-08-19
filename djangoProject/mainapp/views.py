from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Forum, Post, Profile  # 导入模型
from django.contrib.auth.decorators import login_required  # 导入装饰器

def home(request):
    # 查询所有用户的论坛
    forums = Forum.objects.all()
    # 查询所有用户的帖子标题
    posts = Post.objects.all()

    # 传递给模板
    return render(request, 'mainapp/Home.html', {
        'forums': forums,
        'posts': posts
    })

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # 登录成功后重定向到主页
        else:
            messages.error(request, '用户名或密码错误')
    return render(request, 'mainapp/login_register.html')

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, '用户名已存在')
            else:
                user = User.objects.create_user(username=username, password=password1)
                user.save()
                Profile.objects.create(user=user)  # 创建用户时创建对应的 Profile
                messages.success(request, '注册成功，请登录')
                return redirect('login')
        else:
            messages.error(request, '两次密码不一致')
    return render(request, 'mainapp/login_register.html')


@login_required
def user_profile_view(request):
    profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        email = request.POST.get('email')
        city = request.POST.get('city')
        phone_number = request.POST.get('phone_number')

        request.user.email = email
        request.user.save()

        profile.city = city
        profile.phone_number = phone_number
        profile.save()

        messages.success(request, '资料已更新')
        return redirect('profile')

    # 假设Post模型有一个user字段
    posts = Post.objects.filter(user=request.user)

    return render(request, 'mainapp/UserProfile.html', {'profile': profile, 'posts': posts})


@login_required
def add_post_view(request):
    forums = Forum.objects.all()

    if not forums.exists():
        # 如果没有论坛，重定向到创建论坛的页面
        return redirect('create_forum')

    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        forum_id = request.POST.get('forum')
        forum = Forum.objects.get(id=forum_id)

        # 创建新帖子并保存
        new_post = Post.objects.create(title=title, content=content, forum=forum, user=request.user)
        new_post.save()

        return redirect('profile')

    return render(request, 'mainapp/add_post.html', {'forums': forums})


@login_required
def create_forum_view(request):
    if request.method == 'POST':
        forum_name = request.POST.get('forum_name')
        description = request.POST.get('description')

        # 创建新的论坛
        forum = Forum.objects.create(name=forum_name, description=description)
        forum.save()

        # 创建论坛后重定向到添加帖子的页面
        return redirect('add_post')

    return render(request, 'mainapp/create_forum.html')

