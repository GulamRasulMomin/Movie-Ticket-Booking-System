from django.contrib import admin
from movie_booking.models import my_user, Cinema, Movie, Screening, Booking
# Register your models here.

admin.site.register(my_user)
admin.site.register(Cinema)
admin.site.register(Movie)
admin.site.register(Screening)
admin.site.register(Booking)