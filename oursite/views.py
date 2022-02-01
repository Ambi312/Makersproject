from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import CreatePostForm, UpdatePostForm, ImageForm
from .models import *
from django.forms import modelformset_factory
from .models import Post
from .forms import CommentForm
from django.shortcuts import render, get_object_or_404


class SearchListView(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'results'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(SearchListView, self).get_context_data()
        context['search_word'] = self.request.GET.get('q')
        return context

    def get_queryset(self):
        queryset = super(SearchListView, self).get_queryset()
        search_word = self.request.GET.get('q')
        if not search_word:
            queryset = Post.objects.none()
        else:
            if len(search_word) < 3:
                queryset = Post.objects.none()
            else:
                queryset = queryset.filter(name__icontains=search_word)
        return queryset


class PostListView(ListView):
    model = Post
    template_name = 'oursite/index.html'
    context_object_name = 'posts'


class PostDetailView(DetailView):
    model = Post
    template_name = 'oursite/post_detail.html'
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'


class PostCreateView(CreateView):
    model = Post
    template_name = 'oursite/create_post.html'
    form_class = CreatePostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['post_form'] = self.get_form()
        return context


class PostUpdateView(UpdateView):
    ImageFormset = modelformset_factory(Image, form=ImageForm, max_num=5)
    model = Post
    template_name = 'oursite/update_post.html'
    form_class = UpdatePostForm
    pk_url_kwarg = 'post_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['post_form'] = self.get_form()
        return context


class PostDeleteView(DeleteView):
    model = Post
    template_name = 'delete_post.html'
    pk_url_kwarg = 'post_id'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        post = self.object.category.post
        self.object.delete()
        return redirect('list', post)


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
