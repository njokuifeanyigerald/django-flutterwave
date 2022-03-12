from django.urls import path
from .views import list_products, product_detail,payment_response

urlpatterns = [
    path('', list_products, name="list_products" ),
    path('product/<int:pk>/details/', product_detail, name='detail'),
    path('callback/', payment_response, name='payment_response')
]
