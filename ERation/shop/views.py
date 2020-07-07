from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from . forms import NewShopForm, NewCollectionForm, ManageOrderForm
from . models import Shop, StockUpdates, Stocks
from eadmin.forms import LoginForm
from deliverystaff.forms import NewStaffForm
from deliverystaff.models import DeliveryStaff
from customer.models import Customer, Orders
from customer.forms import NewCustomerForm
from eadmin.models import Allocations, Cards, SalesReport, Products, SalesReport, User
from datetime import datetime
from random import randint
from django.core.mail import send_mail as sm

# Create your views here.


def authenticate(fun):
    def dec(request, *args, **kwargs):
        if request.session.has_key('role'):
            if request.session.get('role') == 'shop':
                return fun(request, *args, **kwargs)
            else:
                return HttpResponse("Invalid user")
        else:
            return HttpResponse("Please login first")
    return dec


@login_required
@authenticate
def home(request):
    shop = Shop.objects.get(pk=request.user)
    customers = Customer.objects.filter(shop_id=shop.shop_id)
    return render(request, 'shop_home.html', {'data': customers})

@login_required
@authenticate
def view_report(request):
    shop = Shop.objects.get(pk=request.user)
    years = SalesReport.objects.values('year').distinct()
    months = SalesReport.objects.values('month').distinct()
    print(years)
    return render(request, 'shop_home.html')

@login_required
@authenticate
def new_customer(request):
    if request.method == "GET":
        shop = Shop.objects.get(pk=request.user)
        customer = NewCustomerForm(
            initial={'shop_id': shop.shop_id}
        )
        # customer.fields['shop_id'].initial = shop.shop_id
        customer.fields['shop_id'].widget.attrs['hidden'] = 'hidden'
        customer.fields['shop_id'].label = ''
        return render(request, 'shop_new_customer.html', {'data': customer})
    else:
        shop = Shop.objects.get(pk=request.user)
        customer = NewCustomerForm(request.POST)
        if customer.is_valid():
            customer.shop_id = shop.shop_id
            customer.save()
            msg = "New customer added"
            return render(request, 'shop_new_customer.html', {'data': customer, 'message': msg})
        else:
            customer.fields['shop_id'].widget.attrs['value'] = shop.shop_id
            customer.fields['shop_id'].label = ''
            customer.fields['shop_id'].widget.attrs['hidden'] = 'hidden'
            return render(request, 'shop_new_customer.html', {'data': customer})


@login_required
@authenticate
def view_customer(request, id):
    if request.method == "GET":
        customer = Customer.objects.get(pk=id)
        ncf = NewCustomerForm(instance=customer)
        ncf.fields['shop_id'].widget.attrs['hidden'] = 'hidden'
        ncf.fields['shop_id'].label = 'Shop ID cannot be modified'
        return render(request, 'shop_view_customer.html', {'data': ncf, 'id': id})

    else:
        customer = Customer.objects.get(pk=id)
        ncf = NewCustomerForm(request.POST, instance=customer)
        ncf.shop_id = customer.shop_id
        if ncf.is_valid():
            ncf.save()
            ncf.fields['shop_id'].widget.attrs['hidden'] = 'hidden'
            ncf.fields['shop_id'].label = 'Shop ID cannot be modified'
            return render(request, 'shop_view_customer.html', {'data': ncf, 'id': id, 'message': 'Data updated'})
        else:
            return render(request, 'shop_view_customer.html', {'data': ncf, 'id': id, 'message': 'Data updated'})


@login_required
@authenticate
def delete_customer(request, id):
    if request.method == "GET":
        product = Customer.objects.get(pk=id).delete()
        return redirect('shops')


@login_required
@authenticate
def view_allocations(request):
    if request.method == "GET":
        allocations = Allocations.objects.all().order_by(
            'card_name', 'product', 'quantity')[0:200]
        return render(request, 'shop_view_allocations.html', {'data': allocations})
    else:
        return HttpResponse(status=400)


@login_required
@authenticate
def shop_profile(request):
    if request.method == "GET":
        u = request.user
        shop = Shop.objects.get(pk=u)
        shopform = NewShopForm(instance=shop)
        return render(request, 'shop_profile.html', {'data': shopform})
    else:
        s = Shop.objects.get(pk=request.user)
        shop = NewShopForm(request.POST, instance=s)
        message = ""
        if(shop.is_valid()):
            shop.save()
            message = "Profile updated"
        return render(request, 'shop_profile.html', {'data': shop, 'message': message})

@login_required
@authenticate
def view_cards(request):
    if request.method == "GET":
        cards = Cards.objects.all()
        return render(request, 'shop_view_cards.html', {'data': cards})
    else:
        return HttpResponse(status=400)

