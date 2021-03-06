from datetime import timedelta

from django.contrib import messages
from django.db.models import Q
from django.urls import reverse
from django.utils import timezone
from django.forms import modelformset_factory
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import HttpResponseRedirect

from .forms import CommentForm, ImageForm, PostForm
from .models import Post, Comment, Image
from .forms import UpdatePostForm
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        image = self.get_object().image
        likes = get_object_or_404(Post, id=self.kwargs['pk'])
        total_likes = likes.total_likes()
        context['images'] = self.get_object().images.all()
        context['total_likes'] = total_likes
        return context


class CommentCreateView(CreateView):
    redirect_field_name = 'oursite/post_detail.html'
    model = Comment
    template_name = 'oursite/add_comment.html'
    form_class = CommentForm

    def form_valid(self, form):
        form.instance.post_id = self.kwargs['pk']
        form.instance.author = self.request.user
        return super().form_valid(form)

    
class PostUpdateView(UserHasPermissionMixin, UpdateView):
    model = Post
    template_name = 'oursite/update_post.html'
    form_class = UpdatePostForm
    pk_url_kwarg = 'post_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['post_form'] = self.get_form()
        return context

    # def get_queryset(self, *args, **kwargs):
    #     return super().get_queryset(*args, **kwargs).filter(
    #         author__username=self.kwargs['user']
    #     )

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


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


def post_create(request):

    ImageFormSet = modelformset_factory(Image,
                                        form=ImageForm, extra=4)
    if request.method == 'POST':
        postForm = PostForm(request.POST)
        formset = ImageFormSet(request.POST, request.FILES,
                               queryset=Image.objects.none())
        if postForm.is_valid() and formset.is_valid():
            post_form = postForm.save(commit=False)
            post_form.user = request.user
            post_form.save()
            for form in formset.cleaned_data:
                image = form['image']
                photo = Image(post_image=post_form, image=image,)
                photo.save()
            messages.success(request,
                             "Posted!")
            return HttpResponseRedirect("/")
        else:
            print(postForm.errors, formset.errors)
    else:
        postForm = PostForm()
        formset = ImageFormSet(queryset=Image.objects.none())
    return render(request, 'oursite/create_post.html',
                  {'postForm': postForm, 'formset': formset})


def LikeView(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    post.likes.add(request.user)
    return HttpResponseRedirect(reverse('post_detail', args=[str(pk)]))
