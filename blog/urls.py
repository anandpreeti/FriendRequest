from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    ThreadCreateView,
    UserPostListView,
)
from . import views

app_name = 'blog'
urlpatterns = [
    path('', PostListView.as_view(), name='blog_home'),
    path('user/<str:username>/', UserPostListView.as_view(), name='user-posts'),
    #path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/details/<int:pk>/',views.details, name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('thread/new/', ThreadCreateView.as_view(), name='thread-create'),
    path('about/', views.about, name='blog_about'),
]