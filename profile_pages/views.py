from django.core.checks.messages import Error
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from orders import models as o_mdl
from . import forms
from . import models
# Create your views here.

def profile_main_view(request):
    d_avatar = models.Default_avatar.objects.filter(is_active=True).first()
    cart_objects = o_mdl.CartModel.objects.filter(user=request.user)
    wishlist_items = o_mdl.WishlistModel.objects.filter(user=request.user)
    user_orders = o_mdl.Order.objects.filter(user=request.user)
    try:
        userinfo = models.UserInfo.objects.get(username=request.user.username)
    except:
        userinfo = request.user
    try:
        useraddress = models.UserAddress.objects.get(user=request.user, is_active=True)
    except:
        useraddress = None
    context = {
        'cart_objects': cart_objects,
        'userinfo': userinfo,
        'useraddress': useraddress,
        'd_avatar': d_avatar,
        'user_orders': user_orders,
        'wishlist_items': wishlist_items,
    }
    return render(request, 'profile/profile-main.html', context)

@login_required
def profile_address_view(request):
    cart_objects = o_mdl.CartModel.objects.filter(user=request.user)
    addresses = models.UserAddress.objects.filter(user=request.user)
    context = {
        'cart_objects': cart_objects,
        'addresses': addresses,
    }
    return render(request, 'profile/profile-address.html', context)


def return_products_by_list(objects):
    """"
        Bu funksiya productlarni list shaklida qaytaradi
    """
    ob_list = []
    for ob in objects:
        ob_list.append(ob.product)
    return ob_list


@login_required
def profile_wishlist_view(request):
    
    w_items = o_mdl.WishlistModel.objects.filter(user=request.user)
    cart_items = o_mdl.CartModel.objects.filter(user=request.user)
    
    cart_objects = cart_items 
    w_p_list = return_products_by_list(w_items)            
    ci_list = return_products_by_list(cart_items)
       
    for w_p in w_p_list:
        if w_p in ci_list:
            print('Cartda mavjud')
        else:
            print('cartda yoq')
    context = {
        'w_items': w_p_list,
        'cart_items':ci_list,
        'cart_objects': cart_objects,
    }
    return render(request, 'profile/profile-wishlist.html', context)


@login_required
def profile_setting_view(request):
    d_avatar = models.Default_avatar.objects.filter(is_active=True).first()
    cart_objects = o_mdl.CartModel.objects.filter(user=request.user)
    user = request.user         
    user_info_objects = models.UserInfo.objects.all()
    try:
        user_info = models.UserInfo.objects.get(username=user.username)
        if user_info in list(user_info_objects):
            form = forms.UserInfoForm(instance=user_info)
        else:
            form = forms.UserInfoForm()
    except:
        form = forms.UserInfoForm()
        user_info = ''
        
    if request.POST:
        if user_info in list(user_info_objects):
            form = forms.UserInfoForm(request.POST, request.FILES, instance=user_info)
        else:
            form = forms.UserInfoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            form_data = form.cleaned_data
            try:
                user.first_name = form_data['first_name']
                user.last_name = form_data['last_name']
                user.username = form_data['username']
                user.email = form_data['email'] 
                user.save()
                print('Userga saqlandi ')
            except:
                print('Userga saqlanmadi ')
            
            print('Form saved')
        else:
            print('Form validmas')
            print(form.errors)
     
    context = {
        'cart_objects': cart_objects,
        'user_info': user_info,
        'form': form,
        'user': user, #formada kamchilikim bor soat 00:43
        'd_avatar': d_avatar,
    }
    return render(request, 'profile/profile-setting.html', context)


def profile_seller_view(request):
    cart_objects = o_mdl.CartModel.objects.filter(user=request.user)
    
    context = {
        'cart_objects': cart_objects,
    }
    return render(request, 'profile/profile-seller.html', context)


# profile addings .......
def add_profile_address(request):
    user = request.user
    useraddresses =  models.UserAddress.objects.filter(user=user)
    form = forms.UserAddressForm()
    if request.POST:
        form = forms.UserAddressForm(request.POST)
        # print(form)
        if form.is_valid():
            data = form.cleaned_data
            a = 0
            for ua in useraddresses:
                if ua.country == data['country'] and ua.city == data['city'] and ua.street == data['street'] and ua.building == data['building']:
                    a+=1
            if data['is_active'] == True:
                print('Aktive=True')
                for u_adress in useraddresses:
                    u_adress.is_active = False
                    u_adress.save()                         
            if a < 1:
                print('mavjud emas')
                adres=models.UserAddress(user=request.user, is_active=data['is_active'], country=data['country'], city=data['city'], street=data['street'], building=data['building'], floor=data['floor'], apartment=data['apartment'])
                adres.save()
                return redirect('profile-address')
            else:
                print('Bu manzil allaqachin mavjud')
        else:
            print(form.errors)
    context = {
        'form': form,
        'user': user,
    }
    return render(request, 'profile/add_update_profile_address.html', context)


# profile updatings ........
def update_profile_address(request, pk):
    user = request.user
    user_address = models.UserAddress.objects.get(id=pk)
    user_addresses = models.UserAddress.objects.filter(user=user)
    print('User_addrsee: ', user_address.city)
    form = forms.UserAddressForm(instance=user_address)
    # print(form)
    if request.POST:
        form = forms.UserAddressForm(request.POST, instance=user_address)
        if form.is_valid():
            data = form.cleaned_data
            if data['is_active'] == True:
                for useraddress in user_addresses:
                    if useraddress.is_active == True:
                        useraddress.is_active = False
                        useraddress.save()
                form.save()
                return redirect('profile-address')
            else:
                form.save()
                return redirect('profile-address')
        else:
            form.save()
            return redirect('profile-address')
    context = {
        'form': form,
        'user': user,
    }
    return render(request, 'profile/add_update_profile_address.html', context)


# profile deletings
def delete_address(request, pk):
    try:
        user_address = models.UserAddress.objects.get(id=pk)
        user_address.delete()
    except:
        print('deleteda hatolik')
    return redirect('profile-address')


# making default to address
def make_default(request, pk):
    adress = models.UserAddress.objects.get(id=pk)
    adressses = models.UserAddress.objects.filter(user=request.user)
    for ad in adressses:
        if ad.is_active == True:
            ad.is_active = False
            ad.save()
            print(' adreesslar Active dan olindi')
    try:
        adress.is_active = True
        adress.save()
        print('Addres active qilindi')
    except:
        print("Adres active qilishda hatolik")
        pass
    return redirect('profile-address')


# # out of default
# def out_of_default(request, pk):
#     adress = models.UserAddress.objects.get(id=pk)
   
#     try:
#         adress.is_active = False
#         adress.save()
#         print('Addres activedan olindi albatta bitta addresni active qilishni unutmang') # message qilib jonat
#     except:
#         print("Adres disactive qilishda hatolik")
#     return redirect('profile-address')


