from datetime import timedelta

from django.db.models import Q
from django.urls import reverse
from django.utils import timezone

from .forms import CommentForm
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import CreatePostForm, UpdatePostForm
from .models import Post
from .permissions import UserHasPermissionMixin


class PostListView(ListView):
    model = Post
    template_name = 'oursite/index.html'
    context_object_name = 'posts'
    paginate_by = 4

    def get_template_names(self):
        template_name = super(PostListView, self).get_template_names()
        search = self.request.GET.get('q')
        if search:
            template_name = 'oursite/search.html'
        return template_name

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        search = self.request.GET.get('q')
        filter = self.request.GET.get('filter')
        if search:
            context['posts'] = Post.objects.filter(Q(post__icontains=search)|
                                                   Q(title__icontains=search))
        elif filter:
            start_date = timezone.now() - timedelta(days=1)
            context['posts'] = Post.objects.filter(created_date__gte=start_date)

        else:
            context['posts'] = Post.objects.all()
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'oursite/post_detail.html'
    context_object_name = 'post'
    pk_url_kwarg = 'pk'


class PostCreateView(CreateView):
    model = Post
    template_name = 'oursite/create_post.html'
    form_class = CreatePostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['post_form'] = self.get_form()
        return context


class PostUpdateView(UserHasPermissionMixin, UpdateView):
    model = Post
    template_name = 'oursite/update_post.html'
    form_class = UpdatePostForm
    pk_url_kwarg = 'post_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['post_form'] = self.get_form()
        return context


class PostDeleteView(UserHasPermissionMixin, DeleteView):
    model = Post
    template_name = 'oursite/delete_post.html'
    pk_url_kwarg = 'post_id'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        post = self.object.post
        self.object.delete()
        return redirect('/', )


def post_detail(request, slug):
    template_name = 'post_detail.html'
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.filter(active=True)
    new_comment = None
    # Comment posted
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(request, template_name, {'post': post,
                                           'comments': comments,
                                           'new_comment': new_comment,
                                           'comment_form': comment_form})




