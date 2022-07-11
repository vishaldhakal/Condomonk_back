from django.contrib import admin
from django.urls import path, include
from .views import preconstruction_collection, preconstruction_collection_city, preconstruction_single, preconstruction_search_view, preupload


urlpatterns = [
    path('pre-constructions/', preconstruction_collection),
    path('pre-constructions-city/<str:city>/', preconstruction_collection_city),
    path('pre-constructions/search/', preconstruction_search_view),
    path('pre-constructions/<str:slug>/', preconstruction_single),
    path('preupload/', preupload),
]
