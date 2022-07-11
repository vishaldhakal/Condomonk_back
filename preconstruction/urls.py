from django.contrib import admin
from django.urls import path, include
from .views import preconstruction_collection, preconstruction_collection_city, preconstruction_single, preconstruction_search_view, preconstruction_single_images, UpdatealtTag, DeleteImage, Frontimageupload, preconstruction_single_plans, UpdatePlanData, DeletePlans, Frontplanupload, ContactFormSubmission, preconstruction_single_data, preconstruction_data_update, preconstruction_initial_data, submit_developer, preconstruction_data_upload


urlpatterns = [
    path('pre-constructions/', preconstruction_collection),
    path('pre-constructions-city/<str:city>/', preconstruction_collection_city),
    path('pre-constructions/search/', preconstruction_search_view),
    path('pre-constructions/<str:slug>/', preconstruction_single),
    path('pre-constructions/getdata/<int:id>/', preconstruction_single_data),
    path('pre-constructions/getcity/devs/', preconstruction_initial_data),
    path('pre-constructions-new/submit/developer/', submit_developer),
    path('pre-constructions/data/update/', preconstruction_data_update),
    path('pre-constructions/data/upload/', preconstruction_data_upload),
    path('pre-constructions/images/<int:id>/', preconstruction_single_images),
    path('pre-constructions/plans/<int:id>/', preconstruction_single_plans),
    path('pre-constructions/imagesalt/update/', UpdatealtTag),
    path('pre-constructions/plans/update/', UpdatePlanData),
    path('pre-constructions/image/delete/', DeleteImage),
    path('pre-constructions/plans/delete/', DeletePlans),
    path('pre-constructions/upload/images/<int:id>/', Frontimageupload),
    path('pre-constructions/upload/plans/<int:id>/', Frontplanupload),
    path('contact-form-submit/', ContactFormSubmission),
]
