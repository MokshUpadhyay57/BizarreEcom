from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Product(models.Model):
    product_id = models.IntegerField(default=1)
    product_name = models.CharField(max_length=300)
    category = models.CharField(max_length=50, default="")
    price = models.IntegerField(default=0)
    desc = models.CharField(max_length=800)
    pub_date = models.DateField() 
    image = models.ImageField(upload_to="app/images", default="")

    def __str__(self):
       return self.product_name

class Contact(models.Model):
    msg_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=70, default="")
    phone = models.CharField(max_length=70, default="")
    desc = models.CharField(max_length=500, default="")

    def __str__(self):
       return self.desc

class Orders(models.Model):
    # ForeignKey for Order Model
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)
    order_id = models.AutoField(primary_key=True)
    amount = models.IntegerField(default=0)
    complete = models.BooleanField(default=False,null=True,blank=False)
    name = models.CharField(max_length=90)
    email = models.CharField(max_length=111)
    address = models.CharField(max_length=111)
    city = models.CharField(max_length=111)
    state = models.CharField(max_length=111)
    zip_code = models.CharField(max_length=111)
    phone = models.CharField(max_length=111, default="")


    def __str__(self):
        return str(self.order_id)

    @property
    def get_cart_total(self):
        orderupdate = self.orderupdate_set.all()
        total = sum([item.get_total for item in orderupdate]) 
        return total

    @property
    def get_cart_items(self):
        orderupdate = self.orderupdate_set.all()
        total = sum([item.quantity for item in orderupdate]) 
        return total





class OrderUpdate(models.Model):
    # Foreign Key of Product Model
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    update_id = models.AutoField(primary_key=True)
    quantity = models.IntegerField(default=0,null=True,blank=True)
    # Foreign Key for Order Model
    order = models.ForeignKey(Orders,on_delete=models.SET_NULL,null=True)
    update_desc = models.CharField(max_length=5000,default="Order has been placed.. ")
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.update_id)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


