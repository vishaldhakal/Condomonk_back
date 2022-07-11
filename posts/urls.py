from django.contrib import admin
from django.urls import path, include
from .views import post_collection, post_element, post_element_content, category_element, categories_collection, post_element_slug, post_collection2, categoryposts, send_emails


urlpatterns = [
    path('categories/', categories_collection),
    path('categories/<int:pk>', category_element),
    path('cat-post/<str:name>', categoryposts),
    path('posts/', post_collection),
    path('posts2/', post_collection2),
    path('posts/<int:pk>', post_element),
    path('posts/<str:slugg>', post_element_slug),
    path('send-mail/', send_emails),
    path('posts/content/<str:slugg>', post_element_content),
]
