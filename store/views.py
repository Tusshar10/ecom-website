from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import datetime
import json
from .utils import cookieCart,cartData,guestOrder
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import razorpay
# Create your views here.
def store(request):
    data=cartData(request)
    cartitems=data['cartitems']
    products=Product.objects.all()
    context={"products":products,'cartitems':cartitems}
    return render(request,'store/store.html',context)

def cart(request):
    data=cartData(request)
    cartitems=data['cartitems']
    order=data['order']
    items=data['items']
    context={'items':items,"order":order,'cartitems':cartitems}
    return render(request,'store/cart.html',context)

def checkout(request):
    data=cartData(request)
    cartitems=data['cartitems']
    order=data['order']
    items=data['items']
    client=razorpay.Client(auth=(settings.KEY,settings.SECRET))
    payment=client.order.create({'amount':order.get_cart_total*100,'currency':'INR','payment_capture':1})
    context={'items':items,"order":order,'cartitems':cartitems,'payment':payment}
    print("*************")
    print(payment)
    print("**************")
    return render(request,'store/checkout.html',context)

def updateItem(request):
    data=json.loads(request.body)
    productid=data['productId']
    action=data['action']
    print('Action:',action)
    print('ProductId:',productid)

    customer=request.user.customer
    product=Product.objects.get(id=productid)
    order,created=Order.objects.get_or_create(customer=customer,complete=False)
    orderitem,created=OrderItem.objects.get_or_create(product=product,order=order)
    if action=='add':
        orderitem.quantity+=1
    elif action=='remove':
        orderitem.quantity-=1
    orderitem.save()
    if orderitem.quantity<=0:
        orderitem.delete()
    return JsonResponse('Item was added',safe=False)

def processOrder(request):
    transaction_id=datetime.datetime.now().timestamp()
    data=json.loads(request.body)
    if request.user.is_authenticated:
        customer=request.user.customer
        order,created=Order.objects.get_or_create(customer=customer,complete=False)
        
    else:
        customer,order=guestOrder(request,data)
        
    total=float(data['form']['total'])
    order.transaction_id=transaction_id
    if total==float(order.get_cart_total):
        order.complete=True
    order.save()
    if order.shipping==True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shippinginfo']['address'],
            city=data['shippinginfo']['city'],
            state=data['shippinginfo']['state'],
            zipcode=data['shippinginfo']['zipcode'],
        )
    return JsonResponse('Item was added',safe=False)

@csrf_exempt
def handlerequest(request):
    pass
