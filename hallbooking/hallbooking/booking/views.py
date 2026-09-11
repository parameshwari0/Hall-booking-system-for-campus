from django.shortcuts import (render, redirect,
                               get_object_or_404)
from django.contrib.auth import login, logout
from django.contrib.auth.forms import (
    AuthenticationForm)
from django.contrib.auth.decorators import (
    login_required)
from django.contrib import messages
from .models import Hall, Booking
from .forms import BookingForm, RegisterForm


def home(request):
    return redirect('login')


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(
            request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('book')
    else:
        form = AuthenticationForm()
    return render(request,
                 'booking/login.html',
                 {'form': form})


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            logout(request)
            login(request, user)
            messages.success(request,
                f'Welcome {user.username}! '
                f'Registration Successful.')
            return redirect('book')
    else:
        form = RegisterForm()
    return render(request,
                 'booking/register.html',
                 {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')


@login_required
def book_hall(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user

            # Check for conflicts
            conflicting = Booking.objects.filter(
                hall=booking.hall,
                date=booking.date,
                status='active'
            ).exclude(
                end_time__lte=booking.start_time
            ).exclude(
                start_time__gte=booking.end_time
            )

            if conflicting.exists():
                # Add to pending list
                booking.status = 'pending'
                booking.save()
                messages.warning(request,
                    f'⚠️ {booking.hall} is already '
                    f'booked at this time. '
                    f'You have been added to '
                    f'the waiting list!')
                return redirect('my_bookings')

            # No conflict - book directly
            booking.status = 'active'
            booking.save()
            messages.success(request,
                '✅ Hall booked successfully!')
            return redirect('my_bookings')
    else:
        form = BookingForm()
    return render(request,
                 'booking/book.html',
                 {'form': form})


@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(
        user=request.user)
    return render(request,
                 'booking/my_bookings.html',
                 {'bookings': bookings})


@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(
        Booking,
        id=booking_id,
        user=request.user)

    if request.method == 'POST':
        booking.status = 'cancelled'
        booking.save()
        messages.success(request,
            '✅ Booking cancelled successfully!')

    return redirect('my_bookings')