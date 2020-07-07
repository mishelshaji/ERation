from django.shortcuts import render, redirect
from django.http import HttpResponse, request
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from . forms import *
from . models import *
from shop import forms as sform
from customer import forms as cform
from shop import models as smodel
from customer.models import Customer


def check_admin(request):
    return True if request.session['role'] == 'admin' else False


def home(request):
    return render(request, 'home.html')


@login_required
def newcard(request):
    if not check_admin(request):
        return HttpResponse("You donot have permission to view this page")

    cards = Cards.objects.all()
    if request.method == "GET":
        return render(request, 'newcard.html', {'form': NewCardForm(), 'cards': cards})
    else:
        c = NewCardForm(request.POST)
        if not c.is_valid():
            return render(request, "newcard.html", {'form': c, 'cards': cards})
        else:
            c.save()
            return redirect('newcard')


@login_required
def manage_card(request, id=0):
    if not check_admin(request):
        return HttpResponse("You donot have permission to view this page")

    cards = Cards.objects.all()
    if id > 0:
        Cards.objects.filter(id=id).delete()
        return render(request, 'managecard.html', {'cards': cards, 'message': 'Card Deleted'})

    if request.method == "GET":
        return render(request, 'managecard.html', {'cards': cards})
    else:
        return HttpResponse("Bad Request")


def usr_login(request):
    if request.method == "GET":
        lf = LoginForm()
        return render(request, 'login.html', {'form': lf})
    # ? If the method is POST
    else:
        lf = LoginForm(request.POST)

        #! Validating the form
        if not lf.is_valid():
            return render(request, 'login.html', {'form': lf})
        # ? If the form id valid
        else:
            email = lf.cleaned_data['email']
            password = lf.cleaned_data['password']

            user = authenticate(username=email, password=password)
            if user:
                request.session['username'] = user.email
                request.session['role'] = user.role
                login(request, user)
                if user.role == 'shop':
                    return redirect('shop_home')
                elif user.role == 'staff':
                    return redirect('staff_home')
                else:
                    return redirect('shops', permanent=False)
            else:
                return render(request, 'login.html', {'form': lf, 'message': 'Please check the email and password'})


@login_required
def view_shops(request):
    if not check_admin(request):
        return HttpResponse("You donot have permission to view this page")

    if request.method == "GET":
        shops = smodel.Shop.objects.all()
        return render(request, 'viewshops.html', {'shops': shops})

# * To view a particular shop
@login_required
def view_shop(request, id):
    if not check_admin(request):
        return HttpResponse("You donot have permission to view this page")

    if request.method == "GET":
        shop = smodel.Shop.objects.get(id=id)
        shop_form = sform.NewShopForm(instance=shop)
        return render(request, 'viewshop.html', {'form': shop_form})
    else:
        shop = smodel.Shop.objects.get(id=id)
        shop_form = sform.NewShopForm(request.POST, instance=shop)
        if shop_form.is_valid():
            shop_form.save()
            return render(request, 'viewshop.html', {'form': shop_form, 'message': 'Shop Updated'})
        else:
            return render(request, 'viewshop.html', {'form': shop_form})


@login_required
def new_shop(request):
    if not check_admin(request):
        return HttpResponse("You donot have permission to view this page")

    if request.method == "GET":
        user_form = LoginForm()
        shop_form = sform.NewShopForm()
        return render(request, 'addshop.html', {'form': shop_form, 'userform': user_form})

    else:
        user_form = LoginForm(request.POST)
        shop_form = sform.NewShopForm(request.POST)
        if not shop_form.is_valid() or not user_form.is_valid():
            return render(request, 'addshop.html', {'form': shop_form, 'userform': user_form})
        else:
            usr = user_form.save(commit=False)
            password = user_form.cleaned_data.get('password')
            usr.set_password(password)
            usr.save()
            shop = shop_form.save(commit=False)
            shop.id = usr
            shop.save()
            return redirect('shops', permanent=False)


@login_required
def new_product(request):
    if not check_admin(request):
        return HttpResponse("You donot have permission to view this page")

    if request.method == "GET":
        npf = NewProductForm()
        return render(request, 'newproduct.html', {'form': npf})

    else:
        npf = NewProductForm(request.POST)
        if npf.is_valid():
            npf.save()
            return redirect('viewproducts')
        else:
            return render(request, 'newproduct.html', {'form': npf})


@login_required
def view_products(request):
    if not check_admin(request):
        return HttpResponse("You donot have permission to view this page")

    if request.method == "GET":
        products = Products.objects.all()[0:200]
        return render(request, 'viewproducts.html', {'products': products})


@login_required
def view_product(request, id):
    if not check_admin(request):
        return HttpResponse("You donot have permission to view this page")

    if request.method == "GET":
        product = Products.objects.get(pk=id)
        npf = NewProductForm(instance=product)
        return render(request, 'editproduct.html', {'data': npf, 'id': id})
    else:
        product = Products.objects.get(pk=id)
        npf = NewProductForm(request.POST, instance=product)
        if npf.is_valid():
            npf.save()
            return render(request, 'editproduct.html', {'data': npf, 'id': id, 'message': 'Item updated'})
        else:
            return render(request, 'editproduct.html', {'data': npf, 'id': id})


@login_required
def delete_product(request, id):
    if not check_admin(request):
        return HttpResponse("You donot have permission to view this page")

    if request.method == "GET":
        Products.objects.filter(id=id).delete()
        return redirect('viewproducts')


