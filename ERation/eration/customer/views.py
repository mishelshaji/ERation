from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import CustomerLoginForm, NewComplaintForm
from .models import Customer, Orders
from eadmin.models import Allocations, SalesReport, Products, Complaints
from shop.models import Shop, Stocks
from django.db.models import Sum
from datetime import datetime

# Create your views here.
def home(request):
    if request.session['card_number']:
        customer = Customer.objects.filter(card_number=request.session.get('card_number'))
        print(customer)
        return render(request, 'customer_home.html', {'data': customer[0]})
    else:
        return redirect('customer_login', permanent=False)

def login(request):
    if request.method == "GET":
        clf = CustomerLoginForm()
        return render(request, 'customer_login.html', {'form': clf})
    else:
        print(request.POST)
        customer = Customer.objects.filter(card_number=request.POST.get('card_no'), phone=request.POST.get('phone'))[:1]
        if customer:
            request.session['card_number']=request.POST.get('card_no')
            request.session['role']='customer'
            return redirect('customer_home', permanent=False)
        else:
            return render(request, 'customer_login.html', {'form': CustomerLoginForm(), 'message': 'Invalid login details'})

def order_online(request):
    if request.method == "GET":
        card_number = request.session.get('card_number')

        if not card_number:
            return HttpResponse(status=400)

        # shop = Customer.objects.get(pk=request.user)
        customer = Customer.objects.filter(card_number=card_number)
        card_type = getattr(customer[0], 'card_type')
        products = Allocations.objects.filter(card_name=card_type) 

        #To store the name and total collected amount in a month
        data=[]
        for p in products:
            d={
                'product_name':None,
                'collectable':None,
                'collected':None,
                'form':None
            }
            m=datetime.now().month
            y=datetime.now().year
            total_collected = SalesReport.objects.filter(month=m, year=y, product=p.product.name, customer_id=card_number).aggregate(Sum('quantity'))
            
            d['product_name']=p.product.name
            d['price']=p.product.price * p.quantity
            d['collectable']=p.quantity
            d['collected']=total_collected['quantity__sum'] if total_collected['quantity__sum'] else 0

            # Fetching stocks
            stocks = Stocks.objects.get(shop_id=customer[0].shop_id, product=p.product)
            if stocks.quantity < p.quantity:
                d['status']="Out of stock"
                print(d['status'])
            else:
                d['status']="In Stock"
            # stock = {}
            # for s in stocks:
            #     stock[s.product.name] = s.quantity

            shop = Shop.objects.get(pk=customer[0].shop_id.id)
            # d['form'] = NewCollectionForm(product=p.product.name, card_number=card_number, shop_id=shop.shop_id)
            # print(d['form'])
            data.append(d)
            # collection_status[p.product.name]=total_collected['quantity__sum'] if total_collected['quantity__sum'] else 0


            # Fetching Stocks
            stockupdates = Stocks.objects.filter(shop_id=shop)
            if not stockupdates:
                return HttpResponse('''
                <html>
                <head>
                </head>
                <body>
                <h1>OUT OF STOCK</H1>
                </body>
                </html>
                ''')

        return render(
            request,
            'customer_order_online.html', 
            {
                'customer': customer, #customer details
                'card_name': card_type, #card type
                'products': products, #Collectable products
                'data': data,
                'card_number': card_number,
            }
        )

def save_online_order(request, product, quantity):
    product = Products.objects.get(name=product)
    customer = Customer.objects.get(card_number=request.session['card_number'])

    pre_ordered = Orders.objects.filter(product=product, month=datetime.now().month, year=datetime.now().year, customer=customer)
    if pre_ordered:
        return redirect('customer_home', permanent=False)

    orders = Orders()
    orders.customer = customer
    orders.product = product
    orders.price = quantity * product.price
    orders.otp = 0000
    orders.day=datetime.now().day
    orders.month=datetime.now().month
    orders.year=datetime.now().year
    orders.status=orders.STATUS[0][0]
    orders.quantity = quantity
    orders.save()

    stocks = Stocks.objects.get(product=product)
    stocks.quantity-=quantity
    stocks.save()
    return redirect("customer_home") 

def view_complaints(request):
    complaints = Complaints.objects.filter(customer_id__card_number=request.session.get('card_number'))
    return render(request, 'customer_complaints.html', {'complaints': complaints})

def new_complaint(request):
    if request.method == "GET":
        return render(request, 'customer_new_complaint.html', {'form': NewComplaintForm()})
    if request.method == "POST":
        ncf = NewComplaintForm(request.POST)
        customer = Customer.objects.get(card_number=request.session.get('card_number'))
        ncf.customer = customer.id
        if ncf.is_valid():
            ncf.save()
            return redirect('customer_view_complaints')
        else:
            return render(request, 'customer_new_complaint.html', {'form': ncf})
