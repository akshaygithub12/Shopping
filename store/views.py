from django.shortcuts import render
from .models import Product
# Create your views here.

def store(request):
    product=Product.objects.all()
    context={'product':product}
    return render(request,'store.html',context)


def cart(request):
    context={}
    return render(request,'cart.html',context)

def checkout(request):
    context={}
    return render(request,'checkout.html',context)