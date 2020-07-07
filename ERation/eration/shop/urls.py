from django.urls import path
from . import views as v

urlpatterns = [
    path('', v.home, name='shop_home'),
    path('shopprofile/', v.shop_profile, name='shop_profile'),

    path('newcustomer/', v.new_customer, name='shop_new_customer'),
    path('viewcustomer/<int:id>', v.view_customer, name='shop_view_customer'),
    path('deletecustomer/<int:id>', v.delete_customer, name='shop_delete_customer'),

    path('viewallocations/', v.view_allocations, name='view_shop_allocations'),

    path('viewcards/', v.view_cards, name='shop_view_cards'),

    path('addsales/', v.add_sales, name='shop_add_sales'),
    path('newsale/<str:product>/<str:card_number>', v.new_sale, name='shop_new_sale'),

    path('monthlyreport/', v.monthly_report, name='shop_monthly_report'),

    path('stockupdate/', v.stock_update, name='shop_update_stock'),
    path('viewstockupdates/', v.view_stock_update, name='shop_view_stock_updates'),

    path('newdeliverystaff/', v.new_delivery_staff, name='shop_new_delivery_staff'),
    path('viewstaffs/', v.view_delivery_staffs, name='shop_view_delivery_staffs'),
    path('editstaff/<str:id>', v.edit_delivery_staff, name='shop_edit_delivery_staff'),

    path('vieworders/', v.view_orders, name='shop_view_orders'),
    path('vieworder/<int:orderid>', v.manage_order, name='shop_manage_order'),

]
