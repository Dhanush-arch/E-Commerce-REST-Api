from django.db import models
from django.contrib.auth.models import User as defaultUser
# from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.

# class User(models.Model):
#   userName = models.CharField(max_length=100)
#   email = models.EmailField(unique=True)
#   group = models.CharField(max_length=100,default="Buyer",null=False)
#   isLogedIn = models.BooleanField(default=False,null=False)
  # def __str__(self):
  #     return self.userName
  
class User(models.Model):
  userName = models.OneToOneField(defaultUser, on_delete=models.CASCADE)
  def __str__(self):
      return str(self.userName)
  

@receiver(post_save, sender=defaultUser)
def create_user(sender, instance, created, **kwargs):
    if created:
        User.objects.create(userName=instance)

@receiver(post_save, sender=defaultUser)
def save_user(sender, instance, **kwargs):
    instance.user.save()

class Category(models.Model):
  name = models.CharField(max_length=100)
  description = models.CharField(max_length=200)
  def __str__(self):
    return self.name
class Product(models.Model):
  productID = models.AutoField(primary_key=True)
  productName = models.CharField(max_length=200, )
  productDescription = models.CharField(max_length=1000)
  originalPrice = models.IntegerField()
  discountPrice = models.IntegerField()
  isNew = models.BooleanField(default=False,null=False)
  hasDiscount = models.BooleanField(default=False,null=False)
  stars = models.IntegerField()
  date_uploaded = models.DateTimeField(auto_now_add=True)
  productImage = models.ImageField(upload_to="productImages", null=True, blank=True)
  productCategory = models.ForeignKey(Category, on_delete=models.CASCADE)
  def __str__(self):
    return self.productName

class OrderCart(models.Model):
  orderedUserID = models.ForeignKey(User, on_delete=models.CASCADE)
  orderedProductID = models.ForeignKey(Product, on_delete=models.CASCADE)
  totalPrice = models.IntegerField()
  dateOfOrder = models.DateTimeField(auto_now_add=True)
  quantity = models.IntegerField()
  statusOfProduct = models.CharField(max_length=100)
  def __str__(self):
    return "%s %s" % (self.orderedUserID, self.orderedProductID)
