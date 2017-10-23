from django.contrib import admin
from .models import Restaurant, Dishes, UserProfile, ContactRecord, Order_records

admin.site.register(Restaurant)
admin.site.register(Dishes)
admin.site.register(UserProfile)
admin.site.register(ContactRecord)
admin.site.register(Order_records)

# Register your models here.
