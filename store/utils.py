import json
from . models import *
def cookieCart(request):
    try:
        cart=json.loads(request.COOKIES['cart'])
    except:
        cart={}
    items=[]
    order={'get_cart_total':0,'get_cart_items':0,'shipping':False}
    cartitems=order['get_cart_items']
    for i in cart:
        try:
            cartitems+=cart[i]["quantity"]
            product=Product.objects.get(id=i)
            total=(product.price*cart[i]["quantity"])
            order['get_cart_total']+=total
            order['get_cart_items']+=cart[i]["quantity"]

            item={
                    'product':{
                        'id':product.id,
                        'name':product.name,
                        'price':product.price,
                        'imageURL':product.imageURL,
                    },
                    'quantity':cart[i]["quantity"],
                    'get_total':total
                }
            items.append(item)
            if product.digital==False:
                order['shipping']=True
        except:
            pass
    return {'items':items,"order":order,'cartitems':cartitems}

def cartData(request):
    if request.user.is_authenticated:
        customer=request.user.customer
        order,created=Order.objects.get_or_create(customer=customer,complete=False)
        items=order.orderitem_set.all()
        cartitems=order.get_cart_items
    else:
        cookiedata=cookieCart(request)
        cartitems=cookiedata['cartitems']
        order=cookiedata['order']
        items=cookiedata['items']
    return {'items':items,"order":order,'cartitems':cartitems}

def guestOrder(request,data):
    print("User is not logged in...")
    name=data['form']['name']
    email=data['form']['email']
    cookiedata=cookieCart(request)
    items=cookiedata['items']
    customer,created=Customer.objects.get_or_create(email=email)
    customer.name=name
    customer.save()
    order=Order.objects.create(customer=customer,complete=False)
    for item in items:
        product=Product.objects.get(id=item['product']['id'])
        orderItem=OrderItem.objects.create(product=product,order=order,quantity=item['quantity'])
    return customer,order