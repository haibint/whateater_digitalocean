from django.conf.urls import url, include
from . import views
from django.views.generic import ListView, DetailView
from home.models import Restaurant

urlpatterns = [
    url(r'^$', views.index, name='index'),
#    url(r'^(?p<restaurant_id>[0-9]+)/$', views.redetail, name='redetail')   python said this is not a valid regular expression, Uppercase P!!!
    url(r'^(?P<pk>\d+)$', views.restaurant_detail, name='redetail'),
    # url(r'^search_result/$', views.search_result, name='search_result'),    You Don't need this  url routing neigher
    #the url for adding a new restaurant record.
    url(r'home/add/$', views.RestaurantCreate.as_view(), name='restaurant-add'),
    url(r'^register/$', views.UserFormView.as_view(), name='register'),
    url(r'^login/$', views.login_user, name='login'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^update_profile$', views.update_profile, name='update_profile'),
    url(r'^(?P<pk>\d+)/food_order$', views.food_order, name='food_order'),
    url(r'^(?P<pk>\d+)/shop_view', views.shop_view, name='shop_view'),
]
