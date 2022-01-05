# from django.db import models
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

# pdf file yaratish uchun < reportlab kutubxonasi orqali >
import io
from django.http import FileResponse, response
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

# pdf file yaratish uchun < xhtml2pdf kutubxonasi orqali >
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

from .import models
from products.models import ProductModel
from products.views import listing_large_view
from profile_pages.views import return_products_by_list

from profile_pages import models as p_p_models
# Create your views here.

# < pdf file yaratish funksiyasi < reportlab kutubxonasi orqali > >
def venue_pdf(request):
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica", 14)
    lines = [
        "first line", 
        "second line", 
        "third line",
    ]
    
    for line in lines:
        textob.textLine(line)
    
    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)
    return FileResponse(buf, as_attachment=True, filename='venue.pdf')


#  < pdf file yaratish funksiyasi < xhtml2pdf kutubxonasi orqali > >
def create_pdf_file(request, pk):
    order = models.Order.objects.get(id=pk)
    order_items = models.OrderItem.objects.filter(order_id=pk)
    
    print('Order: ', order.first_name)
    print('Order_item: ', order_items)
    for i in order_items:
        print('Order_item_status: ', i.item_status)
        print('Order_item_status_Type: ', type(i.item_status))
    
    template_path = 'orders/order_pdf.html'
    
    context = {
        'order': order,
        'order_items': order_items,
    }
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Order_qogoz.pdf"'
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(html, dest=response)
    
    if pisa_status.err:
        return HttpResponse('We have some error <pre>' + html + '</pre>')
    return response
# @login_required
def plus_cart_item(request,c_pk):
    try:
        cart_item = models.CartModel.objects.get(user=request.user, id=c_pk)
        cart_item.quantity += 1    
        cart_item.save()
    except models.CartModel.DoesNotExist:
        pass
   
    return redirect("shop-cart")



# @login_required
def minus_cart_item(request, c_pk):
    
    try:
        c_item = models.CartModel.objects.get(user=request.user, id=c_pk)
        if c_item.quantity > 1:
            c_item.quantity -=1
            c_item.save()
        else:
            c_item.delete()
    except models.CartModel.DoesNotExist:
        pass
    
    return redirect('shop-cart')



def add_to_cart(request, pk):                                              
    product = ProductModel.objects.filter(id=pk)
    
    cart_items = models.CartModel.objects.filter(user=request.user)
    c_items = return_products_by_list(cart_items)
    
    if request.POST:
        if product not in c_items:
            cm = models.CartModel(user=request.user)
    return redirect('product-detail')



def offer_view(request):
    
    return render(request, 'orders/offers.html')



def payment_view(request):
    
    return render(request, 'orders/payment.html')



def shopping_cart_view(request):
    cart_items = models.CartModel.objects.filter(user=request.user)
    cart_objects = cart_items
    total_price_in_cart = 0
    for c in cart_items:
        price = c.quantity * c.product.price
        total_price_in_cart += price
        
    # def get_total_price_after_entering_coupon_code(re)
    # <<--- getting total amount after entering coupon code --->>
    if request.POST:
        coupon_code = request.POST['coupon_code']
        if coupon_code:
            coupon = models.CouponModel.objects.get(code=coupon_code)
            print('Coupon code: ', coupon_code)
            print('Coupon: ', coupon)
            print('Based things: ', coupon.based_things.all())
            print('Nechta subcategoryga boglanganligi: ', coupon.based_things.count())
            print('BasedTo: ', coupon.based_things.all())
            coupon_price = 0
            for c_i in cart_items:
                print('Cart_subcatergory: ', c_i.product.subcategory)
                if c_i.product.subcategory in coupon.based_things.all():
                    coupon_price += c_i.product.price * (1/10)
            for co in coupon.based_things.all():
                print('Coupon based........: ', co)
            total_price_in_cart = total_price_in_cart - coupon_price
            print('Coupon_price: ', coupon_price)
    
    wls = models.WishlistModel.objects.filter(user=request.user)# <--- wishlit items
    wishlist_items = return_products_by_list(wls)
           
    context = {
        'cart_items': cart_items,
        'wishlist_items': wishlist_items,
        'total_price_in_cart': total_price_in_cart,
        'cart_objects': cart_objects,
    }
    return render(request, 'orders/shopping-cart.html', context)



