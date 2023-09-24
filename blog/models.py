from django.db import models
from django.urls import reverse

from config import settings

NULLABLE = {'blank': True, 'null': True}


class Blog(models.Model):
    """Запись в блоге"""
    title = models.CharField(max_length=100, verbose_name='Title')
    body = models.TextField(verbose_name='Body')
    preview_pic = models.ImageField(upload_to='blog_pictures/', **NULLABLE, verbose_name='Picture')
    creation_date = models.DateField(auto_now_add=True, verbose_name='Creation date')
    is_published = models.BooleanField(default=True, verbose_name='Is published')
    views_count = models.PositiveIntegerField(default=0, verbose_name='Views')
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE, verbose_name='Author')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'
