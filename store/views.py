from django.shortcuts import render
from . models import *
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import json
import datetime

def store(request):
    if request.user.is_authenticated:
        customer, created = Customer.objects.get_or_create( name = request.user.username, email=request.user.email) 
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order ={'order.get_cart_total':0, 'order.get_cart_items':0,  'shipping':False}
        cartItems = 0
    products = Product.objects.all()
    context = {'products':products, 'cartItems':cartItems, 'shipping':False}
    return render(request, 'store/store.html', context)




@login_required
def cart(request):
    if request.user.is_authenticated:
        customer, created = Customer.objects.get_or_create( name = request.user.username, email=request.user.email, image=request.user.Customer.imageURL) 
        order, created = Order.objects.get_or_create(customer = customer, complete = False, )
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order ={'order.get_cart_items':0, 'order.get_cart_total':0, 'shipping':False}
        cartItems = order['get_cart_items']
    context = { 'items':items, 'order': order, 'cartItems':cartItems}
    return render(request, 'store/cart.html', context)




def checkout(request):
    if request.user.is_authenticated:
        customer, created = Customer.objects.get_or_create( name = request.user.username, email=request.user.email, image=request.user.Customer.imageURL) 
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order ={'order.get_cart_items':0, 'order.get_cart_total':0, 'shipping':False}
        cartItems = order['get_cart_items']
    context = { 'items':items, 'order': order, 'cartItems':cartItems, 'shipping':False}
    return render(request, 'store/checkout.html', context)



def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    customer, created = Customer.objects.get_or_create( name = request.user.username, email=request.user.email, image=request.user.Customer.imageURL)
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    order_item, created = OrderItem.objects.get_or_create(order=order, product=product)
    if action == 'add':
        order_item.quantity += 1
    elif action == 'remove':
        order_item.quantity -= 1
    order_item.save()
    if order_item.quantity <= 0:
        order_item.delete()
    return JsonResponse('Item was added', safe= False)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer, created = Customer.objects.get_or_create( name = request.user.username, email=request.user.email, image=request.user.Customer.imageURL)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id
        if total == order.get_cart_total:
            order.complete=True
        order.save()

        if order.shipping == 'True':
            ShippingAddress.objects.create(
                customer = customer,
                order=order,
                address = data['shipping']['address'],
                city = data['shipping']['city'],
                counrty = data['shipping']['country']
            )

    else:
        print('user is not loged in')
    return JsonResponse('Payment Completed', safe= False)

@login_required
def profile(request):
    return render(request, 'store/profile.html')






