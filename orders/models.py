from django.db import models
from products import models as mdl
from django.contrib.auth.models import AnonymousUser, User
# Create your models here.

class CartModel(models.Model):
    class Meta:
        verbose_name = "Cart Item"
        verbose_name_plural = 'Cart Items'
    
    product = models.ForeignKey(mdl.ProductModel, on_delete=models.CASCADE)    
    quantity = models.IntegerField(default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    
    def total_price(self):
        if self.product.price != 0.0:
            return self.product.price * self.quantity
        else:
            return self.product.price * self.quantity
        
    
class WishlistModel(models.Model):
    class Meta:
        verbose_name = 'Wishlist item'
        verbose_name_plural = 'Wishlist items'
        
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(mdl.ProductModel, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return self.product

def generate_coupon_code():
    import random
    import string
    available_characters = string.ascii_letters + string.digits
    code = ''
    for i in range(8):
        index = random.randint(0, len(available_characters)-1)
        code += available_characters[index]  
    return code
    
    
class CouponModel(models.Model):
    class Meta:
        verbose_name = 'Coupon'
        verbose_name_plural = 'Coupons'
    
    code = models.CharField(max_length=8, null=True, default=generate_coupon_code)
    based_things = models.ManyToManyField(mdl.SubcategoryModel)
    stock = models.PositiveIntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    expiration_time = models.DateTimeField(null=True)  # Tugash vaqti
    
    def __str__(self):
        return f'{self.stock} based to {self.based_things.all()}'
        

class Order(models.Model):
    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    zip = models.IntegerField()
  
    country = models.CharField(max_length=60)
    city = models.CharField(max_length=60)
    street = models.CharField(max_length=80)
    building = models.CharField(max_length=60, null=True)
    apartment = models.CharField(max_length=12, null=True)
    floor = models.CharField(max_length=4, null=True)
   
    STATUS_CHOICES = (
    ('Waiting', "Waiting"),
    ('Delivered', "Delivered"),
    ('Payment is waiting', 'Payment is waiting')
    )
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Waiting')
    ordered_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.id}'

    
class OrderItem(models.Model):
    class Meta:
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'
    order_id = models.PositiveIntegerField()
    product = models.ForeignKey(mdl.ProductModel, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    STATUS_CHOICES = (
    ('All_of_good', 'All_of_good'),
    ('Return', "Return"),
    ('Cancel', "Cancel"),
    )
    item_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='All_of_good', null=True)
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.product}'