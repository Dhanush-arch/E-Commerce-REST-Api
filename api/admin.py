from django.contrib import admin
from .models import User, Product, OrderCart, Category
# Register your models here.
admin.site.register(User)
admin.site.register(Product)
admin.site.register(OrderCart)
admin.site.register(Category)