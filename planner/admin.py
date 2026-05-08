from django.contrib import admin

from .models import (
    Profile,
    Destination,
    Trip,
    Itinerary,
    BookingOption,
    TravelUpdate,
    Review,
    TravelBooking,
    Payment
)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'role',
        'phone',
        'place'
    )

    search_fields = (
        'user__username',
        'role'
    )


@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'country',
        'best_time_to_visit'
    )

    search_fields = (
        'name',
        'country'
    )


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'destination',
        'start_date',
        'end_date',
        'budget'
    )

    search_fields = (
        'user__username',
        'destination__name'
    )


@admin.register(Itinerary)
class ItineraryAdmin(admin.ModelAdmin):

    list_display = (
        'trip',
        'day',
        'activity',
        'location',
        'time'
    )


@admin.register(BookingOption)
class BookingOptionAdmin(admin.ModelAdmin):

    list_display = (
        'trip',
        'booking_type',
        'provider',
        'price'
    )


@admin.register(TravelUpdate)
class TravelUpdateAdmin(admin.ModelAdmin):

    list_display = (
        'destination',
        'title',
        'date_posted'
    )

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'destination',
        'rating',
        'created_at'
    )

@admin.register(TravelBooking)
class TravelBookingAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'destination',
        'travel_date',
        'travelers',
        'hotel_type',
        'booking_status'
    )

    list_filter = (
        'booking_status',
        'hotel_type'
    )

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'booking',
        'amount',
        'payment_method',
        'payment_status'
    )