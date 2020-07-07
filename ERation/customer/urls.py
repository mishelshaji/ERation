from django.urls import path
from . import views as v

urlpatterns = [
    path('', v.home, name='customer_home'),
    path('login/', v.login, name='customer_login'),
    path('orderonline/', v.order_online, name='customer_order_onlline'),
    path('saveonlineorder/<str:product>/<int:quantity>/', v.save_online_order, name='customer_save_online_order'),
    path('viewcomplaints/', v.view_complaints, name='customer_view_complaints'),
    path('newcomplaint/', v.new_complaint, name='customer_new_complaint'),
]