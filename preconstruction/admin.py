from django.contrib import admin
from .models import Developer, PreConstruction, FloorPlans, PreConstructionImage, Cityy, FloorPlanChoices
from django.urls import reverse
from django.utils.http import urlencode
from django.utils.html import format_html


class PreConstructionImageAdmin(admin.StackedInline):
    model = PreConstructionImage


class FloorPlansAdmin(admin.StackedInline):
    model = FloorPlans


@admin.register(PreConstruction)
class PreConstructionAdmin(admin.ModelAdmin):
    list_display = ("project_name", "city", "project_type",
                    "upload_plans_and_images")
    list_filter = ("city", "project_type", "date_of_upload")
    search_fields = ("city__name__contains", "project_name__contains")

    def editdata(self, obj):
        return format_html('<a target="_blank" href="https://homebaba.ca/admin/data/{}">{}</a>', obj.id, " Edit data for "+obj.project_name)

    def upload_plans_and_images(self, obj):
        return format_html('<a target="_blank" href="https://homebaba.ca/admin/plan/{}">{}</a>', obj.id, " Upload Files for "+obj.project_name)

    upload_plans_and_images.short_description = "Upload Images + Plans"

    class Meta:
        model = PreConstruction


@admin.register(PreConstructionImage)
class PreConstructionImageAdmin(admin.ModelAdmin):
    pass


@admin.register(FloorPlans)
class FloorPlansAdmin(admin.ModelAdmin):
    pass


admin.site.register(Developer)
admin.site.register(Cityy)
admin.site.register(FloorPlanChoices)
