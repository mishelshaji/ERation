from django.contrib import admin
from . import models as m

# Register your models here.
admin.site.register(m.Shop)
admin.site.register(m.Stocks)
admin.site.register(m.StockUpdates)