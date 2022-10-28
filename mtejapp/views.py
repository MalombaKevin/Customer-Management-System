from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import *

# Create your views here.

def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()   

    orders_total = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter( status='Pending').count()

    context = {'orders':orders, 'customers': customers, 'ordersTotal':orders_total,'delivered':delivered, 'pending':pending}



    return render (request, 'index.html', context)


def products(request):
    products = Product.objects.all()

    context = {'products': products}

    return render (request, "products.html", context)

def customer(request, pk):
    
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    totalOrders = orders.count()

    context= {'customer':customer, 'orders':orders, 'totalOrders': totalOrders}

    return render (request, "customer.html", context )


def createOrder(request):
    form = OrderForm()
    if request.method=="POST":
        # print("Printing:", request.POST)
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect("/")

    context={'form':form}

    return render(request, 'order_form.html', context)

def orderUpdate(request, pk):
    order = Order.objects.get(id=pk)

    form = OrderForm(instance=order)

    if request.method=="POST":
        form = OrderForm(request.POST,instance=order )
        if form.is_valid():
            form.save()
        return redirect('/')
    
    context={'form':form}

    return render (request, 'orderUpdate_form.html', context)

def deleteOrder(request, pk):
    order=Order.objects.get(id=pk)
    form=OrderForm()
    if request.method=="POST":
        order.delete()
        return redirect('/')

    return render(request, 'deleteOrder.html')


   
