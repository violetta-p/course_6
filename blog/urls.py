from django.urls import path
from django.views.decorators.cache import never_cache

from blog.apps import BlogConfig
from blog.views import BlogCreateView, BlogListView, BlogDetailView, BlogUpdateView, BlogDeleteView, manager_blog_list, \
    ManagerBlogUpdateView, ManagerBlogDeleteView

app_name = BlogConfig.name

urlpatterns = [
    path('create/', never_cache(BlogCreateView.as_view()), name='create'),
    path('', BlogListView.as_view(), name='list'),
    path('view/<int:pk>', BlogDetailView.as_view(), name='view'),
    path('edit/<int:pk>/', BlogUpdateView.as_view(), name='edit'),
    path('delete/<int:pk>/', BlogDeleteView.as_view(), name='delete'),
    path('manager/blog/', manager_blog_list, name='manager_blog_list'),
    path('manager/edit/<int:pk>/', ManagerBlogUpdateView.as_view(), name='manager_blog_edit'),
    path('manager/delete/<int:pk>/', ManagerBlogDeleteView.as_view(), name='manager_blog_delete'),
]