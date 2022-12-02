from itertools import product
from django.contrib import admin
from .models import *

admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderDetails)
admin.site.register(BranchOffice)
admin.site.register(Admin)
admin.site.register(Book)
admin.site.register(Copy)
admin.site.register(Quantity)
admin.site.register(PaymentMethod)
admin.site.register(Booking)
admin.site.register(Shipping)
admin.site.register(PickUpStore)
