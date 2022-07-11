from django.db import models
from django_summernote.fields import SummernoteTextField


class Developer(models.Model):
    image = models.FileField()
    image_alt_text = models.CharField(max_length=300, blank=True)
    name = models.CharField(max_length=500)
    details = models.TextField()

    def __str__(self):
        return self.name


class Cityy(models.Model):
    meta_title = models.CharField(max_length=400, blank=True)
    meta_description = models.TextField(blank=True)
    meta_keywords = models.TextField(blank=True)
    name = models.CharField(max_length=500)
    centerLat = models.CharField(max_length=300)
    centerLong = models.CharField(max_length=300)
    city_details = SummernoteTextField(blank=True)

    def __str__(self):
        return self.name


class PreConstruction(models.Model):

    STATUS_CHOICES = [
        ("Upcoming", "Upcoming"),
        ("Selling", "Selling"),
        ("Sold out", "Sold out")
    ]

    ASSIGNMENT_CHOICES = [
        ("Free", "Free"),
        ("Not Available", "Not Available")
    ]
    PROJECT_CHOICES = [
        ("Condo", "Condo"),
        ("Townhome", "Townhome"),
        ("Semi-Detached", "Semi-Detached"),
        ("Detached", "Detached"),
        ("NaN", "NaN"),
    ]

    meta_title = models.CharField(max_length=400)
    meta_description = models.TextField()
    meta_keywords = models.TextField()
    slug = models.CharField(max_length=300)
    street_map = models.TextField()
    zipcode = models.CharField(max_length=200)
    developer = models.ForeignKey(Developer, on_delete=models.CASCADE)
    project_name = models.CharField(max_length=500)
    project_address = models.CharField(max_length=500)
    project_price_from = models.FloatField()
    project_price_to = models.FloatField(blank=True, null=True)
    project_type = models.CharField(
        max_length=500, choices=PROJECT_CHOICES, default="NaN")
    ready_date = models.CharField(max_length=500, blank=True)
    bedsrange = models.CharField(max_length=500, blank=True)
    bathsrange = models.CharField(max_length=500, blank=True)
    neighbourhood = models.CharField(max_length=100)
    construction_start_date = models.CharField(max_length=500, blank=True)
    main_feature = models.CharField(max_length=500)
    parking = models.CharField(max_length=700, blank=True)
    storeys = models.CharField(max_length=10)
    latitute = models.CharField(max_length=10)
    longitude = models.CharField(max_length=10)
    city = models.ForeignKey(Cityy, on_delete=models.CASCADE)
    description = SummernoteTextField()
    video_url = models.CharField(max_length=600, default="No Video")
    total_no_of_units = models.IntegerField()
    has_amenities = models.BooleanField(default=False)
    amenities_list = models.TextField(blank=True)
    status = models.CharField(
        max_length=500, choices=STATUS_CHOICES, default="Upcoming")
    assignment_closure_type = models.CharField(
        max_length=500, choices=ASSIGNMENT_CHOICES, default="Free")
    development_charges = models.TextField()
    deposit_structure = models.TextField()
    json_ld = models.TextField()
    date_of_upload = models.DateField(auto_now_add=True, null=True, blank=True)
    related1 = models.ManyToManyField('self', blank=True)
    floor_plan_types = models.CharField(max_length=700, blank=True)
    no_in_type = models.CharField(max_length=700, blank=True)
    has_floor_plans = models.BooleanField(default=False)

    def __str__(self):
        return self.project_name


class PreConstructionImage(models.Model):
    preconst = models.ForeignKey(
        PreConstruction, on_delete=models.CASCADE, related_name='images')
    images = models.FileField()
    imagealt = models.CharField(max_length=500, default="image alt tag")

    def __str__(self):
        return self.images.url+","+self.imagealt


class FloorPlans(models.Model):
    image = models.FileField()
    starting_price_of_plan = models.CharField(
        max_length=400, blank=True, null=True)
    no_of_beds = models.CharField(max_length=100)
    no_of_baths = models.CharField(max_length=100, blank=True)
    plan_name = models.CharField(max_length=400)
    area = models.CharField(max_length=100, blank=True)
    has_balcony = models.BooleanField(default=False)
    balcony_area = models.CharField(max_length=100, blank=True, null=True)
    project = models.ForeignKey(
        PreConstruction, on_delete=models.CASCADE, related_name='floorplans')

    def __str__(self):
        return self.plan_name

    def no_of_iteee(self):
        return FloorPlans.objects.filter(no_of_beds=self.no_of_beds).count()
