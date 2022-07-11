from rest_framework import serializers
from . import models


class FloorPlansSerializer(serializers.ModelSerializer):

    plansss = serializers.SerializerMethodField()

    def get_plansss(self, obj):
        return obj.no_of_iteee()

    class Meta:
        fields = ("__all__")
        model = models.FloorPlans


class PreConstructionImageSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ("__all__")
        model = models.PreConstructionImage


class PreConstructionSerializer(serializers.ModelSerializer):
    images = serializers.StringRelatedField(many=True)

    class Meta:
        fields = ('__all__')
        model = models.PreConstruction
        depth = 1


class PreConstructionSingleSerializer2(serializers.ModelSerializer):

    class Meta:
        fields = ('floor_plan_types', 'no_in_type')
        model = models.PreConstruction


class PreConstructionSingleSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ("__all__")
        model = models.PreConstruction
        depth = 1
