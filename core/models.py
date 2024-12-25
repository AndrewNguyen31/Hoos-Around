from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import random


import uuid

def random_filename(instance, filename):
    """
    Returns a random filename
    """
    return f"place/{uuid.uuid4()}.{filename.split('.')[-1]}"

# Create your models here.
class User(AbstractUser):
    """
    Represents a user within the system

    Can either be a base user (someone who finds locations)
    or a superuser (someone who can add locations)
    """

    ROLES = (
        ("base", "Base User"),
        ("super", "Super User"),
    )

    role = models.CharField(max_length=5, choices=ROLES, default="base")

    def has_task(self, place):
        """
        Checks if the user has a task for a given place
        """
        return self.tasks.filter(place=place).exists()

    def check_off_task(self, task_id):
        task = self.tasks.get(id=task_id)
        task.completed = True
        task.completed_at = timezone.now()
        task.save()
        
        eligible_places = Place.objects.exclude(outgoing__user = self)
        eligible_places_list = list(eligible_places)
        
        if len(eligible_places_list) > 2:
            eligible_places_list = random.sample(eligible_places_list, 2)
        for place in eligible_places_list:
            Task.objects.create(user=self, place=place)

    def is_super(self):
        """
        Checks if the user is a super user
        """
        return self.role == "super"


class Picture(models.Model):
    """
    Represents a picture within the system with:
    - A Image
    - A description
    """    
    img = models.ImageField(upload_to=random_filename, blank=False)
    description = models.TextField()

    def __str__(self):
        """Path"""
        return str(self.img)


class Place(models.Model):
    """
    Represents a location within the system
    """

    name = models.CharField(max_length=500)
    description = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()

    pictures = models.ManyToManyField(Picture, blank=True, related_name="pictures", verbose_name="Pictures")

    # address
    address1 = models.CharField("Address line 1", max_length=500)
    address2 = models.CharField("Address line 2", max_length=500, null=True, blank=True)
    zip_code = models.CharField(
        "ZIP / Postal code",
        max_length=12,
    )

    city = models.CharField(
        "City",
        max_length=1024,
    )

    country = models.CharField(
        "Country",
        max_length=3,
    )

    added = models.DateTimeField(auto_now_add=True) 
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)

    approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="approves")
    approved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.name)

    def thumbnail(self) -> str:
        """
        Returns the first picture of the place
        """
        if self.pictures.count() == 0:
            return ""
        
        return self.pictures.first().img.url

    def address(self) -> str:
        """
        Returns the address of the place
        """
        parts = [
            self.address1,
            self.address2,
            self.zip_code,
            self.city,
            self.country,
        ]

        parts = [part for part in parts if part is not None and part != ""]
        return ", ".join(parts)


class Task(models.Model):
    """
    Represents a task which links a user to a place
    """

    user = models.ForeignKey(User, related_name="tasks", on_delete=models.CASCADE)
    place = models.ForeignKey(Place, related_name="outgoing", on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    assigned_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.user) + " - " + str(self.place)
