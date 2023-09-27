from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView

from blog.forms import BlogForm
from blog.models import Blog


def get_current_user(request):
    return request.user


class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Blog
    form_class = BlogForm
    success_url = reverse_lazy('blog:list')

    def form_valid(self, form):
        self.object = form.save()
        self.object.creator = self.request.user
        self.object.save()
        return super().form_valid(form)


class BlogUpdateView(LoginRequiredMixin, UpdateView):
    model = Blog
    form_class = BlogForm

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.creator == self.request.user:
            return self.object
        elif self.request.user.is_staff:
            return self.object
        else:
            raise Http404

    def form_valid(self, form):
        self.object = form.save()
        #self.object.creator = self.request.user
        self.object.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:view', args=[self.kwargs.get('pk')])


class BlogListView(ListView):
    model = Blog

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True)
        return queryset


class BlogDetailView(DetailView):
    model = Blog

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if not self.request.user.is_staff:
            self.object.views_count += 1
            self.object.save()
        return self.object


class BlogDeleteView(LoginRequiredMixin, DeleteView):
    model = Blog
    success_url = reverse_lazy('blog:list')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.creator == self.request.user:
            return self.object
        elif self.request.user.is_staff:
            return self.object
        else:
            raise Http404


def manager_blog_list(request):
    content = {
        'blog_list': Blog.objects.all(),
    }
    return render(request, 'blog/manager_blog_list.html', content)


class ManagerBlogUpdateView(LoginRequiredMixin, UpdateView):
    model = Blog
    form_class = BlogForm
    template = 'manager_blog_form'
    success_url = reverse_lazy('blog:manager_blog_list')

    def form_valid(self, form):
        self.object = form.save()
        self.object.save()
        return super().form_valid(form)


class ManagerBlogDeleteView(LoginRequiredMixin, DeleteView):
    model = Blog
    success_url = reverse_lazy('blog:manager_blog_list')
