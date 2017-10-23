from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from .models import Restaurant, Dishes, UserProfile, ContactRecord, Order_records
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View, DetailView
from .forms import UserForm, UserSignInForm
from django.contrib.auth.models import User
import random 


# Create your views here.
def index(request):
    if request.method == "POST":
        queryset_list = Restaurant.objects.all()
        query = request.POST.get("q")
        if query:
            queryset_list = queryset_list.filter(name__icontains=query)
            context = {"search_result":queryset_list}
            template = loader.get_template('home/search_result.html')
            return HttpResponse(template.render(context, request))
        elif not query:
            draw_food_type = request.POST.get("draw_food_type")
            if draw_food_type:
                queryset_list = Restaurant.objects.all()
                drawn_list = []
                drawn_list.append(queryset_list[random.randrange(0,4)])
                drawn_list.append(queryset_list[random.randrange(0,4)])
                drawn_list.append(queryset_list[random.randrange(0,4)])
                context = {"search_result":drawn_list}
                template = loader.get_template('home/search_result.html')
                return HttpResponse(template.render(context, request))
        elif not query and not draw_food_type:
            draw_restaurant = request.POST.get("draw_restaurant")
            if draw_restaurant:
                queryset_list = Restaurant.objects.all()
                drawn_list = []
                drawn_list.append(queryset_list[random.randrange(0,4)])
                drawn_list.append(queryset_list[random.randrange(0,4)])
                drawn_list.append(queryset_list[random.randrange(0,4)])
                context = {"search_result":drawn_list}
                template = loader.get_template('home/search_result.html')
                return HttpResponse(template.render(context, request))
                
    elif request.user.is_authenticated():
        user_profile = UserProfile.objects.get(user=request.user)
        context = {'user_profile': user_profile}
        return render(request, 'home/index.html', context)
    else:
        # In the case of no user logged in. But the template can't load the picture because of bad pathing. 
        context = {'user_profile.user_icon.url': "/media/Screen_Shot_2017-08-16_at_3.06.20_PM_WdUo2EA.jpg"}
        return render(request, 'home/index.html', context)
        
    
#below is a way to show a detail view/ you should change it and use generic view later
#This view haven't be figured out yet.
# class RestaurantDetailView(DetailView):
#     model = Restaurant
#     template_name = 'home/redetail.html'
#     slug_field = 'restaurant_id'
#     slug_url_kwarg = 'name'
#     context_object_name = 'restaurant'
    #Still working on it( how to get dishes from the currently requested restaurant.)
    # def get_context_data(self, **kwargs):
    #     context = super(RestaurantDetailView, self).get_context_data(**kwargs)
    #     context["dishes"] = Dishes.objects.get(restaurant=self.object.pk)
    #     return context


# trying to make function based view for detail view below(remeber to change the url.py file if you want to use class based view.)
def restaurant_detail(request, pk):
    restaurant = Restaurant.objects.get(pk=pk)
    dishes = Dishes.objects.get(restaurant=pk)  #not sure how to call dishes of a particular restaurant.
    context = {'restaurant': restaurant, "dishes":dishes}
    return render(request, 'home/redetail.html', context)
    
    

    
    
  # You actually don't need the code in the following two blocks belows.
# def search_result(request):
#     queryset_list = Restaurant.objects.all()
#     query = request.GET.get("q")
#     if query:
#         queryset_list = queryset_list.filter(name__icontains=query)
#         context = {"search_result":queryset_list}
#         template = loader.get_template('home/search_result.html')
#         return HttpResponse(template.render(context, request))
        
    # elif not query:
    #     draw = request.GET.get("draw")
    #     if draw:
    #         queryset_list = Restaurant.objects.all()
    #         # queryset_list = queryset_list[:random.randrange(0,4)]
    #         context = {"search_result":queryset_list}
    #         template =  loader.get_template('home/search_result.html')
    #         return HttpResponse(template.render(context, request))
            
    

class RestaurantCreate(CreateView):
    model = Restaurant
    fields = ['name', 'address', 'cruisine', 'restaurant_logo']
    success_url = '/'
    


