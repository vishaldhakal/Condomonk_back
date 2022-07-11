from rest_framework import status
from django.core.mail import send_mail, EmailMultiAlternatives
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from django.shortcuts import render, HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import (
    PreConstructionSerializer,
    PreConstructionSingleSerializer,
    FloorPlansSerializer,
    PreConstructionImageSerializer,
    FloorPlanChoicesSerializer,
    CityySerializer,
    PreConstructionSingleDataSerializer,
    CityySerializerUpload,
    DeveloperSerializerUpload,
    PreConstructionSerializerCity
)
from .models import PreConstruction, Developer, FloorPlans, PreConstructionImage, Cityy, FloorPlanChoices
from rest_framework.pagination import PageNumberPagination
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import json
import math


@api_view(["POST"])
def ContactFormSubmission(request):
    if request.method == "POST":
        subject = "Inquiry for pre-construction homes - Homebaba"
        email = "Homebaba <admin@homebaba.ca>"
        headers = {'Reply-To': request.POST["email"]}
        contex = {
            "name": request.POST["name"],
            "email": request.POST["email"],
            "phone": request.POST["phone"],
            "message": request.POST["message"]
        }
        html_content = render_to_string("contactForm.html", contex)
        text_content = strip_tags(html_content)
        msg = EmailMultiAlternatives(
            subject, "You have been sent a Contact Form Submission. Unable to Receive !", email, ["milan@homebaba.ca"], headers=headers)
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        return HttpResponse("Sucess")
    else:
        return HttpResponse("Not post req")


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
        cityy = request.GET.get("city", "All")
        status = request.GET.get("status", "All")
        typee = request.GET.get("typee", "All")

        try:
            cityyy = Cityy.objects.get(name__contains=cityy)
            if((typee == "All") & (status == "All")):
                cats = PreConstruction.objects.filter(city=cityyy)
            elif((typee == "All") & (status != "All")):
                cats = PreConstruction.objects.filter(
                    status=status, city=cityyy)
            elif((typee != "All") & (status == "All")):
                cats = PreConstruction.objects.filter(
                    project_type=typee, city=cityyy)
            else:
                cats = PreConstruction.objects.filter(
                    status=status, project_type=typee, city=cityyy)
        except:
            if((typee == "All") & (status == "All")):
                cats = PreConstruction.objects.all()
            elif((typee == "All") & (status != "All")):
                cats = PreConstruction.objects.filter(status=status)
            elif((typee != "All") & (status == "All")):
                cats = PreConstruction.objects.filter(project_type=typee)
            else:
                cats = PreConstruction.objects.filter(
                    status=status, project_type=typee)

        paginator = CustomPagination()
        paginator.page_size = 10
        total_data = cats.count()
        no_of_pages = math.ceil(total_data/paginator.page_size)
        result_page = paginator.paginate_queryset(cats, request)
        serializer_cat = PreConstructionSerializerCity(result_page, many=True)
        final = paginator.get_paginated_response(
            serializer_cat.data, no_of_pages)
        return Response({"data": final.data})


