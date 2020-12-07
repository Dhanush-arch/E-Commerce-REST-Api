from django.shortcuts import render
from rest_framework import generics
from .models import User, Product, OrderCart, Category
from rest_framework.authtoken.models import Token
from .serializers import userSerializer, productSerializer, orderSerializer, useridSerializer, categorySerializer
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.pagination import PageNumberPagination

from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
# Create your views here.

class UserView(generics.CreateAPIView,generics.DestroyAPIView):
  authentication_classes = [TokenAuthentication]
  permission_classes = [IsAuthenticated]


  queryset = User.objects.all()
  serializer_class = userSerializer

  def get(self, request, uid,format=None):
    # print(request,uid,"Jkkkk")
    if uid is "0":
      getqueryset = User.objects.all()
      getserializer = userSerializer(getqueryset, many=True)
    else:
      getqueryset = User.objects.get(email=uid) ##GET request for a specific email
      getserializer = userSerializer(getqueryset, many=False)
    return Response(data=getserializer.data, status=status.HTTP_200_OK)

  def put(self, request):
    # print(request.data,"hello")
    putqueryset = User.objects.get(email=request.data['email'])
    putserializer = userSerializer(putqueryset, data=request.data)
    if putserializer.is_valid():
      putserializer.save()
      return Response(data=putserializer.data, status=status.HTTP_202_ACCEPTED)

class ProductView(generics.CreateAPIView,generics.DestroyAPIView):
  authentication_classes = [TokenAuthentication]
  #permission_classes = [IsAuthenticatedOrReadOnly]


  queryset = Product.objects.all()
  serializer_class = productSerializer

  def get(self, request, uid, format=None):
    # print("product", uid)
    if uid is "0":
      getqueryset = Product.objects.all()
      filter_word = request.query_params.get('search', '') #search
      if filter_word: #search filter
        getqueryset_productname = getqueryset.filter(productName__icontains=filter_word) #search by productname
        getqueryset_productdescription = getqueryset.filter(productDescription__icontains=filter_word) #search by productdescription
        getqueryset = getqueryset_productname | getqueryset_productdescription
      
      sortby_list = request.query_params.getlist("sortby") #Sorting # (-word) for descending and (word) for ascending
      if sortby_list:
        for word in sortby_list:
          getqueryset = getqueryset.order_by(word)
  
      page_number = request.query_params.get('page','') #pagination setup
      if page_number:
        paginator = PageNumberPagination()
        paginator.page_size = 1
        result_page = paginator.paginate_queryset(getqueryset, request)
        getserializer = productSerializer(result_page, many=True)
        return paginator.get_paginated_response(getserializer.data)
      
      getProductForOrder = request.query_params.getlist("fororder")
      print(getProductForOrder)
      if getProductForOrder:
        emptyqueryset = Product.objects.none()
        for productid in getProductForOrder:
          queryset_temp = getqueryset.filter(productID=productid)
          emptyqueryset = emptyqueryset | queryset_temp
        getqueryset = emptyqueryset
        
      getserializer = productSerializer(getqueryset, many=True)
    else:
      getqueryset = Product.objects.get(productID = uid) ##GET request for a specific ProductID
      getserializer = productSerializer(getqueryset, many=False)
    return Response(data=getserializer.data, status=status.HTTP_200_OK)

  def put(self, request):
    # print(request.data,"hello")
    putqueryset = Product.objects.get(productID=request.data['productID'])
    putserializer = productSerializer(putqueryset, data=request.data)
    if putserializer.is_valid():
      putserializer.save()
      return Response(data=putserializer.data, status=status.HTTP_202_ACCEPTED)

class OrderView(generics.CreateAPIView):
  authentication_classes = [TokenAuthentication]
  permission_classes = [IsAuthenticated]
  
  queryset = OrderCart.objects.all()
  serializer_class = orderSerializer
  
  def get(self, request, uid,format=None):
    # print(request,uid,"order")
    if uid is "0":
      getqueryset = OrderCart.objects.all()
      getserializer = orderSerializer(getqueryset, many=True)
    else:
      getqueryset = OrderCart.objects.filter(orderedUserID=uid)##GET request for a specific orderdedUserID
      getserializer = orderSerializer(getqueryset, many=True)
    return Response(data=getserializer.data, status=status.HTTP_200_OK)

  def put(self, request, uid):
    # print(request.data,"hello")
    putqueryset = OrderCart.objects.get(orderedUserID=request.data["orderedUserID"], orderedProductID=request.data["orderedProductID"])
    putserializer = orderSerializer(putqueryset, data=request.data)
    if putserializer.is_valid():
      putserializer.save()
      return Response(data=putserializer.data, status=status.HTTP_202_ACCEPTED)

  def delete(self, request, uid):
    try:
      queryset = OrderCart.objects.get(orderedUserID=request.data["orderedUserID"], orderedProductID=request.data["orderedProductID"]).delete()
    except:
      print("no content")
    #print(queryset)
    getqueryset = OrderCart.objects.filter(orderedUserID=uid)##GET request for a specific orderdedUserID
    getserializer = orderSerializer(getqueryset, many=True)
    return Response(data=getserializer.data, status=status.HTTP_200_OK)
    # return Response(data="deleted", status=status.HTTP_204_NO_CONTENT)
class UserId(APIView):
  authentication_classes = [TokenAuthentication]
  permission_classes = [IsAuthenticated]

  def post(self, request, format=None):
    queryset = Token.objects.filter(key=request.auth)
    serializer = useridSerializer(queryset, many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)
    
class CheckOrder(APIView):
  authentication_classes = [TokenAuthentication]
  permission_classes = [IsAuthenticated]

  def post(self, request, format=None):
    queryset = OrderCart.objects.filter(orderedUserID=request.data["orderedUserID"], orderedProductID=request.data["orderedProductID"])
    if(queryset):
      serializer = orderSerializer(queryset, many=True)
      return Response(data=serializer.data, status=status.HTTP_200_OK)
    else:
      return Response(data=False, status=status.HTTP_200_OK)

class CategoryView(APIView):
  def get(self, request, format=None):
    filter_word = request.query_params.get('search', '') #search
    if(filter_word):
      queryset = Product.objects.filter(productCategory=filter_word)
      print(len(queryset))
      if(len(queryset)>12):
        queryset = queryset[:12]
      getserializer = productSerializer(queryset, many=True)
      return Response(data=getserializer.data, status=status.HTTP_200_OK)
