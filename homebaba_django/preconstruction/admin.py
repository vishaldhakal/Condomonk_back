from django.contrib import admin
from .models import Developer, PreConstruction, FloorPlans, PreConstructionImage, Cityy


class PreConstructionImageAdmin(admin.StackedInline):
    model = PreConstructionImage


class FloorPlansAdmin(admin.StackedInline):
    model = FloorPlans


@admin.register(PreConstruction)
class PreConstructionAdmin(admin.ModelAdmin):
    inlines = [PreConstructionImageAdmin,
               FloorPlansAdmin]

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
