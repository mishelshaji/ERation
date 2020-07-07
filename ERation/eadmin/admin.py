from django.contrib import admin
from . import models as m

# Register your models here.
admin.site.register(m.User)
admin.site.register(m.Cards)
admin.site.register(m.Products)
admin.site.register(m.Allocations)
admin.site.register(m.SalesReport)
admin.site.register(m.Complaints)