class UserFormView(View):
    form_class = UserForm
    template_name = 'home/registration_form.html'
     
    #display a blank form
    def get(self, request):
        # form = self.form_class(None)
        return render(request, self.template_name)
         
    # process form data and store them in the database         
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # clean data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
             
             # returns User objects if credentials are correct
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('home:index')
        return render(request, self.template_name, {'form': form})             
                     
          
             
# Trying to make a sign in page here 

         
         
def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                # albums = Album.objects.filter(user=request.user)
                # return render(request, 'home/homepage.html')
                return redirect('home:index')
            else:
                return render(request, 'home/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'home/login.html', {'error_message': 'Invalid login'})
    return render(request, 'home/login.html')


         #This is not working well because the icon file is not link to the db.
def profile(request):
    try:
        request.method == "GET"
        user_profile = UserProfile.objects.get(user=request.user)
        context = {'user_profile': user_profile}
        return render(request, 'home/profile.html', context)
    except Exception:
        return render(request, 'home/registration_form.html')
        
        # try:
        #     profile = request.user.userprofile
        #     profile.update(name=request.user, user_icon=request.POST.get('user_icon'))
        # except UserProfile.DoesNotExist:
        #     UserProfile.objects.create(user=request.user, user_icon=request.POST.get('user_icon'))
        #     user_profile = UserProfile.objects.get(user=request.user)
    # context = {'user_profile': user_profile}
    # return render(request, 'home/profile.html', context)
        
        

def contact(request):
    if request.method == "GET":
        return render(request, 'home/contact.1.html')
    elif request.method == "POST":
        ContactRecord.objects.create(name=request.POST['name'], email=request.POST['email'], phone=request.POST['phone'], message=request.POST['message'] )
        return render(request, 'home/index.html')


def food_order(request, pk):
    if request.method == "GET" and request.user.is_authenticated():
        restaurant = Restaurant.objects.get(pk=pk)
        dishes = Dishes.objects.filter(restaurant=pk)
        context = {'restaurant_pk':pk, 'dishes':dishes}
        return render(request, 'home/food_order.html', context)
    elif request.method == "GET" and not request.user.is_authenticated():
        return render(request, 'home/login.html')
    elif request.method == "POST" and request.user.is_authenticated():
        Order_records.objects.create(
        order_restaurant = Restaurant.objects.get(pk=pk),
        order_user = request.user,
        wanted_dish = Dishes.objects.get(restaurant=Restaurant.objects.get(pk=pk), name=request.POST['wanted_dish']),
        quantity = request.POST['quantity'],
        )
        return render(request, 'home/index.html')
        
        
def shop_view(request, pk):
    pass
#I probably need to add new attribute to the Django User model.

def logout_user(request):
    logout(request)
    # form = UserForm(request.POST or None)
    # context = {
    #     "form": form,
    # }
    # return render(request, 'home/homepage.html', context)
    return redirect('home:index')



# CreateView will automatically look for a template called "modelname_form.html" as the template of this view.
# class UpdateProfile(UpdateView):
#     model = UserProfile
#     fields = ['user_icon']
#     template_name_suffix = '_update_form'
#     success_url = '/'


# I am trying to make the update profile page using function based view
def update_profile(request):
    if request.method == "GET":
        return render(request, 'home/userprofile_form.html')
    elif request.method == "POST":
        #something wrong with the file uploading
        if request.FILES.get('user_icon'):
            user_profile = UserProfile.objects.get(user=request.user)
        # user_profile.update(user=request.user, user_icon=request.POST['uesr_icon'])
            # UserProfile.objects.filter(user=request.user).update(user_icon=request.FILES['user_icon'])
            # instance = UserProfile(user=request.user, user_icon=request.FILES['user_icon'])
            user_profile.user_icon=request.FILES['user_icon']
            user_profile.save(update_fields=['user_icon'])
        #Somethin wrong here but I don't know why this error doesn't affect the function of file uploading.
            
        username_update = request.POST.get("username_update")
        if username_update:
            User.objects.filter(pk=request.user.pk).update(username=username_update)
        # return render(request, 'home/profile.html')
            return redirect('home:index')
        
    