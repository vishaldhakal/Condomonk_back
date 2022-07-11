from django.shortcuts import render, HttpResponse, redirect
from django.core.mail import send_mail, EmailMultiAlternatives
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .serializers import PostsSerializer, CategorySerializer
from .models import Posts, Categories
from django.http import HttpResponse
import json
from django.template.loader import render_to_string
from django.utils.html import strip_tags


@api_view(['GET'])
def categories_collection(request):
    if request.method == 'GET':
        cats = Categories.objects.all()
        serializer_cat = CategorySerializer(cats, many=True)
        return Response(serializer_cat.data)


@api_view(['GET'])
def category_element(request, pk):
    try:
        cats = Categories.objects.get(pk=pk)
    except Posts.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer_cat = CategorySerializer(cats)
        return Response(serializer_cat.data)


@api_view(['GET'])
def post_collection(request):
    paginator = PageNumberPagination()
    paginator.page_size = 100
    person_objects = Posts.objects.all().order_by('created_at')
    result_page = paginator.paginate_queryset(person_objects, request)
    serializer = PostsSerializer(result_page, many=True)
    cats = Categories.objects.all()
    serializer_cat = CategorySerializer(cats, many=True)
    haha = paginator.get_paginated_response(serializer.data)
    return Response({"categories": serializer_cat.data, "data": haha.data})


@api_view(['GET'])
def post_collection2(request):
    if request.method == 'GET':
        posts = Posts.objects.filter()[:2]
        serializer = PostsSerializer(posts, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def post_element(request, pk):
    try:
        post = Posts.objects.get(pk=pk)
    except Posts.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = PostsSerializer(post)
        return Response(serializer.data)


@api_view(['GET'])
def post_element_slug(request, slugg):
    try:
        post = Posts.objects.get(slug=slugg)
    except Posts.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = PostsSerializer(post)
        return Response(serializer.data)


@api_view(['GET'])
def categoryposts(request, name):
    try:
        mycat = Categories.objects.get(name=name)
        post = Posts.objects.filter(category=mycat)
    except Posts.DoesNotExist:
        return HttpResponse(status=404)
    serializer = PostsSerializer(post, many=True)
    cats = Categories.objects.all()
    serializer_cat = CategorySerializer(cats, many=True)
    return Response({"categories": serializer_cat.data, "data": serializer.data})


@api_view(['GET'])
def post_element_content(request, slugg):
    try:
        post = Posts.objects.get(slug=slugg)
    except Posts.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        return HttpResponse(json.dumps(post.content))


@csrf_exempt
def send_emails(request):
    if request.method == "POST":
        subject = json.loads(request.body.decode('utf-8'))["name"]
        name = "Milan Pandey"
        email = "Homebaba <admin@homebaba.ca>"
        contex = {
            "imgdata": json.loads(request.body.decode('utf-8'))["img_url1"],
            "name": json.loads(request.body.decode('utf-8'))["name"],
            "cityname": json.loads(request.body.decode('utf-8'))["cityname"],
            "address": json.loads(request.body.decode('utf-8'))["address"],
            "developer": json.loads(request.body.decode('utf-8'))["developer"],
            "slug": json.loads(request.body.decode('utf-8'))["slug"],
            "deposite": json.loads(request.body.decode('utf-8'))["deposite"],
            "movein": json.loads(request.body.decode('utf-8'))["movein"],
            "act": json.loads(request.body.decode('utf-8'))["act"],
            "from": json.loads(request.body.decode('utf-8'))["from"],
            "to": json.loads(request.body.decode('utf-8'))["to"]
        }
        html_content = render_to_string("email.html", contex)
        text_content = strip_tags(html_content)
        msg = EmailMultiAlternatives(subject, "You have been sent a Pre Construction From homebaba from Unable to Receive !", email, [
                                     json.loads(request.body.decode('utf-8'))
                                     ["email"]])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        return HttpResponse("Sucess")
    else:
        return HttpResponse("Not post req")
