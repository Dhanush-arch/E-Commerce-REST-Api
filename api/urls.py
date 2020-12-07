from django.urls import path, include
from .views import *

urlpatterns = [
    path('user/<str:uid>/', UserView.as_view(),name="UserView"),
    path('product/<str:uid>/', ProductView.as_view(),name="ProductView"),
    path('order/<str:uid>/', OrderView.as_view(),name="OrderView"),
    path('getuserid/', UserId.as_view(), name='Getuserview'),
    path('checkorder/', CheckOrder.as_view(), name="checkorder"),
    path('getcategory/', CategoryView.as_view(), name="category"),
]
