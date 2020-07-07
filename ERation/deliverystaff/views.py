from django.shortcuts import render, HttpResponse
from customer.models import Customer, Orders
from datetime import datetime

# Create your views here.
def home(request):
    orders = Orders.objects.filter(delivery_staff = request.user, status='Approved')
    if request.method == "GET":
        return render(request, 'staff_home.html', {'orders': orders})
    else:
        orderid = request.POST.get('orderid')
        otp = request.POST.get('otp')
        print(otp)
        order = Orders.objects.get(pk=orderid)
        print(order.otp)
        if order.otp == int(otp):
            order.status = 'Delivered'
            order.dday = datetime.now().day
            order.dmonth = datetime.now().month
            order.year = datetime.now().month
            order.save()

            return render(
                request, 
                'staff_home.html', 
                {
                    'orders': orders,
                    'message': 'Order marked as delivered'
                }
            )

        else:

            return render(
                request, 
                'staff_home.html', 
                {
                    'orders': orders,
                    'message': 'Invalid OTP'
                }
            )