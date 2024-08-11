from django.test import TestCase
from .models import Booking, Menu, Type, CustomUser, CartItem, DeliveryCrew, Reservation

class BookingModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Booking.objects.create(
            first_name='John',
            last_name='Doe',
            guest_number=3,
            comment='Test comment'
        )

    def test_first_name_label(self):
        booking = Booking.objects.get(id=1)
        field_label = booking._meta.get_field('first_name').verbose_name
        self.assertEqual(field_label, 'first name')  # Change assertEquals to assertEqual

    def test_booking_str_representation(self):
        booking = Booking.objects.get(id=1)
        self.assertEqual(str(booking), 'John Doe')  # Change assertEquals to assertEqual

class MenuModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Menu.objects.create(
            menu_name='Test Menu',
            menu_type=1,
            menu_url='test-url',
            menu_price=10.50,
            menu_description='Test description',
            menu_image='menu_images/test_image.jpg'
        )

    def test_menu_name_label(self):
        menu = Menu.objects.get(id=1)
        field_label = menu._meta.get_field('menu_name').verbose_name
        self.assertEqual(field_label, 'menu name')

    def test_menu_str_representation(self):
        menu = Menu.objects.get(id=1)
        self.assertEqual(str(menu), 'Test Menu')

class TypeModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Type.objects.create(
            type_name='Test Type'
        )

    def test_type_name_label(self):
        type_instance = Type.objects.get(id=1)
        field_label = type_instance._meta.get_field('type_name').verbose_name
        self.assertEqual(field_label, 'type name')

    def test_type_str_representation(self):
        type_instance = Type.objects.get(id=1)
        self.assertEqual(str(type_instance), 'Test Type')

class ReservationModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Reservation.objects.create(
            name='Test Reservation',
            reservation_date='2024-02-10',
            reservation_time='12:00:00'
        )

    def test_reservation_name_label(self):
        reservation = Reservation.objects.get(id=1)
        field_label = reservation._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_reservation_str_representation(self):
        reservation = Reservation.objects.get(id=1)
        expected_str = 'Test Reservation - 2024-02-10 12:00:00'
        self.assertEqual(str(reservation), expected_str)