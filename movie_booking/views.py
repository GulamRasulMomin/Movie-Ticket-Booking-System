# views.py
from movie_booking.models import my_user, Cinema, Movie, Screening, Booking
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
import re

# Create your views here.

def home(request):
    email = request.session.get('email', None)
    user = my_user.objects.filter(email=request.session.get('email')).first()
    my_movie = Movie.objects.all()
    return render(request, 'home.html',{'my_movie': my_movie, 'email': email, 'user' : user})

def signup(request):
    error = None

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['password']
        confirmpassword = request.POST['confirmpassword']
        
        if not validate_username(username):
            error = 'Invalid username'
            return render(request, 'signup.html',{'error': error})
        
        if not validate_email(email):
            error = 'Invalid email'
            return render(request, 'signup.html',{'error': error})
        
        if not validate_phone(phone):
            error = 'Invalid phone number'
            return render(request, 'signup.html',{'error': error})
        
        if not validate_password(password):
            error = 'Password must contain at least 8 characters, one uppercase, one lowercase, one number and one special character'
            return render(request, 'signup.html',{'error': error})

        if password!=confirmpassword:
            return render(request, 'signup.html', {'error': 'Confirm password do not match'})
        
        if my_user.objects.filter(email=email).exists():
            return render(request, 'signup.html', {'error': 'user already exists'})
        else:
            user = my_user(username=username, phone=phone, email=email, password=password)
            user.save()
            request.session['email'] = email  # Store email in session
            return redirect('home')
    return render(request, 'signup.html')

def login(request):
    error = None
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = my_user.objects.filter(email=email, password=password)
        if user.exists():
            request.session['email'] = email  # Store email in session
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Invalid email or password'})
    return render(request, 'login.html')

def cinemas(request):
    cinemas = Cinema.objects.all()
    return render(request, 'cinemas.html', {'cinemas': cinemas})

def cinemas_movie(request, cinema_id):
    cinema = get_object_or_404(Cinema, pk=cinema_id)
    my_movie = Movie.objects.all()
    return render(request, 'cinemas_movie.html', {'cinema': cinema, 'my_movie' : my_movie})

def book(request, cinema_id, movie_id):
    cinema = get_object_or_404(Cinema, pk=cinema_id)
    movie = get_object_or_404(Movie, pk=movie_id)
    return render(request, 'book.html', {'cinema': cinema, 'movie': movie})

def sitmatrix(request, cinema_id, movie_id, date='12-3-2025-friday', time='11:00'):
    cinema = get_object_or_404(Cinema, pk=cinema_id)
    movie = get_object_or_404(Movie, pk=movie_id)
    user = my_user.objects.filter(email=request.session.get('email')).first()
    screening = Screening.objects.filter(cinema=cinema, movie=movie, date=date, time=time).first()
    seats = screening.booked_seats if screening else []
    total_seats = [i for i in range(screening.total_seats if screening else 100)]

    if request.method == 'POST':
        selected_seats = request.POST.getlist('tickets')

        if len(selected_seats) == 0:
            return render(request, 'sitmatrix.html', {'cinema': cinema, 'movie': movie, 'seats': list(map(lambda x: int(x), seats)), 'total_seats': total_seats, 'date' : date, 'time' : time})
        
        if screening:
            screening.booked_seats.extend(selected_seats)
            screening.save()
            user_booking = Booking(user=user, screening=screening, seats=selected_seats, total_price=len(selected_seats)*100)
            user_booking.save()
        else :
            book_screening = Screening(movie=movie, cinema=cinema, date=date, time=time, total_seats=100, booked_seats=selected_seats)
            book_screening.save()
            user_booking = Booking(user=user, screening=book_screening, seats=selected_seats, total_price=len(selected_seats)*100)
            user_booking.save()
        return render(request, 'ticket.html', {'booking': user_booking})       

    return render(request, 'sitmatrix.html', {'cinema': cinema, 'movie': movie, 'seats': list(map(lambda x: int(x), seats)), 'total_seats': total_seats, 'date' : date, 'time' : time})

def ticket(request):
    return render(request, 'ticket.html')

def booking_history(request):
    user = my_user.objects.filter(email=request.session.get('email')).first()
    bookings = Booking.objects.filter(user=user)
    return render(request, 'booking_history.html', {'bookings': bookings})

def profile(request):
    user = my_user.objects.filter(email=request.session.get('email')).first()    
    return render(request, 'profile.html', {'user': user})


def validate_email(email):
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return bool(re.match(pattern, email))

def validate_username(username):
    pattern = r'^[a-zA-Z0-9_ ]{3,20}$'
    return bool(re.match(pattern, username))

def validate_phone(phone):
    pattern = r'^(\+\d{1,3})?\d{10}$' 
    return bool(re.match(pattern, phone))

def validate_password(password):
    pattern = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
    return bool(re.match(pattern, password))