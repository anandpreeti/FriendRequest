from django.shortcuts import render

from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from .models import Post, Reply, Thread
from django.urls import reverse

def home(request):
    return render(request, 'blog/home.html', {'title': 'Home'})

def details(request,post_id ,**kwargs):
    post = Post.objects.get(pk)
    context = {
        'title': post.title,

    }
    return render(request, 'blog/post_detail.html', context)



class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'

    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

class PostCreateView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content', 'subject']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    login_url = '/login/'
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    login_url = '/login/'
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = '/blog/'


    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})

def vote(request, reply_id):
    selected_choice = get_object_or_404(Reply, pk=reply_id)

    selected_choice.votes += 1
    selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
    #return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
    return HttpResponseRedirect(reverse('blog:post-detail', args=(selected_choice.post.id,)))

class ThreadCreateView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    model = Thread
    template_name = 'thread/thread_form.html'
    fields = ['sub', 'post']

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)




