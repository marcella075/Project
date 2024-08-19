# mainapp/views.py
from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def profile(request):
    return render(request, 'profile.html')

def forum(request):
    return render(request, 'forum.html')

def post_detail(request, id):
    # 假设你要从数据库中获取某个帖子
    # post = get_object_or_404(Post, id=id)
    # context = {'post': post}
    return render(request, 'post_detail.html')  # 可以传递上下文数据
