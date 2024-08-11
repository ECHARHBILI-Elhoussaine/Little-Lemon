# from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .forms import BookingForm, ReservationForm
from django.urls import reverse
from .models import Menu, Type, DeliveryCrew, CartItem, Reservation
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer, TypeSerializer, CartItemSerializer, DeliveryCrewSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password
from .authentication import CustomUserAuthenticationBackend, CustomJWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer, MenuSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.pagination import PageNumberPagination
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers import serialize
from django.http import JsonResponse
import json


# Create your views here.
def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def menu(request):
    # Retrieve menu items from the database and order them by name ascending and price descending
    menu_items = Menu.objects.order_by('menu_name', '-menu_price')

    # Create a list to store menu data
    menu_data = []

    # Iterate over menu items to create URLs
    for item in menu_items:
        url = reverse('menu_detail', args=[item.id])  # Example URL pattern
        menu_data.append({'menu_name': item.menu_name, 'menu_url': url, 'menu_price': item.menu_price})

    context = {'menu_data': menu_data}
    return render(request, 'menu.html', context)

def menu_detail(request, id):
    # Retrieve the menu item detail from the database
    menu_item = get_object_or_404(Menu, id=id)
    menu_hierarchy = [
        {'title': 'Home', 'url': '/'},  # Define the Home link
        {'title': 'Menu', 'url': '/menu/'},  # Define the Menu link
        {'title': menu_item.menu_name, 'url': ''},  # Define the Current Item link with the menu name
    ]
    context = {'menu_item': menu_item, 'menu_hierarchy': menu_hierarchy}
    return render(request, 'menu_detail.html', context)

@csrf_exempt
def book(request):
    form = ReservationForm()

    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('reservations') 

    reserved_times = []
    reservations = []

    if request.POST.get('reservation_date'):
        selected_date = request.POST['reservation_date']
        reservations_qs = Reservation.objects.filter(reservation_date=selected_date)
        reserved_times = [reservation.reservation_time.strftime('%H:%M') for reservation in reservations_qs]
        reservations = [{'name': reservation.name, 'reservation_time': reservation.reservation_time.strftime('%H:%M')} for reservation in reservations_qs]

    context = {'form': form, 'reserved_times': reserved_times, 'reservations': reservations}

    if request.POST.get('reservation_date'):
        return JsonResponse({'reserved_times': reserved_times, 'reservations': reservations, 'timeslots': [f"{hour:02d}:{minute:02d}" for hour in range(8, 21) for minute in [0, 15, 30, 45]]})

    return render(request, 'book.html', context)

def reservations(request):
    # Retrieve reservations from the database and order them by reservation_date ascending and reservation_time ascending
    reservations = Reservation.objects.order_by('reservation_date', 'reservation_time')

    # Create a list to store reservation data
    reservation_data = []

    # Iterate over reservations to create reservation data
    for reservation in reservations:
        # Format reservation date and time as strings
        reservation_date_str = reservation.reservation_date.strftime('%Y-%m-%d')
        reservation_time_str = reservation.reservation_time.strftime('%H:%M')

        # Create a dictionary for each reservation with the specified structure
        reservation_dict = {
            "model": "restaurant.reservation",
            "pk": reservation.pk,
            "fields": {
                "name": reservation.name,
                "reservation_date": reservation_date_str,
                "reservation_time": reservation_time_str,
                "reservation_slot": 1
            }
        }

        # Append the reservation dictionary to the list
        reservation_data.append(reservation_dict)

    # Pass the reservation data to the template context
    context = {'reservation_data': reservation_data}

    # Render the reservations.html template with the context
    return render(request, 'reservations.html', context)

# Add your code here to create new views
# Api 


