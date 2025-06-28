from django.db import models

# Create your models here.
class my_user(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=10)
    password = models.CharField(max_length=10)

    def __str__(self):
        return self.username
    
# Cinema Model
class Cinema(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    cinema_poster = models.ImageField(upload_to='static/images/', null=True, blank=True)

    def __str__(self):
        return self.name

# Movie Model
class Movie(models.Model):
    title = models.CharField(max_length=255)
    genre = models.CharField(max_length=255)
    movie_poster = models.ImageField(upload_to='static/images/', null=True, blank=True)
    trailer = models.CharField(max_length=255)

    def __str__(self):
        return self.title

# Screening Model (Movie Shows)
class Screening(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE)
    date = models.CharField(max_length=255)
    time = models.CharField(max_length=255)
    total_seats = models.IntegerField(default=100)
    booked_seats = models.JSONField(default=list)

    def available_seats(self):
        return self.total_seats - len(self.booked_seats)

    def __str__(self):
        return f"{self.movie.title} at {self.cinema.name} on {self.date} at {self.time}"

# Booking Model
class Booking(models.Model):
    user = models.ForeignKey(my_user, on_delete=models.CASCADE)
    screening = models.ForeignKey(Screening, on_delete=models.CASCADE)
    seats = models.JSONField()
    total_price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.user.username} - {self.screening.movie.title} ({len(self.seats)} seats)"

