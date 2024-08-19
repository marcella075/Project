from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # 主页视图
    path('login/', views.login_view, name='login'),  # 登录视图
    path('register/', views.register_view, name='register'),  # 注册视图
    path('profile/', views.user_profile_view, name='profile'),  # 个人信息视图
    path('add_post/', views.add_post_view, name='add_post'),  # 新增帖子视图
    path('create_forum/', views.create_forum_view, name='create_forum'),  # 新增的创建论坛视图

]
