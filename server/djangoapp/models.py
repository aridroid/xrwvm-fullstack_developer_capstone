from django.db import models
from django.contrib.auth.models import User

class CarDealer(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=300, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    zip_code = models.CharField(max_length=20, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    website = models.URLField(blank=True, null=True)
    lat = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    lon = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Car Dealer"
        verbose_name_plural = "Car Dealers"

    def __str__(self):
        return f"{self.name} — {self.city or 'No city'}"

class CarReview(models.Model):
    dealer_id = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.TextField()
    purchase_date = models.DateField(null=True, blank=True)
    car_make = models.CharField(max_length=128, blank=True)
    car_year = models.CharField(max_length=10, blank=True)
    sentiment = models.CharField(max_length=16, default='neutral')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.review[:30]}"

class CarMake(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
class Car(models.Model):
    make = models.ForeignKey('CarMake', on_delete=models.CASCADE)   # relation to CarMake
    model = models.CharField(max_length=100)
    year = models.IntegerField(null=True, blank=True)
    dealer = models.ForeignKey(CarDealer, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.make} {self.model} ({self.year})"
