from django.db import models
from django.contrib.auth.models import User

class Hall(models.Model):
    name = models.CharField(max_length=100)
    capacity = models.IntegerField()
    location = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Booking(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('cancelled', 'Cancelled'),
        ('pending', 'Pending'),
    ]
    user = models.ForeignKey(
        User, on_delete=models.CASCADE)
    hall = models.ForeignKey(
        Hall, on_delete=models.CASCADE)
    department = models.CharField(max_length=200)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    purpose = models.CharField(max_length=300)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='active'
    )
    created_at = models.DateTimeField(
        auto_now_add=True)

    def __str__(self):
        return (f"{self.user} | {self.hall} | "
                f"{self.date} | {self.status}")

class PendingBooking(Booking):
    class Meta:
        proxy = True
        verbose_name = 'Pending Booking'
        verbose_name_plural = 'Pending Bookings'

class CancelledBooking(Booking):
    class Meta:
        proxy = True
        verbose_name = 'Cancelled Booking'
        verbose_name_plural = 'Cancelled Bookings'