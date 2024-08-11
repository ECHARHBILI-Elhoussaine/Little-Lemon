from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .swagger import schema_view


urlpatterns = [
    path('', views.home, name="home"),
    path('about/', views.about, name="about"),
    path('book/', views.book, name="book"),
    path('menu/', views.menu, name="menu"),
    path('menu_item/<int:id>/', views.menu_detail, name='menu_detail'),
    path('reservations/', views.reservations, name='reservations'),
    # Add the remaining URL path configurations here

    #api for register, api for login to get token
    path('api/register/', views.UserRegistration.as_view(), name='user-registration'),
    path('api/login/', views.UserLogin.as_view(), name='user-login'),

    #api need authentication

    #Get menu with pagination, post menu
    path('api/user/menu/', views.MenuList.as_view(), name='menu-list'),  # For listing all menus and creating new menu items
    #get detail menu by id, update menu by id, delete menu by id
    path('api/user/menu/<int:pk>/', views.MenuDetail.as_view(), name='menu-detail'),  # For retrieving, updating, and deleting a specific menu item

    #api get type (category) with pagination, register type
    path('api/master/types/', views.TypeList.as_view(), name='type-list'),
    #api get detail by id, update by id, delete by id
    path('api/master/types/<int:pk>/', views.TypeDetail.as_view(), name='type-detail'),

    #api get cart item with pagination, add cart item
    path('api/master/cart-items/', views.CartItemList.as_view(), name='cart-item-list'),
    #api get cart by id, update cart by id, delete cart by id
    path('api/master/cart-items/<int:pk>/', views.CartItemDetail.as_view(), name='cart-item-detail'),
    
    #api get all delivery crew, register
    path('api/master/delivery-crews/', views.DeliveryCrewList.as_view(), name='delivery-crew-list'),
    #api get detail delivery, update status delivery, delete by id
    path('api/master/delivery-crews/<int:pk>/', views.DeliveryCrewDetail.as_view(), name='delivery-crew-detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)