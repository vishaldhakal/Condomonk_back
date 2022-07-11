from rest_framework import serializers
from . import models


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ("__all__")
        model = models.Categories


class AccountSerializerr(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'first_name', 'last_name', 'email')
        model = models.User


class AccountSerializer(serializers.ModelSerializer):
    user = AccountSerializerr(read_only=True)

    class Meta:
        fields = ('user', 'profile_img', 'user_post')
        model = models.UserProfile


class MyPostSerializer2(serializers.ModelSerializer):
    author = AccountSerializer(read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        fields = ('slug', 'title', 'category', 'created_at', 'updated_at',
                  'thumbnail_image', 'thumbnail_image_alt_description', 'author',)
        model = models.Posts


class PostsSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    author = AccountSerializer(read_only=True)
    related1 = MyPostSerializer2(many=True, read_only=True)

    class Meta:
        model = models.Posts
        fields = ('slug', 'meta_title', 'meta_description', 'meta_keyword',
                  'title', 'category', 'created_at', 'updated_at', 'scripts_ld', 'thumbnail_image', 'thumbnail_image_alt_description', 'author', 'content', 'related1')
