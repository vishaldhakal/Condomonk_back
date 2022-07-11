from django.db import models
from django_summernote.fields import SummernoteTextField


class Developer(models.Model):
    image = models.FileField()
    name = models.CharField(max_length=500)
    website_link = models.TextField(blank=True)
    details = models.TextField()

    def __str__(self):
        return self.name


class Cityy(models.Model):
    name = models.CharField(max_length=500)
    centerLat = models.CharField(max_length=300)
    centerLong = models.CharField(max_length=300)
    city_details = SummernoteTextField(blank=True)

    def __str__(self):
        return self.name


class FloorPlanChoices(models.Model):
    choice = models.CharField(max_length=500, unique=True)

    def __str__(self):
        return self.choice


class PreConstruction(models.Model):

    STATUS_CHOICES = [
        ("Upcoming", "Upcoming"),
        ("Selling", "Selling"),
        ("Sold out", "Sold out")
    ]

    ASSIGNMENT_CHOICES = [
        ("Free", "Free"),
        ("Not Available", "Not Available"),
        ("Available With Fee", "Available With Fee")
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
    street_map = models.TextField()
    developer = models.ForeignKey(Developer, on_delete=models.CASCADE)
    city = models.ForeignKey(Cityy, on_delete=models.CASCADE)
    project_name = models.CharField(max_length=500)
    slug = models.CharField(max_length=1000, unique=True)
    storeys = models.CharField(max_length=10, blank=True)
    total_no_of_units = models.IntegerField(default=0, blank=True)
    price_starting_from = models.FloatField()
    price_to = models.FloatField(blank=True, null=True, default=0)
    project_type = models.CharField(
        max_length=500, choices=PROJECT_CHOICES, default="NaN")
    description = SummernoteTextField(blank=True)
    project_address = models.CharField(max_length=500)
    postalcode = models.CharField(max_length=200)
    latitute = models.CharField(max_length=10)
    longitude = models.CharField(max_length=10)
    occupancy = models.CharField(max_length=500, blank=True)
    feature_button_text = models.CharField(max_length=500)
    status = models.CharField(
        max_length=500, choices=STATUS_CHOICES, default="Upcoming")
    assignment_closure_type = models.CharField(
        max_length=500, choices=ASSIGNMENT_CHOICES, default="Free")
    video_url = models.CharField(max_length=1300, default="No Video")
    facts_about = SummernoteTextField(blank=True)
    deposit_structure = SummernoteTextField(blank=True)
    date_of_upload = models.DateField(auto_now_add=True, null=True, blank=True)
    related1 = models.ManyToManyField('self', blank=True)
    type_of_plan = models.ManyToManyField(FloorPlanChoices, blank=True)

    def __str__(self):
        return self.project_name + " [ " + self.city.name+" ] "

    def first_five_related(self):
        return self.related1.all()[:5]

    class Meta:
        ordering = ('-id',)


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
    type_of_plan = models.ForeignKey(
        FloorPlanChoices, on_delete=models.CASCADE, blank=True, null=True)
    no_of_baths = models.CharField(max_length=100, blank=True)
    plan_name = models.CharField(max_length=400, blank=True)
    area = models.CharField(max_length=100, blank=True)
    has_balcony = models.BooleanField(default=False)
    balcony_area = models.CharField(max_length=100, blank=True, null=True)
    project = models.ForeignKey(
        PreConstruction, on_delete=models.CASCADE, related_name='floorplans')

    def __str__(self):
        return self.plan_name+" "+self.type_of_plan.choice

    def no_of_iteee(self):
        return FloorPlans.objects.filter(type_of_plan=self.type_of_plan).count()
