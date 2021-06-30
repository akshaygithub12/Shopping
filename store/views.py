from django.shortcuts import render
from .models import *
from django.contrib.auth.models import UserManager


# Create your views here.

def store(request):
    product=Product.objects.all()
    context={'product':product}
    return render(request,'store.html',context)


def cart(request):
    if request.user.is_authenticated:
        customer=request.user.customer
        order,created=Order.objects.get_or_create(customer=customer,complete=False)
        items= order.orderitem_set.all()
    else:
        items=[]
        order={'get_cart_total':0,'get_cart_item':0}
    context={'items':items,'order':order}
    return render(request,'cart.html',context)

def checkout(request):
    context={}
    return render(request,'checkout.html',context)