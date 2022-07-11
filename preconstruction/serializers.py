from rest_framework import serializers
from . import models


class FloorPlansSerializer(serializers.ModelSerializer):
    plansss = serializers.SerializerMethodField()

    def get_plansss(self, obj):
        return obj.no_of_iteee()

    class Meta:
        exclude = ('project', )
        model = models.FloorPlans
        depth = 1


class CitySmallSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id', 'name']
        model = models.Cityy


class DeveloperSmallSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id', 'name', 'image']
        model = models.Developer


class PreConstructionImageSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ("__all__")
        model = models.PreConstructionImage


class PreConstructionSerializer(serializers.ModelSerializer):
    images = serializers.StringRelatedField(many=True)
    city = CitySmallSerializer()
    developer = DeveloperSmallSerializer()

    class Meta:
        fields = ['id', 'images', 'slug', 'postalcode', 'project_name', 'project_address', 'price_starting_from', 'price_to', 'project_type',
                  'occupancy', 'feature_button_text', 'storeys', 'latitute', 'longitude', 'status', 'assignment_closure_type', 'city', 'developer']
        model = models.PreConstruction
        depth = 1


class PreConstructionSerializerCity(serializers.ModelSerializer):
    city = CitySmallSerializer()

    class Meta:
        fields = ['id', 'slug', 'project_name',
                  'project_type', 'city', 'status']
        model = models.PreConstruction
        depth = 1


class PreConstructionSingleSerializer(serializers.ModelSerializer):
    related1 = PreConstructionSerializer(
        read_only=True, many=True, source='first_five_related')
    city = CitySmallSerializer()
    developer = DeveloperSmallSerializer()

    class Meta:
        fields = ("__all__")
        model = models.PreConstruction
        depth = 1


class PreConstructionSingleDataSerializer(serializers.ModelSerializer):
    city = CitySmallSerializer()
    developer = DeveloperSmallSerializer()

    class Meta:
        fields = ("__all__")
        model = models.PreConstruction
        depth = 1


class FloorPlanChoicesSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ("__all__")
        model = models.FloorPlanChoices


class CityySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ("__all__")
        model = models.Cityy


class CityySerializerUpload(serializers.ModelSerializer):

    class Meta:
        fields = ['id', 'name']
        model = models.Cityy


class DeveloperSerializerUpload(serializers.ModelSerializer):

    class Meta:
        fields = ['id', 'name']
        model = models.Cityy
