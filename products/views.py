from itertools import product
from django.core.checks import messages
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

from orders.admin import CarttAdmin
from . import models
from orders.models import CartModel, WishlistModel
from orders.forms import CartForm

from profile_pages.views import return_products_by_list
from .extra_functions import filter_by_price
# Create your views here.

def categories_view(request, slug):
    cart_objects = CartModel.objects.filter(user=request.user)
    subcategories = models.SubcategoryModel.objects.filter(category_slug = slug)
    context = {
        'subcategories': subcategories,
        'cart_objects': cart_objects,
    }
    
    return render(request, 'products/category.html', context)

@login_required
def product_details(request, slug):
    product = models.ProductModel.objects.get(slug=slug)
    
    cart_objects = CartModel.objects.filter(user=request.user)
    
    cart_form = CartForm()
    cart_s = CartModel()                                            # kartga maxsulot qo'shish qismi
                                                                    # try va exept dan maqsad xatolik bolgan mahal
    try:                                                            #  kartaga mahsulot qo'shilishida muammo bolmasligin taminlash
        print('salom')
        cart_items = CartModel.objects.all()
        cart_items_list = list(cart_items)
        if product in cart_items_list:
            messages.info()
        if request.POST:
            cart_s.quantity = request.POST.get('quantity')
            cart_s.user = request.user
            cart_s.product = product
            cart_s.save()
            
    
    except ObjectDoesNotExist:
        print('alik')
        cart = CartModel.objects.create(product_id=models.ProductModel.objects.get(id=id), user = User.objects.get(id=request.user.id))
        cart.quantity = request.POST.get('quantity')
        try:
            cart.save()
        except:
            print('Error in saving')
    context = {
        'product': product,
        'cart_form': cart_form,
        'cart_objects': cart_objects,
    }
    
    return render(request, 'products/detail-product.html', context)

@login_required
def listing_large_view(request, slug):
    
    cart_objects = CartModel.objects.filter(user=request.user)
    
    wls = WishlistModel.objects.filter(user=request.user)
    wishlist_items = return_products_by_list(wls)
    productss = models.ProductModel.objects.filter(subcategory_slug = slug)
    # products = filter_by_price(request, products)
    products=productss
    if productss.count() > 1:
        mn_price = request.POST.get('min', None)
        mx_price = request.POST.get('max_price', None)
        if not mx_price:
            mx_price = 0
        if not mn_price:
            mn_price = 0
        min_price = float(mn_price)
        max_price = float(mx_price)
        
        print('min_price: ', min_price, 'type: ', type(min_price))
        print('max_price: ', max_price, 'type: ', type(max_price))
        
        try:
            if min_price and max_price:
                products = []
                for product in productss:
                    if product.price >= min_price and product.price <= max_price:
                        products.append(product)
                        print(product.name)
                
                if len(products)==0:
                    print('Bunday narxdagi maxsulotimiz topilmadi')
                        
        except:
            products = productss
            print('Filterlashda xatolik')
    else:
        products=productss
            
            
    # brands = []
    # if products.count() >1:
    #     for v in products:
    #         if v.manufacture not in brands:
    #             brands.append(v.manufacture)
    # elif products.count() == 1:
    #     brands=products.manufacture
    # else:
    #     pass
    # print('slug: ', slug, '   type: ', type(slug))
    context = {
        'products': products,
        'wishlist_items': wishlist_items,
        'cart_objects': cart_objects,
        # 'brands': brands,
    }
    return render(request, 'products/listing-large.html', context)