@api_view(['GET'])
def preconstruction_collection_city(request, city):
    if request.method == 'GET':
        slug_city = city.capitalize()
        cityyy = Cityy.objects.get(name__contains=slug_city)
        paginationsize = request.GET.get("perpage", "30")

        try:
            cats = PreConstruction.objects.filter(
                city=cityyy).order_by('date_of_upload')
        except:
            cats = PreConstruction.objects.all()[0:0]

        paginator = CustomPagination()
        paginator.page_size = int(paginationsize)
        total_data = cats.count()
        no_of_pages = math.ceil(total_data/paginator.page_size)
        result_page = paginator.paginate_queryset(cats, request)
        serializer_cat = PreConstructionSerializer(result_page, many=True)
        serializer_city = CityySerializer(cityyy)
        final = paginator.get_paginated_response(
            serializer_cat.data, no_of_pages)
        return Response({"data": final.data, "citydata": serializer_city.data})


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
        try:
            pree = PreConstruction.objects.get(slug=slug)
            serializer_cat = PreConstructionSingleSerializer(pree)
            floors = FloorPlans.objects.filter(project=pree)
            try:
                floorser = []
                noarr = []
                for it in pree.type_of_plan.all():
                    choi = FloorPlanChoices.objects.get(id=it.id)
                    floo = FloorPlans.objects.filter(
                        project=pree, type_of_plan=choi)
                    noarr.append(floo.count())
                    floorser.append(FloorPlansSerializer(floo, many=True).data)
                serializer_floor = FloorPlansSerializer(floors, many=True)
                imagess = PreConstructionImage.objects.filter(preconst=pree)
                serializer_images = PreConstructionImageSerializer(
                    imagess, many=True)
                return Response({"house_detail": serializer_cat.data, "floor_plans": serializer_floor.data, "images": serializer_images.data, "noarr": noarr})
            except:
                floorser = []
                imagess = PreConstructionImage.objects.filter(preconst=pree)
                serializer_images = PreConstructionImageSerializer(
                    imagess, many=True)
                return Response({"house_detail": serializer_cat.data, "images": serializer_images.data})
        except:
            return Response({"error": "Not Found"})


@api_view(['GET'])
def preconstruction_single_data(request, id):
    if request.method == 'GET':
        try:
            pree = PreConstruction.objects.get(id=id)
            serializer_pre = PreConstructionSingleDataSerializer(pree)
            cities = Cityy.objects.all()
            serializer_city = CityySerializerUpload(cities, many=True)
            return Response({"house_detail": serializer_pre.data, "cities": serializer_city.data})
        except:
            return Response({"error": "Not Found"})


@api_view(['GET'])
def preconstruction_initial_data(request):
    if request.method == 'GET':
        try:
            developers = Developer.objects.all()
            serializer_developers = DeveloperSerializerUpload(
                developers, many=True)
            cities = Cityy.objects.all()
            serializer_city = CityySerializerUpload(cities, many=True)
            return Response({"developers": serializer_developers.data, "cities": serializer_city.data})
        except:
            return Response({"error": "Not Found"})


@api_view(['POST'])
def submit_developer(request):
    if request.method == 'POST':
        try:
            devimage = request.FILES['image']
            namee = request.POST['developer_name']
            websitee = request.POST['website_link']
            detailss = request.POST['details']
            devv = Developer.objects.create(
                name=namee, website_link=websitee, details=detailss, image=devimage)
            developers = Developer.objects.all()
            serializer_developers = DeveloperSerializerUpload(
                developers, many=True)
            return Response({"developers": serializer_developers.data})
        except:
            return Response({"error": "Error Adding Developer"})


@api_view(["POST"])
def preconstruction_data_upload(request):
    try:
        datas = JSONParser().parse(request)
        cityc = Cityy.objects.get(name=datas["city"]["name"])
        alll = PreConstruction.objects.filter(city=cityc)
        devcc = Developer.objects.get(name=datas["developer"]["name"])
        preconst = PreConstruction.objects.create(
            meta_title=datas["meta_title"],
            meta_description=datas["meta_description"],
            street_map=datas["street_map"],
            project_name=datas["project_name"],
            slug=datas["slug"],
            total_no_of_units=datas["total_no_of_units"],
            price_starting_from=datas["price_starting_from"],
            price_to=datas["price_to"],
            project_type=datas["project_type"],
            description=datas["description"],
            project_address=datas["project_address"],
            postalcode=datas["postalcode"],
            latitute=datas["latitute"],
            longitude=datas["longitude"],
            occupancy=datas["occupancy"],
            feature_button_text=datas["feature_button_text"],
            status=datas["status"],
            assignment_closure_type=datas["assignment_closure_type"],
            video_url=datas["video_url"],
            facts_about=datas["facts_about"],
            deposit_structure=datas["deposit_structure"],
            city=cityc,
            developer=devcc,
        )
        preconst.related1.add(*alll)
        return Response({"status": "Uploaded"})
    except:
        return Response({"error": "Not Uploaded"})


