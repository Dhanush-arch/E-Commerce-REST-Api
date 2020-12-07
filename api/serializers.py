from rest_framework.serializers import ModelSerializer 
from .models import User, Product, OrderCart, Category
from rest_framework.authtoken.models import Token

class userSerializer(ModelSerializer):
  class Meta:
    model = User
    fields = "__all__"

class productSerializer(ModelSerializer):
  class Meta:
    model = Product
    fields = "__all__"

class orderSerializer(ModelSerializer):
  class Meta:
    model = OrderCart
    fields = "__all__"

class useridSerializer(ModelSerializer):
  class Meta:
    model = Token
    fields = '__all__'

class categorySerializer(ModelSerializer):
  class Meta:
    model = Category
    fields = '__all__'