from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password

# Create your models here.
class Booking(models.Model):
   first_name = models.CharField(max_length=200)    
   last_name = models.CharField(max_length=200)
   guest_number = models.IntegerField()
   comment = models.CharField(max_length=1000)

   def __str__(self):
      return self.first_name + ' ' + self.last_name

class Menu(models.Model):
   menu_name = models.CharField(max_length=200)    
   menu_type = models.IntegerField()
   menu_url = models.CharField(max_length=200)
   menu_price = models.FloatField();
   menu_description = models.TextField()
   menu_image = models.ImageField(upload_to='menu_images/')

   def __str__(self):
      return self.menu_name 

class Type(models.Model):
    type_name = models.CharField(max_length=200)

    def __str__(self):
      return self.type_name
   
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, role='user', **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, role=role, **extra_fields)
        if password:
            user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('role', 'admin')
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('role') != 'admin':
            raise ValueError('Superuser must have role="admin".')

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    role_choices = [
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('user', 'User'),
        ('delivery_crew', 'delivery crew')
    ]
    role = models.CharField(max_length=100, choices=role_choices, default='user')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
   
class CartItem(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Menu, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s CartItem {self.id}"

class DeliveryCrew(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='delivery_crew')
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user')
    status_choices = (
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('delivered', 'Delivered'),
        # Add other status choices as needed
    )
    status = models.CharField(max_length=20, choices=status_choices, default='pending')

    def __str__(self):
        return f"Delivery Crew: {self.user.username}"

from django.db import models

class Reservation(models.Model):
    name = models.CharField(max_length=100)
    reservation_date = models.DateField()
    reservation_time = models.TimeField()

    def __str__(self):
        return self.name + " - " + str(self.reservation_date) + " " + str(self.reservation_time)



# Add code to create Menu model