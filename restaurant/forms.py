from django.forms import ModelForm
from .models import Booking,Menu, Reservation


# Code added for loading form data on the Booking page
class BookingForm(ModelForm):
    class Meta:
        model = Booking
        fields = "__all__"

class MenuForm(ModelForm):
    class Meta:
        model = Menu
        fields = "__all__"

class ReservationForm(ModelForm):
    class Meta:
        model = Reservation
        fields = ['name', 'reservation_date', 'reservation_time']
