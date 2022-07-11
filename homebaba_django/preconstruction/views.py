import json
import math
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import PreConstructionSerializer, PreConstructionSingleSerializer, FloorPlansSerializer, PreConstructionImageSerializer, PreConstructionSingleSerializer2
from .models import PreConstruction, Developer, FloorPlans, PreConstructionImage, Cityy
from rest_framework.pagination import PageNumberPagination


def preupload(request):
    return render(request, 'preupload.html')


class CustomPagination(PageNumberPagination):
    def get_paginated_response(self, data, noo):
        return Response({
            'totalCount': self.page.paginator.count,
            'totalPages': noo,
            'dataPerpage': self.page_size,
            'results': data
        })


@api_view(['GET'])
def preconstruction_collection(request):
    if request.method == 'GET':
        paginator = CustomPagination()
        paginator.page_size = 30
        cats = PreConstruction.objects.all().order_by('date_of_upload')
        total_data = cats.count()
        no_of_pages = math.ceil(total_data/paginator.page_size)
        result_page = paginator.paginate_queryset(cats, request)
        serializer_cat = PreConstructionSerializer(result_page, many=True)
        final = paginator.get_paginated_response(
            serializer_cat.data, no_of_pages)
        return Response(final.data)


@api_view(['GET'])
def preconstruction_collection_city(request, city):
    if request.method == 'GET':
        slug_city = city.capitalize()
        try:
            cityyy = Cityy.objects.get(name=slug_city)
            cats = PreConstruction.objects.filter(
                city=cityyy).order_by('date_of_upload')
        except:
            cats = PreConstruction.objects.all()[0:0]
        paginator = CustomPagination()
        paginator.page_size = 30
        total_data = cats.count()
        no_of_pages = math.ceil(total_data/paginator.page_size)
        result_page = paginator.paginate_queryset(cats, request)
        serializer_cat = PreConstructionSerializer(result_page, many=True)
        final = paginator.get_paginated_response(
            serializer_cat.data, no_of_pages)
        return Response(final.data)


@api_view(['GET'])
def preconstruction_search_view(request):
    if request.method == 'GET':
        cityy = request.GET.get('city', 'Toronto')
        pricemin = request.GET.get('pricemin', '700000')
        pricemax = request.GET.get('pricemax', '800000')
        occupancy = request.GET.get('occupancy', '2024')
        assignment_type = request.GET.get('assigntype', 'Free')
        paginator = PageNumberPagination()
        paginator.page_size = 30
        citt = Cityy.objects.get(name=cityy)
        cats = PreConstruction.objects.filter(
            city=citt, assignment_closure_type=assignment_type, ready_date=occupancy)
        paginator = PageNumberPagination()
        total_data = cats.count()
        no_of_pages = math.ceil(total_data/paginator.page_size)
        result_page = paginator.paginate_queryset(cats, request)
        serializer_cat = PreConstructionSerializer(result_page, many=True)
        final = paginator.get_paginated_response(serializer_cat.data)
        return Response({"api_data": final.data, "no_of_pages": no_of_pages, "records_per_page": paginator.page_size})


@api_view(['GET'])
def preconstruction_single(request, slug):
    if request.method == 'GET':
        pree = PreConstruction.objects.get(slug=slug)
        serializer_cat = PreConstructionSingleSerializer(pree)
        floors = FloorPlans.objects.filter(project=pree)
        try:
            floorser = []
            x = pree.floor_plan_types.split(",")
            for it in x:
                floo = FloorPlans.objects.filter(project=pree, no_of_beds=it)
                floorser.append(FloorPlansSerializer(floo, many=True).data)
            serializer_plan = PreConstructionSingleSerializer2(pree)
            serializer_floor = FloorPlansSerializer(floors, many=True)
            imagess = PreConstructionImage.objects.filter(preconst=pree)
            serializer_images = PreConstructionImageSerializer(
                imagess, many=True)
            return Response({"house_detail": serializer_cat.data, "floor_plans": floorser, "images": serializer_images.data, "plan_details": serializer_plan.data})
        except:
            floorser = []
            imagess = PreConstructionImage.objects.filter(preconst=pree)
            serializer_images = PreConstructionImageSerializer(
                imagess, many=True)
            return Response({"house_detail": serializer_cat.data, "images": serializer_images.data})
