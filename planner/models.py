from django.db import models
from django.contrib.auth.models import User


# PROFILE MODEL
class Profile(models.Model):

    ROLE_CHOICES = (
        ('traveler', 'Traveler'),
        ('staff', 'Staff'),
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES
    )

    phone = models.CharField(
        max_length=15,
        blank=True
    )

    place = models.CharField(
        max_length=100,
        blank=True
    )

    def __str__(self):
        return self.user.username


# DESTINATION MODEL
class Destination(models.Model):

    name = models.CharField(max_length=100)

    country = models.CharField(max_length=100)

    description = models.TextField()

    best_time_to_visit = models.CharField(max_length=100)

    # GOOGLE MAP LINK
    google_map_link = models.URLField(
        blank=True,
        null=True
    )

    image = models.ImageField(
        upload_to='destinations/',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name


# TRIP MODEL
class Trip(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    destination = models.ForeignKey(
        Destination,
        on_delete=models.CASCADE
    )

    start_date = models.DateField()

    end_date = models.DateField()

    budget = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):
        return f"{self.user.username} - {self.destination.name}"


# ITINERARY MODEL
class Itinerary(models.Model):

    trip = models.ForeignKey(
        Trip,
        on_delete=models.CASCADE
    )

    day = models.IntegerField()

    activity = models.CharField(max_length=200)

    location = models.CharField(max_length=150)

    time = models.TimeField()

    def __str__(self):
        return f"Day {self.day} - {self.activity}"


# BOOKING OPTION MODEL
class BookingOption(models.Model):

    trip = models.ForeignKey(
        Trip,
        on_delete=models.CASCADE
    )

    booking_type = models.CharField(max_length=50)

    provider = models.CharField(max_length=100)

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    link = models.URLField()

    def __str__(self):
        return self.provider


# TRAVEL UPDATE MODEL
class TravelUpdate(models.Model):

    destination = models.ForeignKey(
        Destination,
        on_delete=models.CASCADE
    )

    title = models.CharField(max_length=150)

    update_text = models.TextField()

    date_posted = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title


# REVIEW MODEL
class Review(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    destination = models.ForeignKey(
        Destination,
        on_delete=models.CASCADE
    )

    rating = models.IntegerField()

    comment = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.user.username} - {self.destination.name}"


# TRAVEL BOOKING MODEL
class TravelBooking(models.Model):

    HOTEL_CHOICES = (
        ('standard', 'Standard'),
        ('deluxe', 'Deluxe'),
        ('premium', 'Premium'),
    )

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    destination = models.ForeignKey(
        Destination,
        on_delete=models.CASCADE
    )

    travel_date = models.DateField()

    travelers = models.IntegerField()

    hotel_type = models.CharField(
        max_length=20,
        choices=HOTEL_CHOICES
    )

    special_request = models.TextField(
        blank=True,
        null=True
    )

    booking_status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.user.username} - {self.destination.name}"
    
# PAYMENT MODEL
class Payment(models.Model):

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    booking = models.ForeignKey(
        TravelBooking,
        on_delete=models.CASCADE
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    payment_method = models.CharField(
        max_length=100
    )

    payment_status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    paid_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.user.username} - ₹{self.amount}"