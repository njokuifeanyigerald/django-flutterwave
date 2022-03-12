from django.shortcuts import render, redirect
from .models import Product
from .forms import PaymentForm
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse

import math
import random
import requests



import environ
# Initialise environment variables
env = environ.Env()
environ.Env.read_env()

def list_products(request):
    products=Product.objects.all()
    context={
        'products':products
    }
    return render(request, 'app/products.html', context)

def product_detail(request, pk):
    data = Product.objects.get(id=pk)
    if request.method=='POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
             name=  form.cleaned_data['name']
             email = form.cleaned_data['email']
             amount = form.cleaned_data['amount']
             phone = form.cleaned_data['phone']
             return redirect(str(process_payment(name,email,amount,phone)))
    else:
        form = PaymentForm()
    ctx={
        'product':data,
        'form':form
    }
    return render(request,
                  'app/product.html',
                  ctx)

def process_payment(name,email,amount,phone):
    auth_token= env('SECRET_KEY')
    hed = {'Authorization': 'Bearer ' + auth_token}
    data = {
            "tx_ref":''+str(math.floor(1000000 + random.random()*9000000)),
            "amount":amount,
            "currency":"NGN",
            "redirect_url":"http://localhost:8000/callback",
            "payment_options":"card",
            "meta":{
                "consumer_id":23,
                "consumer_mac":"92a3-912ba-1192a"
            },
            "customer":{
                "email":email,
                "phonenumber":phone,
                "name":name
            },
            "customizations":{
                "title":"Trade9ja",
                "description":"Best Ecommerce store In Africa",
                "logo":"https://getbootstrap.com/docs/4.0/assets/brand/bootstrap-solid.svg"
            }
            }
    url = ' https://api.flutterwave.com/v3/payments'
    response = requests.post(url, json=data, headers=hed)
    response=response.json()
    link=response['data']['link']
    return link

@require_http_methods(['GET', 'POST'])
def payment_response(request):
    status=request.GET.get('status', None)
    tx_ref=request.GET.get('tx_ref', None)
    print(status)
    print(tx_ref)
    return HttpResponse('Finished')