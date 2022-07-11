from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.contrib.auth.models import User
from django_summernote.fields import SummernoteTextField


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile_img = models.FileField()
    user_post = models.CharField(max_length=300)


class Categories(models.Model):
    name = models.CharField(max_length=200, primary_key=True)
    cat_img = models.FileField(blank=True)

    def __str__(self):
        return self.name


class ImageUploads(models.Model):
    imagee = models.FileField()

    def __str__(self):
        return self.imagee.url


class Posts(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.CharField(max_length=300)
    meta_description = models.TextField()
    meta_title = models.CharField(max_length=200)
    title = models.CharField(max_length=500)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    thumbnail_image = models.FileField()
    thumbnail_image_alt_description = models.CharField(max_length=300)
    content = SummernoteTextField()
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    related1 = models.ManyToManyField('self', blank=True)

    def __str__(self):
        return self.title