@api_view(["POST"])
def preconstruction_data_update(request):
    try:
        datas = JSONParser().parse(request)
        preconst = PreConstruction.objects.get(pk=datas["id"])
        preconst.project_name = datas["project_name"]
        preconst.project_type = datas["project_type"]
        preconst.project_address = datas["project_address"]
        preconst.postalcode = datas["postalcode"]
        preconst.latitute = datas["latitute"]
        preconst.longitude = datas["longitude"]
        preconst.price_starting_from = datas["price_starting_from"]
        preconst.price_to = datas["price_to"]
        preconst.occupancy = datas["occupancy"]
        preconst.status = datas["status"]
        preconst.assignment_closure_type = datas["assignment_closure_type"]
        preconst.video_url = datas["video_url"]
        preconst.feature_button_text = datas["feature_button_text"]
        preconst.slug = datas["slug"]
        preconst.status = datas["status"]
        preconst.total_no_of_units = datas["total_no_of_units"]
        preconst.street_map = datas["street_map"]
        preconst.description = datas["description"]
        preconst.deposit_structure = datas["deposit_structure"]
        preconst.facts_about = datas["facts_about"]
        preconst.meta_title = datas["meta_title"]
        preconst.meta_description = datas["meta_description"]
        cityyy = Cityy.objects.get(name=datas["city"]["name"])
        preconst.city = cityyy
        preconst.save()
        pree = PreConstruction.objects.get(id=id)
        serializer_pre = PreConstructionSingleDataSerializer(pree)
        cities = Cityy.objects.all()
        serializer_city = CityySerializerUpload(cities, many=True)
        return Response({"house_detail": serializer_pre.data, "cities": serializer_city.data})
    except:
        return Response({"error": "Not Found"})


@api_view(['GET'])
def preconstruction_single_images(request, id):
    if request.method == 'GET':
        pree = PreConstruction.objects.get(id=id)
        serializer_cat = PreConstructionSingleSerializer(pree)
        floors = FloorPlans.objects.filter(project=pree)
        try:
            imagess = PreConstructionImage.objects.filter(preconst=pree)
            serializer_images = PreConstructionImageSerializer(
                imagess, many=True)
            return Response({"images": serializer_images.data, "preid": pree.id, "preconstinfo": {"name": pree.project_name, "city": pree.city.name}})
        except:
            floorser = []
            imagess = PreConstructionImage.objects.filter(preconst=pree)
            serializer_images = PreConstructionImageSerializer(
                imagess, many=True)
            return Response({"house_detail": serializer_cat.data, "images": serializer_images.data})


