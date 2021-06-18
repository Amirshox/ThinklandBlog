from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_list', args=[self.slug])


class Article(models.Model):
    TYPE = [
        ('free', 'Free'),
        ('premium', 'Premium')
    ]
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    type = models.CharField(choices=TYPE, max_length=7, default='Free')
    content = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category')

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article_detail', args=[self.slug])


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    publish = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return f'Comment by {self.author.username} on {self.article}'
