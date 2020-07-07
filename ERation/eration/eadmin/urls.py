from django.urls import path
from . import views as v

urlpatterns = [
    path('', v.home, name='adminhome'),
    path('login/', v.usr_login, name='user_login'),
    path('newcard/', v.newcard, name='newcard'),
    path('managecard/', v.manage_card, name='managecard'),
    path('managecard/<int:id>/', v.manage_card, name='managecard'),

    path('shops/', v.view_shops, name='shops'),
    path('newshop/', v.new_shop, name='newshop'),
    path('viewshop/<int:id>/', v.view_shop, name='viewshop'),

    path('newproduct/', v.new_product, name='newproduct'),
    path('viewproducts/', v.view_products, name='viewproducts'),
    path('viewproduct/<int:id>', v.view_product, name='viewproduct'),
    path('deleteproduct/<int:id>', v.delete_product, name='deleteproduct'),

    path('newallocation/', v.new_allocation, name='newallocation'),
    path('viewallocations/', v.view_allocations, name='viewallocations'),
    path('deleteallocation/<int:id>', v.delete_allocation, name='deleteallocation'),

    path('viewsalesreport/<int:id>', v.view_sales_report, name='viewsalesreport'),

    path('newcustomer/', v.new_customer, name='newcustomer'),
    path('viewcustomers/<int:shopid>', v.view_customers, name='viewcustomers'),
    path('viewcustomer/<int:id>', v.view_customer, name='viewcustomer'),

    path('viewfeedbacks/', v.view_feedback, name='viewfeedbacks'),
    path('replyfeedback/<int:id>', v.reply_feedback, name='replyfeedback'),

    path('user_logout/', v.logout, name='user_logout'),
]
