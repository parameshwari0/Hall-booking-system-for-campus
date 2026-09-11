from django.contrib import admin
from .models import Hall, Booking, PendingBooking, CancelledBooking

admin.site.site_header = (
    'Campus Hall Booking Administration')
admin.site.site_title = 'Hall Booking Admin'
admin.site.index_title = 'Administration'
admin.site.site_url = (
    'http://127.0.0.1:8000/login/')

class HallAdmin(admin.ModelAdmin):
    list_display = ['name', 'capacity', 'location']

class BookingAdmin(admin.ModelAdmin):
    list_display = ['user', 'hall', 'department',
                    'date', 'start_time',
                    'end_time', 'purpose',
                    'status', 'created_at']
    list_filter = ['hall', 'date']
    search_fields = ['user__username',
                     'hall__name', 'department']

    def get_queryset(self, request):
        # Show ONLY active bookings
        return super().get_queryset(
            request).filter(status='active')

class PendingBookingAdmin(admin.ModelAdmin):
    list_display = ['user', 'hall', 'department',
                    'date', 'start_time',
                    'end_time', 'purpose',
                    'created_at']
    search_fields = ['user__username',
                     'hall__name', 'department']

    def get_queryset(self, request):
        # Show ONLY pending bookings
        return super().get_queryset(
            request).filter(status='pending')

class CancelledBookingAdmin(admin.ModelAdmin):
    list_display = ['user', 'hall', 'department',
                    'date', 'start_time',
                    'end_time', 'purpose',
                    'created_at']
    search_fields = ['user__username',
                     'hall__name', 'department']
    list_filter = ['hall', 'date']

    def get_queryset(self, request):
        # Show ONLY cancelled bookings
        return super().get_queryset(
            request).filter(status='cancelled')

admin.site.register(Hall, HallAdmin)
admin.site.register(Booking, BookingAdmin)
admin.site.register(PendingBooking,
                    PendingBookingAdmin)
admin.site.register(CancelledBooking,
                    CancelledBookingAdmin)