@login_required
@authenticate
def add_sales(request):
    if request.method == "GET":
        card_number = request.GET.get('cardno')

        if not card_number:
            return HttpResponse(status=400)

        shop = Shop.objects.get(pk=request.user)
        customer = Customer.objects.filter(shop_id=shop.shop_id, card_number=card_number)
        card_type = getattr(customer[0], 'card_type')
        products = Allocations.objects.filter(card_name=card_type) 

        #To store the name and total collected amount in a month
        data=[]
        for p in products:
            d={
                'product_name':None,
                'collectable':None,
                'collected':None,
                # 'form':None
            }
            m=datetime.now().month
            y=datetime.now().year
            total_collected = SalesReport.objects.filter(month=m, year=y, product=p.product.name, customer_id=card_number).aggregate(Sum('quantity'))
            
            d['product_name']=p.product.name
            d['collectable']=p.quantity
            d['collected']=total_collected['quantity__sum'] if total_collected['quantity__sum'] else 0

            # Fetching stocks
            stocks = Stocks.objects.get(shop_id=shop, product=p.product)
            if stocks.quantity < p.quantity:
                d['status']="Out of stock"
            else:
                d['status']="In Stock"
            # stock = {}
            # for s in stocks:
            #     stock[s.product.name] = s.quantity

            shop = Shop.objects.get(pk=request.user)
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
                <a href="/shop/stockupdate/">You must add stocks first. Click here to add some stocks.</a>
                </body>
                </html>
                ''')

        return render(
            request,
            'shop_add_sales.html', 
            {
                'customer': customer, #customer details
                'card_name': card_type, #card type
                'products': products, #Collectable products
                'data': data,
                'card_number': card_number,
            }
        )
        #return HttpResponse(card_number)

@login_required
@authenticate
def new_sale(request, product, card_number):
    if request.method == "GET":
        card_number = card_number

        if not card_number:
            return HttpResponse(status=400)

        shop = Shop.objects.get(pk=request.user)
        customer = Customer.objects.filter(shop_id=shop.shop_id, card_number=card_number)
        card_type = getattr(customer[0], 'card_type')
        products = Allocations.objects.filter(card_name=card_type) 

        #To store the name and total collected amount in a month
        data={
            'product_name':None,
            'collectable':None,
            'collected':None
        }
        for p in products:          
            m=datetime.now().month
            y=datetime.now().year
            total_collected = SalesReport.objects.filter(month=m, year=y, product=p.product.name, customer_id=card_number).aggregate(Sum('quantity'))
            
            data['product_name']=p.product.name
            data['collectable']=p.quantity
            data['collected']=total_collected['quantity__sum'] if total_collected['quantity__sum'] else 0
        
        form = NewCollectionForm() 
        form.fields['shop_id'].widget.attrs['readonly']='true'
        form.fields['shop_id'].widget.attrs['value']=shop.shop_id
        form.fields['card_number'].widget.attrs['readonly']='true'
        form.fields['card_number'].widget.attrs['value']=card_number
        form.fields['product'].widget.attrs['readonly']='true'
        form.fields['product'].widget.attrs['value']=product
        return render(
            request,
            'shop_new_sale.html', 
            {
                'form': form
            }
        )
    
    else:
        card_number = card_number

        if not card_number:
            return HttpResponse(status=400)

        shop = Shop.objects.get(pk=request.user)
        customer = Customer.objects.filter(shop_id=shop.shop_id, card_number=card_number)
        card_type = getattr(customer[0], 'card_type')
        products = Allocations.objects.filter(card_name=card_type) 

        #To store the name and total collected amount in a month
        data={
            'product_name':None,
            'collectable':None,
            'collected':None
        }
        for p in products:          
            m=datetime.now().month
            y=datetime.now().year
            total_collected = SalesReport.objects.filter(month=m, year=y, product=p.product.name, customer_id=card_number).aggregate(Sum('quantity'))
            
            data['product_name']=p.product.name
            data['collectable']=p.quantity
            data['collected']=total_collected['quantity__sum'] if total_collected['quantity__sum'] else 0
        
        form = NewCollectionForm(request.POST)
        if(int(request.POST.get('quantity'))+int(data['collected'])>int(data['collectable'])):
            return HttpResponse("Invalid Quantity")
        
        if form.is_valid():
            sr=SalesReport()
            sr.shop_id=shop
            sr.customer_id=Customer.objects.filter(card_number=card_number)[0]
            sr.quantity=request.POST.get('quantity')
            sr.product=Products.objects.filter(name=product)[0]
            sr.save()
        
            return render(
                request,
                'shop_new_sale.html', 
                {
                    'form': form,
                    'message': "New sales recorded",
                    'redirect': True,
                    'cardno': card_number
                }
            )
        else:   
            form.fields['shop_id'].widget.attrs['readonly']='true'
            form.fields['shop_id'].widget.attrs['value']=shop.shop_id
            form.fields['card_number'].widget.attrs['readonly']='true'
            form.fields['card_number'].widget.attrs['value']=card_number
            form.fields['product'].widget.attrs['readonly']='true'
            form.fields['product'].widget.attrs['value']=product
            return render(
                request,
                'shop_new_sale.html', 
                {
                    'form': form
                }
            )

@login_required
@authenticate
def monthly_report(request):
    shop = Shop.objects.get(pk=request.user)
    if request.method == "GET":
        month=datetime.now().month
        year=datetime.now().year
        reports=SalesReport.objects.filter(year=year, month=month, shop_id=shop.shop_id)
        return render(request, 'shop_monthly_report.html', {"data": reports})

    else:
        reports = SalesReport.objects.filter(year=request.POST.get('year'), month=request.POST.get('month'), shop_id=shop.shop_id)
        return render(request, 'shop_monthly_report.html', {"data": reports})

@login_required
@authenticate
def stock_update(request):
    if request.method == "GET":
        products = Products.objects.all()
        return render(request, 'shop_update_stock.html', {'products': products})
    else:
        # Creating stock record and create a stock update recore
        stockname = request.POST.get("name")
        if not stockname:
            return HttpResponse("Bad request")
        
        shop = Shop.objects.get(pk=request.user)
        stockupdate = StockUpdates.objects.create(
            name=stockname,
            shop_id=shop,
        )

        newstocks = request.POST

        for k,v in newstocks.items():
            # Updating stock table
            if k == "name" or k == "csrfmiddlewaretoken":
                continue
            product = Products.objects.get(name=k)
            
            stock = Stocks.objects.filter(
                shop_id = shop,
                product = product,
            )[:1]
            if not stock:
                s = Stocks.objects.create(
                    update_id = stockupdate,
                    shop_id = shop,
                    product = product,
                    quantity = int(v)
                )
            else:
                stock[0].quantity+=int(v)
                stock[0].update_id = stockupdate
                stock[0].save()
            # try:
            #     stock = Stocks.objects.get(product=product, shop_id=shop)
            #     stock.update_id = stockupdate
            #     stock.quantity += int(v)
            #     stock.save()
            # except Stocks.DoesNotExist as e:
            #     stock = Stocks.objects.create(
            #         update_id = stockupdate,
            #         shop_id = shop,
            #         product = product,
            #         quantity = int(v)
            #     )
        
        return redirect('shop_view_stock_updates')
        

@login_required
@authenticate
def view_stock_update(request):
    shop = Shop.objects.get(pk=request.user)
    stockupdates = StockUpdates.objects.filter(
        shop_id=shop
    )[:100]
    return render(request, 'shop_view_stock_updates.html', {"data": stockupdates})

@login_required
@authenticate
def new_delivery_staff(request):
    if request.method == "GET":
        user_form = LoginForm()
        staff_form = NewStaffForm
        return render(request, 'shop_new_staff.html', {'form': staff_form, 'userform': user_form})

    else:
        user_form = LoginForm(request.POST)
        staff_form = NewStaffForm(request.POST)
        if not staff_form.is_valid() or not user_form.is_valid():
            return render(request, 'shop_new_staff.html', {'form': staff_form, 'userform': user_form})
        else:
            usr = user_form.save(commit=False)
            password = user_form.cleaned_data.get('password')
            usr.set_password(password)
            usr.role = "staff"
            usr.save()
            staff = staff_form.save(commit=False)
            staff.id = usr
            staff.shop = Shop.objects.get(pk=request.user)
            staff.save()
            return redirect('/', permanent=False)

@login_required
@authenticate
def edit_delivery_staff(request, id):
    if request.method == "GET":
        staff = DeliveryStaff.objects.get(id__email=id)
        nsf = NewStaffForm(instance=staff)
        return render(request, 'shop_edit_staff.html', {'form':nsf})

@login_required
@authenticate
def view_delivery_staffs(request):
    staff = DeliveryStaff.objects.filter(shop=Shop.objects.get(pk=request.user))
    return render(request, 'shop_view_staff.html', {'data': staff})

@login_required
@authenticate
def view_orders(request):
    # orders = Orders.objects.select_related('customer')
    orders = Orders.objects.filter(customer__shop_id = Shop.objects.get(pk=request.user))
    return render(request, 'shop_view_orders.html', {'data': orders})


@login_required
@authenticate
def manage_order(request, orderid):
    if request.method == "GET":
        order = Orders.objects.get(pk=orderid)
        stafflist = DeliveryStaff.objects.filter(shop=Shop.objects.get(pk=request.user))
        return render(
            request, 
            'shop_manage_order.html', 
            {
                'order': order,
                'stafflist': stafflist,
            }
        )
    
    else:
        action = request.POST.get('status')
        if action == "approve":
            order = Orders.objects.get(pk=orderid)
            otp = randint(1000, 9999)

            res = sm(
                subject = 'OTP for your eration order.',
                message = 'Your OTP is: ' + str(otp),
                from_email = 'erationproject27@gmail.com',
                recipient_list = ['mishelvettukattil@outlook.com'],
                fail_silently=False,
            )    

            print(f"Email sent to {res} members")
            print(str.center(str(otp), 25, "*"))

            order.otp = otp
            order.status = "Approved"

            order.delivery_staff = request.POST.get('staff')
            print(order)
            order.save()
            return redirect('shop_view_orders', permanent=False)
        elif action == "reject":
            order = Orders.objects.get(pk=orderid)
            order.status = "Rejected"
            order.save()

            shop = Shop.objects.get(pk=request.user)
            stock = Stocks.objects.get(shop_id=shop, product=order.product)
            print(stock.update_id)
            stock.quantity += order.quantity
            stock.save()
            return redirect('shop_view_orders', permanent=False)
