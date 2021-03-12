from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from django.contrib.auth.models import User
from django.contrib import  messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin




def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request,'blog/home.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    paginate_by = 5
        


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

class PostDetailView(DetailView):
    model = Post

class PostCreateView(LoginRequiredMixin,CreateView):
    permission_denied_message = 'You need to login to post an entry !'
    model = Post
    fields = ['title','content']

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.add_message(request,messages.INFO, self.permission_denied_message)
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def  form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, f'Post Created ! ')
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Post
    fields = ['title','content']

    def  form_valid(self, form,):
        form.instance.author = self.request.user
        messages.success(self.request, f'Post Updated ! ')
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if  self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if  self.request.user == post.author:
            return True
        return False



        

def about(request):
    return render(request,'blog/about.html', {'title':'About'})




