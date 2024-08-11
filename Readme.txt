API Endpoints
-------------

1. Booking:
   - List all bookings and create new bookings:
     GET /api/bookings/
     POST /api/bookings/

   - Retrieve, update, and delete a specific booking:
     GET /api/bookings/<booking_id>/
     PUT /api/bookings/<booking_id>/
     DELETE /api/bookings/<booking_id>/

2. Registration:
   - Register a new user:
     POST /api/registration/

3. Menu:
   - List all menus and create new menu items:
     GET /api/user/menu/
     POST /api/user/menu/

   - Retrieve, update, and delete a specific menu item:
     GET /api/user/menu/<menu_id>/
     PUT /api/user/menu/<menu_id>/
     DELETE /api/user/menu/<menu_id>/

4. Type (Category):
   - List all types and create new types:
     GET /api/master/types/
     POST /api/master/types/

   - Retrieve, update, and delete a specific type:
     GET /api/master/types/<type_id>/
     PUT /api/master/types/<type_id>/
     DELETE /api/master/types/<type_id>/

5. Cart Item:
   - List all cart items and create new cart items:
     GET /api/master/cart-items/
     POST /api/master/cart-items/

   - Retrieve, update, and delete a specific cart item:
     GET /api/master/cart-items/<cart_item_id>/
     PUT /api/master/cart-items/<cart_item_id>/
     DELETE /api/master/cart-items/<cart_item_id>/

6. Delivery Crew:
   - List all delivery crews and create new delivery crews:
     GET /api/master/delivery-crews/
     POST /api/master/delivery-crews/

   - Retrieve, update, and delete a specific delivery crew:
     GET /api/master/delivery-crews/<delivery_crew_id>/
     PUT /api/master/delivery-crews/<delivery_crew_id>/
     DELETE /api/master/delivery-crews/<delivery_crew_id>/
