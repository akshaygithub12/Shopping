import json
from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import requests
import datetime
# Create your views here.

def store(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_item': 0}
        cartItems = order['get_cart_items']

    product=Product.objects.all()
    context={'product':product,'cartItems':cartItems}
    return render(request,'store.html',context)


def cart(request):
    if request.user.is_authenticated:
        customer=request.user.customer
        order,created=Order.objects.get_or_create(customer=customer,complete=False)
        items= order.orderitem_set.all()
        cartItems=order.get_cart_items
    else:
        items=[]
        order={'get_cart_total':0,'get_cart_item':0}
        cartItems = order['get_cart_items']
    context={'items':items,'order':order,'cartItems':cartItems}
    return render(request,'cart.html',context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_item': 0}
        cartItems = order['get_cart_items']
    context = {'items': items, 'order': order,'cartItems':cartItems}
    return render(request,'checkout.html',context)

def updateItem(request):
    data=json.loads(request.body)
    action = data['action']
    productId = data['productId']
    print('action:',action)
    print('productid',productId)
    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order,created=Order.objects.get_or_create(customer=customer,complete=False)
    orderItem, created=OrderItem.objects.get_or_create(order=order,product=product)

    if action=='add':
        orderItem.quantity=(orderItem.quantity+1)
    elif action=='remove':
        orderItem.quantity=(orderItem.quantity-1)
    orderItem.save()

    if orderItem.quantity<=0:
        orderItem.delete()

    return JsonResponse('new data found',safe=False)


def process_order(request):
    transaction_id=datetime.datetime.now().timestamp()
    data=json.loads(request.body)

    if request.user.is_authenticated:
        customer=request.user.customer
        order,created=Order.objects.get_or_create(customer=customer,complete=False)
        total=float(data['form']['total'])
        order.transaction_id=transaction_id
        if total == order.get_cart_total:
            order.complete=True
        order.save()


        if Order.shipping == True:
            ShippingAddress.objects.create(
                customer=Customer,
                order=Order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zipcode'],
            )
    else:
        print('USer is not logged in')

    print('Data:',request.body)
    return JsonResponse("newdaaaaaaaa",safe=False)