@login_required
def new_allocation(request):
    if not check_admin(request):
        return HttpResponse("You donot have permission to view this page")

    if request.method == "GET":
        allocations = NewAllocationForm()
        return render(request, 'newallocation.html', {'form': allocations})

    else:
        allocations = NewAllocationForm(request.POST)
        if allocations.is_valid():
            allocations.save()
            return redirect('viewallocations')
        else:
            return render(request, 'newallocation.html', {'form': allocations})


@login_required
def view_allocations(request):
    if not check_admin(request):
        return HttpResponse("You donot have permission to view this page")

    if request.method == "GET":
        allocations = Allocations.objects.all().order_by(
            'card_name', 'product')[0:200]
        return render(request, 'viewallocations.html', {'data': allocations})

    else:
        return HttpResponse(status=400)


@login_required
def delete_allocation(request, id):
    if not check_admin(request):
        return HttpResponse("You donot have permission to view this page")

    if request.method == "GET":
        Allocations.objects.get(pk=id).delete()
        return redirect('viewallocations')

    else:
        return HttpResponse(status=400)

@login_required
def view_sales_report(request, id):
    if not id:
        return HttpResponse("Bad request")
    
    shop = smodel.Shop.objects.get(pk=id)
    if request.method == "GET":
        month=datetime.now().month
        year=datetime.now().year
        reports=SalesReport.objects.filter(year=year, month=month, shop_id=shop)
        return render(request, 'monthlyreport.html', {"data": reports})

    else:
        reports = SalesReport.objects.filter(year=request.POST.get('year'), month=request.POST.get('month'), shop_id=shop.shop_id)
        return render(request, 'monthlyreport.html', {"data": reports})

@login_required
def new_customer(request):
    if not check_admin(request):
        return HttpResponse("You donot have permission to view this page")

    if request.method == "GET":
        # shop = Shop.objects.get(pk=request.user)
        customer = cform.NewCustomerForm()
        # customer.fields['shop_id'].initial = shop.shop_id
        # customer.fields['shop_id'].widget.attrs['hidden'] = 'hidden'
        # customer.fields['shop_id'].label = ''
        return render(request, 'newcustomer.html', {'data': customer})
    else:
        # shop = Shop.objects.get(pk=request.user)
        customer = cform.NewCustomerForm(request.POST)
        if customer.is_valid():
            # customer.shop_id = shop.shop_id
            customer.save()
            msg = "New customer added"
            return render(request, 'newcustomer.html', {'data': customer, 'message': msg})
        else:
            # customer.fields['shop_id'].widget.attrs['value'] = shop.shop_id
            # customer.fields['shop_id'].label = ''
            # customer.fields['shop_id'].widget.attrs['hidden'] = 'hidden'
            return render(request, 'newcustomer.html', {'data': customer})

@login_required
def view_customers(request, shopid):
    if not check_admin(request):
        return HttpResponse("You donot have permission to view this page")
    
    if request.method == "GET":
        customer = Customer.objects.filter(pk=shopid)
        print(customer)
        return render(request, 'viewcustomers.html', {'data': customer})

@login_required
def view_customer(request, id):
    if not check_admin(request):
        return HttpResponse("You donot have permission to view this page")
    
    if request.method == "GET":
        customer = Customer.objects.get(pk=id)
        ncf = cform.NewCustomerForm(instance=customer)
        ncf.fields['shop_id'].widget.attrs['hidden'] = 'hidden'
        ncf.fields['shop_id'].label = 'Shop ID cannot be modified'
        return render(request, 'viewcustomer.html', {'data': ncf, 'id': id})

    else:
        customer = Customer.objects.get(pk=id)
        ncf = cform.NewCustomerForm(request.POST, instance=customer)
        ncf.shop_id = customer.shop_id
        if ncf.is_valid():
            ncf.save()
            return render(request, 'viewcustomer.html', {'data': ncf, 'id': id, 'message': 'Data updated'})
        else:
            return render(request, 'viewcustomer.html', {'data': ncf, 'id': id, 'message': 'Data not updated'})

@login_required
def delete_customer(request, id):
    if not check_admin(request):
        return HttpResponse("You donot have permission to view this page")

    if request.method == "GET":
        product = Customer.objects.get(pk=id).delete()
        return redirect('shop_home')

@login_required
def view_feedback(request):
    if not check_admin(request):
        return HttpResponse("You donot have permission to view this page")
    
    feedbacks = Complaints.objects.filter(reply = '')
    return render(request, 'viewfeedbacks.html', {'complaints':feedbacks})

@login_required
def reply_feedback(request, id):
    if not check_admin(request):
        return HttpResponse("You donot have permission to view this page")
    
    if request.method == "GET":
        complaint = Complaints.objects.get(pk=id)
        feedbackform = NewComplaintForm(instance=complaint)

        return render(request, 'replyfeedback.html', {'form':feedbackform})
    else:
        complaint = Complaints.objects.get(pk=id)
        feedbackform = NewComplaintForm(data=request.POST, instance=complaint)

        if feedbackform.is_valid():
            feedbackform.title = complaint.title
            feedbackform.complaint = complaint.complaint
            feedbackform.save()
            return render(request, 'replyfeedback.html', {'form':feedbackform, 'message': "You posted a reply"})
        else:
            return render(request, 'replyfeedback.html', {'form':feedbackform})

@login_required
def logout(request):
    request.session.clear()
    return redirect('user_login')
