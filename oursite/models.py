from django.db import models
from django.urls import reverse
from django.utils import timezone


class Post(models.Model):
    slug = models.SlugField(primary_key=True)
    name = models.CharField(max_length=155)
    title = models.CharField(max_length=55, unique=True)
    image = models.ImageField(upload_to='post_images', null=True, blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def get_absolute_url(self):
        return reverse('detail', kwargs={'post_id': self.pk})

    def __str__(self):
        return self.name

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    class Meta:
        ordering = ('name',)


# class Image(models.Model):
#     image = models.ImageField(upload_to='posts')
#     post_image = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')
#
#     def __str__(self):
#         return self.image.url
