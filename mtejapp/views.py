from django.shortcuts import render, redirect
from django.http import HttpResponse

from mtejapp.decorators import unauthenticated_user, allowed_users, admin_only
from .models import *
from .forms import *
from django.forms import inlineformset_factory
from .filters import OrderFilter
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import login, logout,authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
# Create your views here.
@unauthenticated_user
def registerPage(request):
   
        form= CreateUserForm()

        if request.method =="POST":
            form = CreateUserForm(request.POST)
            if form.is_valid():
                user = form.save()
                username = form.cleaned_data.get('username')
                group = Group.objects.get(name='customer')
                user.groups.add(group)
                Customer.objects.create(
                    user=user
                )
                messages.success(request, 'Account was created for ' + username)
                return redirect('loginPage')


        context = {'form':form}
        return render(request, 'accounts/register.html', context)

@unauthenticated_user
def loginPage(request):
  
    if request.method=="POST":
        username=request.POST.get('username')
        password= request.POST.get('password')
        user=authenticate(request, username=username, password=password )
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.info(request, "Username or  password is incorrect")         
   
    context = {}
    return render(request, 'accounts/login.html', context)

def logoutPage(request):
    logout(request)

    return redirect('loginPage')

@login_required(login_url='loginPage')
# @allowed_users(allowed_roles=["admin"])
@admin_only
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()   

    orders_total = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter( status='Pending').count()
    title= "MtejaBase"

    context = {'orders':orders, 'customers': customers, 'ordersTotal':orders_total,'delivered':delivered, 'pending':pending, 'title':title}



    return render (request, 'index.html', context)


@login_required(login_url='loginPage')
@allowed_users(allowed_roles=["customer"])
def UserPage(request):
    orders=request.user.customer.order_set.all()
    totalOrders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter( status='Pending').count()

    context ={
        "orders":orders,
        "ordersTotal":totalOrders,
        "delivered":delivered,
        "pending": pending,
       
    }
    print(orders)
    return render(request, "user.html", context)



@login_required(login_url='loginPage')
@allowed_users(allowed_roles=["admin"])
def products(request):
    products = Product.objects.all()

    context = {'products': products}

    return render (request, "products.html", context)

@login_required(login_url='loginPage')
@allowed_users(allowed_roles=["admin"])
def customer(request, pk):
    
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    totalOrders = orders.count()

    myFilter = OrderFilter(request.GET, queryset=orders)

    orders= myFilter.qs

    context= {'customer':customer, 'orders':orders, 'totalOrders': totalOrders, 'myFilter': myFilter}

    return render (request, "customer.html", context )

@login_required(login_url='loginPage')
@allowed_users(allowed_roles=["admin"])
def createOrder(request, pk):
    
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'))
    customer=Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(),instance=customer)
    
    # form = OrderForm(initial={'customer': customer})
    if request.method=="POST":
        # print("Printing:", request.POST)
        # form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST,instance=customer)
        if formset.is_valid():
            formset.save()
        return redirect("/")

    context={'formset':formset}

    return render(request, 'order_form.html', context)

@login_required(login_url='loginPage')
@allowed_users(allowed_roles=["admin"])
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

@login_required(login_url='loginPage')
@allowed_users(allowed_roles=["admin"])
def deleteOrder(request, pk):
    order=Order.objects.get(id=pk)
    form=OrderForm()
    if request.method=="POST":
        order.delete()
        return redirect('/')
    
    context = {'order':order}

    return render(request, 'deleteOrder.html', context)


@login_required(login_url='loginPage')
@allowed_users(allowed_roles=["admin"])
def createUser(request):

    form = CustomerForm()
    if request.method=="POST":
        form=CustomerForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('/')
    
    context = {'form':form}


    return render(request, 'customer/create.html', context)

@login_required(login_url='loginPage')
@allowed_users(allowed_roles=["admin"])
def updateUser(request, pk):
    customers = Customer.objects.get(id=pk)

    form = CustomerForm(instance=customers)

    if request.method=="POST":
        form=CustomerForm(request.POST, instance=customers)
        if form.is_valid():
            form.save()
        return redirect('/')
    
    context = {'form':form}

    return render (request, 'customer/update.html', context)

@login_required(login_url='loginPage')
@allowed_users(allowed_roles=["admin"])
def deleteUser(request, pk):

    customer = Customer.objects.get(id=pk)
    form = CustomerForm()
    
    if request.method=="POST":
        customer.delete()
        return redirect('/')
    context= {'form':form}
    
    return render(request, 'customer/delete.html', context)


@login_required(login_url='loginPage')
@allowed_users(allowed_roles=["customer"])
def settingsP(request):

    context = {}

    return render (request, 'settings.html', context )


   
