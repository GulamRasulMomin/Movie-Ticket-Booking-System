"""
URL configuration for book_my_show project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from movie_booking import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', views.signup, name='signup'),
    path('', views.login, name='login'),
    path('home/', views.home, name='home'),
    path('cinemas/', views.cinemas, name='cinemas'),
    path('cinemas_movie/<int:cinema_id>/', views.cinemas_movie, name='cinemas_movie'),
    path('book/<int:cinema_id>/<int:movie_id>/', views.book, name='book'),
    path('sitmatrix/<int:cinema_id>/<int:movie_id>/<str:date>/<str:time>/', views.sitmatrix, name='sitmatrix'),
    path('sitmatrix/<int:cinema_id>/<int:movie_id>/', views.sitmatrix, name='sitmatrix'),    
    path('ticket/', views.ticket, name='ticket'),
    path('booking_history/', views.booking_history, name='booking_history'),
    path('profile/', views.profile, name='profile'),
]
