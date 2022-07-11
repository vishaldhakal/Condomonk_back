from django.contrib import admin
from .models import Posts, Categories, ImageUploads, UserProfile

""" from django_summernote.admin import SummernoteModelAdmin


class PostsAdmin(SummernoteModelAdmin):
    summernote_fields = ('content')

 """
admin.site.register(Posts)
admin.site.register(Categories)
admin.site.register(ImageUploads)
admin.site.register(UserProfile)