class UserRegistration(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response({"message": "User registration failed", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class UserLogin(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        # Authenticate using custom authentication backend
        user = CustomUserAuthenticationBackend().authenticate(request, email=email, password=password)

        if user:
            role = user.role
            refresh = RefreshToken.for_user(user)
            return Response({
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh),
                'role': role 
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class MenuList(APIView):
    authentication_classes = [CustomJWTAuthentication]

    def get(self, request):
        # Get page, per_page, order_by, and order_type parameters from query parameters
        page = int(request.query_params.get('page', 1))
        per_page = int(request.query_params.get('per_page', 10))
        order_by = request.query_params.get('order_by')
        order_type = request.query_params.get('order_type', 'desc')

        # Get all menus
        menus = Menu.objects.all()

        # Apply ordering if specified
        if order_by:
            if order_type == 'desc':
                menus = menus.order_by(f'-{order_by}')
            else:
                menus = menus.order_by(order_by)

        # Paginate the queryset
        paginator = PageNumberPagination()
        paginator.page_size = per_page
        paginated_menus = paginator.paginate_queryset(menus, request)

        # Serialize paginated menus
        serializer = MenuSerializer(paginated_menus, many=True)

        # Construct paginated response
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = MenuSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MenuDetail(APIView):
    authentication_classes = [CustomJWTAuthentication]

    def get_object(self, pk):
        try:
            return Menu.objects.get(pk=pk)
        except Menu.DoesNotExist:
            raise status.HTTP_400_BAD_REQUEST

    def get(self, request, pk):
        menu = self.get_object(pk)
        serializer = MenuSerializer(menu)
        return Response(serializer.data)

    def put(self, request, pk):
        menu = self.get_object(pk)
        serializer = MenuSerializer(menu, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        menu = self.get_object(pk)
        menu.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class TypeList(APIView):
    authentication_classes = [CustomJWTAuthentication]

    def get(self, request):
        # Get page, per_page, order_by, and order_type parameters from query parameters
        page = int(request.query_params.get('page', 1))
        per_page = int(request.query_params.get('per_page', 10))
        order_by = request.query_params.get('order_by')
        order_type = request.query_params.get('order_type', 'desc')

        # Get all types
        types = Type.objects.all()

        # Apply ordering if specified
        if order_by:
            if order_type == 'desc':
                types = types.order_by(f'-{order_by}')
            else:
                types = types.order_by(order_by)

        # Paginate the queryset
        paginator = PageNumberPagination()
        paginator.page_size = per_page
        paginated_types = paginator.paginate_queryset(types, request)

        # Serialize paginated types
        serializer = TypeSerializer(paginated_types, many=True)

        # Construct paginated response
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = TypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TypeDetail(APIView):
    authentication_classes = [CustomJWTAuthentication]

    def get_object(self, pk):
        try:
            return Type.objects.get(pk=pk)
        except Type.DoesNotExist:
            raise status.HTTP_400_BAD_REQUEST

    def get(self, request, pk):
        type_obj = self.get_object(pk)
        serializer = TypeSerializer(type_obj)
        return Response(serializer.data)

    def put(self, request, pk):
        type_obj = self.get_object(pk)
        serializer = TypeSerializer(type_obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        type_obj = self.get_object(pk)
        type_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class CartItemList(APIView):
    authentication_classes = [CustomJWTAuthentication]

    def get(self, request):
        # Get page, per_page, order_by, and order_type parameters from query parameters
        page = int(request.query_params.get('page', 1))
        per_page = int(request.query_params.get('per_page', 10))
        order_by = request.query_params.get('order_by')
        order_type = request.query_params.get('order_type', 'desc')

        # Get all cart items
        cart_items = CartItem.objects.all()

        # Apply ordering if specified
        if order_by:
            if order_type == 'desc':
                cart_items = cart_items.order_by(f'-{order_by}')
            else:
                cart_items = cart_items.order_by(order_by)

        # Paginate the queryset
        paginator = PageNumberPagination()
        paginator.page_size = per_page
        paginated_cart_items = paginator.paginate_queryset(cart_items, request)

        # Serialize paginated cart items
        serializer = CartItemSerializer(paginated_cart_items, many=True)

        # Construct paginated response
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = CartItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CartItemDetail(APIView):
    authentication_classes = [CustomJWTAuthentication]

    def get_object(self, pk):
        try:
            return CartItem.objects.get(pk=pk)
        except CartItem.DoesNotExist:
            raise status.HTTP_400_BAD_REQUEST

    def get(self, request, pk):
        cart_item = self.get_object(pk)
        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data)

    def put(self, request, pk):
        cart_item = self.get_object(pk)
        serializer = CartItemSerializer(cart_item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        cart_item = self.get_object(pk)
        cart_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class DeliveryCrewList(APIView):
    authentication_classes = [CustomJWTAuthentication]

    def get(self, request):
        delivery_crew = DeliveryCrew.objects.all()
        serializer = DeliveryCrewSerializer(delivery_crew, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = DeliveryCrewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeliveryCrewDetail(APIView):
    authentication_classes = [CustomJWTAuthentication]

    def get_object(self, pk):
        try:
            return DeliveryCrew.objects.get(pk=pk)
        except DeliveryCrew.DoesNotExist:
            raise status.HTTP_400_BAD_REQUEST

    def get(self, request, pk):
        delivery_crew = self.get_object(pk)
        serializer = DeliveryCrewSerializer(delivery_crew)
        return Response(serializer.data)

    def put(self, request, pk):
        delivery_crew = self.get_object(pk)
        serializer = DeliveryCrewSerializer(delivery_crew, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        delivery_crew = self.get_object(pk)
        delivery_crew.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)