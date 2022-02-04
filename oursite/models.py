from django.db import models
from django.urls import reverse
from django.utils import timezone

from account.models import User


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    post = models.CharField(max_length=50)
    title = models.CharField(max_length=250)
    image = models.ImageField(upload_to='post_images', null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='blog_posts')

    def total_likes(self):
        return self.likes.count()

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.post

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    class Meta:
        ordering = ('created_date',)


class Image(models.Model):
    image = models.ImageField(upload_to='posts')
    post_image = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')

    def __str__(self):
        return self.image.url


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)
