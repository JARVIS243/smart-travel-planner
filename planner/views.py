from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from reportlab.pdfgen import canvas


from .models import (
    Profile,
    Destination,
    Review,
    Trip,
    Itinerary,
    BookingOption,
    TravelUpdate,
    TravelBooking,
    Payment
)


def home(request):
    destinations = Destination.objects.all()[:3]
    return render(request, 'home.html', {'destinations': destinations})


def signup_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        place = request.POST.get('place')
        role = request.POST.get('role')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('signup')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        Profile.objects.create(
            user=user,
            role=role,
            phone=phone,
            place=place
        )

        messages.success(request, "Account created successfully. Please login.")
        return redirect('login')

    return render(request, 'signup.html')


def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('dashboard')

        messages.error(request, "Invalid username or password")
        return redirect('login')

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard(request):

    profile, created = Profile.objects.get_or_create(
        user=request.user,
        defaults={
            'role': 'traveler',
            'phone': '',
            'place': ''
        }
    )

    trips = Trip.objects.filter(user=request.user)

    return render(request, 'dashboard.html', {
        'profile': profile,
        'trips': trips
    })


def destinations(request):
    destinations = Destination.objects.all()
    return render(request, 'destinations.html', {'destinations': destinations})


@login_required
def itinerary(request):
    itineraries = Itinerary.objects.filter(trip__user=request.user)
    return render(request, 'itinerary.html', {'itineraries': itineraries})


@login_required
def bookings(request):
    bookings = BookingOption.objects.filter(trip__user=request.user)
    return render(request, 'bookings.html', {'bookings': bookings})


def updates(request):
    updates = TravelUpdate.objects.all().order_by('-date_posted')
    return render(request, 'updates.html', {'updates': updates})

@login_required
def reviews(request):

    reviews = Review.objects.all().order_by('-created_at')

    destinations = Destination.objects.all()

    if request.method == "POST":

        destination_id = request.POST.get('destination')

        rating = request.POST.get('rating')

        comment = request.POST.get('comment')

        destination = Destination.objects.get(id=destination_id)

        Review.objects.create(
            user=request.user,
            destination=destination,
            rating=rating,
            comment=comment
        )

        messages.success(request, "Review added successfully")

        return redirect('reviews')

    return render(request, 'reviews.html', {
        'reviews': reviews,
        'destinations': destinations
    })

@login_required
def create_booking(request):

    destinations = Destination.objects.all()

    if request.method == "POST":

        destination_id = request.POST.get('destination')

        travel_date = request.POST.get('travel_date')

        travelers = request.POST.get('travelers')

        hotel_type = request.POST.get('hotel_type')

        special_request = request.POST.get('special_request')

        destination = Destination.objects.get(id=destination_id)

        TravelBooking.objects.create(
            user=request.user,
            destination=destination,
            travel_date=travel_date,
            travelers=travelers,
            hotel_type=hotel_type,
            special_request=special_request
        )

        messages.success(request, "Booking created successfully")

        return redirect('my_bookings')

    return render(request, 'create_booking.html', {
        'destinations': destinations
    })


@login_required
def my_bookings(request):

    bookings = TravelBooking.objects.filter(
        user=request.user
    ).order_by('-created_at')

    return render(request, 'my_bookings.html', {
        'bookings': bookings
    })

@login_required
def analytics(request):

    total_trips = Trip.objects.filter(
        user=request.user
    ).count()

    total_bookings = TravelBooking.objects.filter(
        user=request.user
    ).count()

    total_reviews = Review.objects.filter(
        user=request.user
    ).count()

    pending_bookings = TravelBooking.objects.filter(
        user=request.user,
        booking_status='pending'
    ).count()

    confirmed_bookings = TravelBooking.objects.filter(
        user=request.user,
        booking_status='confirmed'
    ).count()

    return render(request, 'analytics.html', {

        'total_trips': total_trips,
        'total_bookings': total_bookings,
        'total_reviews': total_reviews,
        'pending_bookings': pending_bookings,
        'confirmed_bookings': confirmed_bookings,

    })

@login_required
def download_pdf(request):

    response = HttpResponse(
        content_type='application/pdf'
    )

    response['Content-Disposition'] = (
        'attachment; filename="travel_booking_report.pdf"'
    )

    p = canvas.Canvas(response)

    p.setFont("Helvetica-Bold", 24)
    p.drawString(145, 800, "Smart Travel Planner")

    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, 760, "Booking Report")

    p.setFont("Helvetica", 13)
    p.drawString(50, 735, f"User: {request.user.username}")

    bookings = TravelBooking.objects.filter(
        user=request.user
    ).order_by('-created_at')

    y = 700

    if not bookings:

        p.setFont("Helvetica-Bold", 15)
        p.drawString(50, y, "No booking details found.")

    else:

        for booking in bookings:

            if y < 140:
                p.showPage()
                y = 800

            p.setFont("Helvetica-Bold", 15)
            p.drawString(50, y, f"Destination: {booking.destination.name}")

            y -= 25

            p.setFont("Helvetica", 12)
            p.drawString(70, y, f"Country: {booking.destination.country}")

            y -= 20
            p.drawString(70, y, f"Travel Date: {booking.travel_date}")

            y -= 20
            p.drawString(70, y, f"Travelers: {booking.travelers}")

            y -= 20
            p.drawString(70, y, f"Hotel Type: {booking.hotel_type}")

            y -= 20
            p.drawString(70, y, f"Booking Status: {booking.booking_status}")

            y -= 20
            p.drawString(70, y, f"Created At: {booking.created_at.strftime('%Y-%m-%d %H:%M')}")

            y -= 35
            p.line(50, y, 550, y)

            y -= 30

    p.save()

    return response

@login_required
def ai_trip_planner(request):

    trip_plan = None

    if request.method == "POST":

        destination = request.POST.get('destination')

        budget = request.POST.get('budget')

        days = request.POST.get('days')

        interests = request.POST.get('interests')

        # SIMPLE AI RESPONSE
        trip_plan = f"""
        AI Recommended Trip Plan

        Destination:
        {destination}

        Duration:
        {days} Days

        Budget:
        ₹{budget}

        Interests:
        {interests}

        Suggested Activities:
        • Explore famous tourist attractions
        • Try local food experiences
        • Visit cultural landmarks
        • Enjoy adventure activities
        • Capture travel photography
        • Explore nightlife and shopping

        Recommended Hotel:
        Premium Resort

        Travel Tip:
        Carry essential travel documents and enjoy your trip.
        """

    return render(request, 'ai_planner.html', {
        'trip_plan': trip_plan
    })

@login_required
def payment_page(request, booking_id):

    booking = TravelBooking.objects.get(
        id=booking_id
    )

    amount = booking.travelers * 5000

    # PAYMENT SUBMIT
    if request.method == "POST":

        payment_method = request.POST.get(
            'payment_method'
        )

        # SAVE PAYMENT
        Payment.objects.create(

            user=request.user,

            booking=booking,

            amount=amount,

            payment_method=payment_method,

            payment_status='paid'

        )

        # UPDATE BOOKING STATUS
        booking.booking_status = 'confirmed'

        booking.save()

        # SUCCESS MESSAGE
        messages.success(
            request,
            "Payment completed successfully!"
        )

        return redirect('my_bookings')

    return render(request, 'payment.html', {

        'booking': booking,

        'amount': amount

    })