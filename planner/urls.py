from django.urls import path
from . import views


urlpatterns = [

    # HOME
    path(
        '',
        views.home,
        name='home'
    ),

    # SIGNUP
    path(
        'signup/',
        views.signup_view,
        name='signup'
    ),

    # LOGIN
    path(
        'login/',
        views.login_view,
        name='login'
    ),

    # LOGOUT
    path(
        'logout/',
        views.logout_view,
        name='logout'
    ),

    # DASHBOARD
    path(
        'dashboard/',
        views.dashboard,
        name='dashboard'
    ),

    # DESTINATIONS
    path(
        'destinations/',
        views.destinations,
        name='destinations'
    ),

    # ITINERARY
    path(
        'itinerary/',
        views.itinerary,
        name='itinerary'
    ),

    # BOOKINGS
    path(
        'bookings/',
        views.bookings,
        name='bookings'
    ),

    # TRAVEL UPDATES
    path(
        'updates/',
        views.updates,
        name='updates'
    ),

    path(
        'reviews/',
        views.reviews,
        name='reviews'
    ),

    path(
        'create-booking/',
        views.create_booking,
        name='create_booking'
    ),

    path(
        'my-bookings/',
        views.my_bookings,
        name='my_bookings'
    ),

    path(
        'analytics/',
        views.analytics,
        name='analytics'
    ),

    path(
        'download-pdf/',
        views.download_pdf,
        name='download_pdf'
    ),

    path(
        'ai-trip-planner/',
        views.ai_trip_planner,
        name='ai_trip_planner'
    ),

    path(
        'payment/<int:booking_id>/',
        views.payment_page,
        name='payment_page'
    ),
]