from django.db import models
import readtime
import uuid
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.utils.text import slugify


# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=100,null=True, blank=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Categories'

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.name)


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.ForeignKey(
        to=Category, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=1000, unique=True)
    content = RichTextField()
    post_thumbnail = models.ImageField(
        upload_to='post-thumbnails/', default='default_thumbnail.jpg')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_on']

    def get_readtime(self):
        result = readtime.of_text(self.content)
        return result

    def __str__(self):
        return self.title


class Comment(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE)
    content = models.TextField()
    parent = models.ForeignKey(to='self', on_delete=models.CASCADE, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s-%s' % (self.user, self.post)