def add_to_wishlist(request, pk, data):    
    if request.user.is_authenticated:
        product = ProductModel.objects.get(id=pk)
        wishlist_item = models.WishlistModel.objects.filter(user=request.user, product=product)

        if not wishlist_item.exists():
            wi = models.WishlistModel(user=request.user, product=product)
            wi.save()
            print('USer: ', wi.user)
            print('product: ', wi.product)
            print('added_at: ', wi.added_at)
        
        if data=='listing-large':
            slug=product.subcategory_slug
            return listing_large_view(request, slug)
        else:
            print('bu mahsulot allaqachon Wishlistda mavjud')
                
        return redirect(data)



def delete_from_wishlist(request, pk, data):    
    if request.user.is_authenticated:
        product = ProductModel.objects.get(id=pk)
        d_w_i = models.WishlistModel.objects.filter(product=product)
        w_items = models.WishlistModel.objects.filter(user=request.user)
        
        a = return_products_by_list(w_items)
        print(data)
        slug=product.subcategory_slug
        print(slug)
        try:
            d_w_i.delete()
            print('SUccess deleting ')
            
        except:
            print('yana xato')
    
        if data=='listing-large':
            slug=product.subcategory_slug
            
            return listing_large_view(request,slug)
        else:
            return redirect(data)



@login_required
def delete_from_cart(request, pk):
    c_item = models.CartModel.objects.filter(user = request.user, id=pk)
    if c_item.exists():
        c_item.delete()
    else:
        print('Cartdan ochirishda hatolik')
        
    return redirect('shop-cart')



def profile_order_view(request):
    wishlist_objects = models.WishlistModel.objects.filter(user=request.user)
    cart_objects = models.CartModel.objects.filter(user=request.user)
    # --------- orderlarni chiqrish bolimi boshlandi
    orders = models.Order.objects.filter(user=request.user)
    orders_id = []
    
    for o in orders:
        orders_id.append(o.id)
        
    order_items_nested = []
    order_items = []
    for o_i in orders_id:
        o_i_s = models.OrderItem.objects.filter(order_id=o_i) # o_i_s -> order items ni filter qilib olganlarim
        order_items_nested.append(o_i_s)
        
    if len(order_items_nested) > 1:
        for ob in order_items_nested:
            if len(ob) > 1:
                for i in ob:
                    order_items.append(i)
            else:
                order_items.append(ob[0])
    elif len(order_items_nested) == 1:
        order_items = order_items_nested[0]
    else:
        order_items = order_items_nested            
    # -------orderlarni chiqrish bolimi boshlandi tugadi
    context = {
        'cart_objects': cart_objects,
        'orders': orders,
        'order_items': order_items,
        'wishlist_objects': wishlist_objects,
    }
    return render(request, 'orders/profile-orders.html', context)



def add_to_order(request, data):
    user = request.user
    if user.is_authenticated and data=='add':
        cart_items = models.CartModel.objects.filter(user=user)
        order = models.Order()
        order_item = models.OrderItem()
        u_address = p_p_models.UserAddress.objects.filter(user=user).get(is_active=True)
        u_info = p_p_models.UserInfo.objects.get(username=user.username)
        if u_address != None:
            if u_info != None:
                print('Cart objects: ', cart_items)
                if cart_items.exists():
                    order.user = user
                    order.first_name = u_info.first_name
                    order.last_name = u_info.last_name
                    order.phone = u_info.phone
                    order.email = u_info.email
                    order.zip = u_info.zip
                    order.country = u_address.country
                    order.city = u_address.city
                    order.street = u_address.street
                    order.building = u_address.building
                    order.apartment = u_address.apartment
                    order.floor = u_address.floor
                    order.save()
                    for cart_item in cart_items:
                        order_item = models.OrderItem()
                        order_item.order_id = str(order.id)
                        order_item.product = ProductModel.objects.get(id=cart_item.product.id)
                        order_item.quantity = cart_item.quantity
                        order_item.status = 'All of good '
                        order_item.save()  
                        print(f'Cart item: {cart_item} \nPoduct_id: {cart_item.product.id}')
                        cart_item.delete()
            else:
                print('User_info yoq')
        else:
            print('User address yoq')
        return redirect('profile-orders')
    


def update_order_item_status(request, pk, status):
    if request.user.is_authenticated:
        o_item = models.OrderItem.objects.get(id=pk)
        o_item.item_status = status
        o_item.save()
        return redirect('profile-orders')
    else:
        pass