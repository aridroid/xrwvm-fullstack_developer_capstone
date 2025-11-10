from django.contrib import admin
from .models import CarDealer, CarMake, CarReview, Car  # Include Car if you have it

@admin.register(CarDealer)
class CarDealerAdmin(admin.ModelAdmin):
    list_display = ("name", "city", "state", "phone", "website")
    search_fields = ("name", "city", "state", "zip_code")
    list_filter = ("state",)

@admin.register(CarMake)
class CarMakeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(Car)   # only if you have a Car model
class CarAdmin(admin.ModelAdmin):
    list_display = ('id', 'make', 'model', 'year', 'dealer')
    list_filter = ('make', 'year')
    search_fields = ('model', 'make__name')

@admin.register(CarReview)
class CarReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'dealer_id', 'created_at')
    search_fields = ('user__username','review')
