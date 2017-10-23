from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
# Create your models here.

class Restaurant(models.Model):
    name = models.CharField(max_length=250)
    address = models.CharField(max_length=250)
    cruisine = models.CharField(max_length=30)
    restaurant_logo = models.ImageField(blank=True, upload_to="restaurant_logo")
    def __str__(self):
        return self.name
    
    #The following two lines of code redirect you to its detail view page once it is created.
    def get_absolute_url(self):
        return reverse('home:redetail', kwargs={'pk': self.pk})
    
class Dishes(models.Model):
    name = models.CharField(max_length=30)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    price = models.CharField(max_length=30)
    food_type = models.CharField(max_length=30)
    main_picture = models.ImageField(blank=True, upload_to="dishes_picture")
    
    def __str__(self):
        return self.name
        
        
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    user_icon = models.FileField(blank=True, default='WhatEater_Small.jpeg', upload_to="user_icon")
    user_footprint = models.IntegerField(default=0)
    def __str__(self):
        return self.user.username

def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = UserProfile.objects.create(user=kwargs['instance'])

post_save.connect(create_profile, sender=User)


class ContactRecord(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField(max_length=254)
    phone = models.CharField(max_length=30)
    message = models.CharField(max_length=300)
    def __str__(self):
        return self.name
        
class Order_records(models.Model):
    order_restaurant = models.ForeignKey(Restaurant)
    order_user = models.ForeignKey(User, on_delete=models.CASCADE)
    wanted_dish = models.ForeignKey(Dishes)
    quantity = models.SmallIntegerField(default=1)
    def __str__(self):
        return self.order_restaurant.name