@api_view(["POST"])
def UpdatealtTag(request):
    try:
        datas = JSONParser().parse(request)
        preconstruct = PreConstruction.objects.get(pk=datas[0]["preconst"])
        for data in datas:
            preimg = PreConstructionImage.objects.get(
                pk=data["id"], preconst=preconstruct)
            preimg.imagealt = data["imagealt"]
            preimg.save()

        return JsonResponse(
            {"success": "Update Successfull"},
            status=status.HTTP_201_CREATED,
        )
    except:
        return JsonResponse(
            {"error": "Update Failed"}, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(["DELETE"])
def DeleteImage(request):
    try:
        data = JSONParser().parse(request)
        preconstruct = PreConstruction.objects.get(pk=data["preconst"])
        preimg = PreConstructionImage.objects.get(
            pk=data["id"], preconst=preconstruct)
        preimg.delete()
        return JsonResponse(
            {"success": "Update Successfull"},
            status=status.HTTP_201_CREATED,
        )
    except:
        return JsonResponse(
            {"error": "Update Failed"}, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(["POST"])
def Frontimageupload(request, id):
    try:
        files = request.FILES.getlist('images')
        prec = PreConstruction.objects.get(id=id)
        for file in files:
            img = PreConstructionImage.objects.create(
                images=file, preconst=prec)
        return JsonResponse(
            {"success": "Upload Successfull"},
            status=status.HTTP_201_CREATED,
        )
    except:
        return JsonResponse(
            {"error": "Upload Failed"}, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['GET'])
def preconstruction_single_plans(request, id):
    if request.method == 'GET':
        pree = PreConstruction.objects.get(id=id)
        floors = FloorPlans.objects.filter(project=pree)
        choicess = FloorPlanChoices.objects.all()
        choiceser = FloorPlanChoicesSerializer(choicess, many=True)
        try:
            floorser = []
            noarr = []
            for it in pree.type_of_plan.all():
                choi = FloorPlanChoices.objects.get(id=it.id)
                floo = FloorPlans.objects.filter(
                    project=pree, type_of_plan=choi)
                noarr.append(floo.count())
                floorser.append(FloorPlansSerializer(floo, many=True).data)
            choicse = pree.type_of_plan.all()
            serializer_choi = FloorPlanChoicesSerializer(choicse, many=True)
            serializer_floor = FloorPlansSerializer(floors, many=True)

            return Response({"plans": serializer_floor.data, "preid": pree.id, "choices": choiceser.data, "choosed": serializer_choi.data, "noarr": noarr})
        except:
            return Response({"plans": [], "preid": pree.id, "choices": choiceser.data})


@api_view(["POST"])
def UpdatePlanData(request):
    try:
        datas = JSONParser().parse(request)
        flop = FloorPlans.objects.get(id=datas[0]["id"])
        preconstruct = flop.project

        for data in datas:
            preimg = FloorPlans.objects.get(
                pk=data["id"], project=preconstruct)

            if preimg.no_of_iteee() == 1:
                preimg.project.type_of_plan.remove(preimg.type_of_plan)

            plan_nn = FloorPlanChoices.objects.get(
                id=data["type_of_plan"]["id"])
            preimg.type_of_plan = plan_nn
            preimg.no_of_baths = data["no_of_baths"]
            preimg.plan_name = data["plan_name"]
            preimg.starting_price_of_plan = data["starting_price_of_plan"]
            preimg.area = data["area"]
            preimg.has_balcony = data["has_balcony"]
            preimg.balcony_area = data["balcony_area"]
            preimg.save()

            if preimg.no_of_iteee() == 1:
                preimg.project.type_of_plan.add(preimg.type_of_plan)

        return JsonResponse(
            {"success": "Update Successfull"},
            status=status.HTTP_201_CREATED,
        )
    except:
        return JsonResponse(
            {"error": "Update Failed"}, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(["DELETE"])
def DeletePlans(request):
    try:
        data = JSONParser().parse(request)
        flop = FloorPlans.objects.get(id=data["id"])
        if flop.no_of_iteee() == 1:
            flop.project.type_of_plan.remove(flop.type_of_plan)
        flop.delete()

        return JsonResponse(
            {"success": "Update Successfull"},
            status=status.HTTP_201_CREATED,
        )
    except:
        return JsonResponse(
            {"error": "Update Failed"}, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(["POST"])
def Frontplanupload(request, id):
    try:
        files = request.FILES.getlist('images')
        typp = request.POST["typee"]
        startingpri = request.POST["starting"]
        choi = FloorPlanChoices.objects.get(choice=typp)
        prec = PreConstruction.objects.get(id=id)
        check = 0
        for it in prec.type_of_plan.all():
            if it == choi:
                check = 1
        if check == 0:
            prec.type_of_plan.add(choi)

        for file in files:
            img = FloorPlans.objects.create(
                image=file, project=prec, type_of_plan=choi, starting_price_of_plan=startingpri)
        return JsonResponse(
            {"success": "Upload Successfull"},
            status=status.HTTP_201_CREATED,
        )
    except:
        return JsonResponse(
            {"error": "Upload Failed"}, status=status.HTTP_400_BAD_REQUEST
        )
