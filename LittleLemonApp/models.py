from django.db import models
from datetime import time


# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=255)


class Menu(models.Model):
    logo = models.ImageField(upload_to="logos/")
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    inventory = models.PositiveIntegerField()
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=None)


GUEST_CHOICES = [("1", "1"), ("2", "2"), ("3", "3"), ("4", "4"), ("5", "5"), ("6", "6")]


SEATING_CHOICES = [
    ("Indoor", "Indoor"),
    ("Outdoor", "Outdoor"),
    ("No Preference", "No Preference"),
]


class Booking(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    date = models.DateField()
    time = models.TimeField()
    phone_number = models.CharField(max_length=15)
    number_of_guests = models.CharField(max_length=2, choices=GUEST_CHOICES)
    seating = models.CharField(
        choices=SEATING_CHOICES, max_length=20, default="No Preference"
    )
    comment = models.TextField(blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["date", "time"], name="unique_date_time")
        ]
