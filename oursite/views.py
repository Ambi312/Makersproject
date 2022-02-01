from django.http import request
from django.shortcuts import redirect, render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import CreatePostForm, UpdatePostForm, ImageForm
from .models import *
from django.forms import modelformset_factory


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
    template_name = 'oursite/detail.html'
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'


class PostCreateView(CreateView):
    def add_post(request):
        ImageFormSet = modelformset_factory(Image, form=ImageForm, max_num=5)
        if request.method == 'POST':
            post_form = CreatePostForm(request.POST)
            formset = ImageFormSet(request.POST, request.FILES, queryset=Image.objects.none())
            if post_form.is_valid() and formset.is_valid():
                post = post_form.save()

                for form in formset.cleaned_data:
                    image = form['image']
                    Image.objects.create(image=image, post=post)
                return redirect(post.get_absolute_url())
        else:
            post_form = CreatePostForm()
            formset = ImageFormSet(queryset=Image.objects.none())
        return render(request, 'create_post.html', locals())

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
        slug = self.object.category.slug
        self.object.delete()
        return redirect('list', slug)



