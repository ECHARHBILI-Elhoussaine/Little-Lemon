from django.contrib import admin
from .models import Menu, Booking, CustomUser, Type, CartItem, DeliveryCrew, Reservation

admin.site.register(Menu)
admin.site.register(Booking)
admin.site.register(CustomUser)
admin.site.register(Type)
admin.site.register(CartItem)
admin.site.register(DeliveryCrew)
admin.site.register(Reservation)
# Register your models here.
