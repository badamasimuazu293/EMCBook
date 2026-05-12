from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('doctor-dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),

    path('search/', views.search_doctor, name='search_doctor'),
    path('book/<int:doctor_id>/', views.book_appointment, name='book'),

    path('history/', views.booking_history, name='booking_history'),
    path('cancel/<int:appointment_id>/', views.cancel_appointment, name='cancel'),

    path('availability/', views.manage_availability, name='availability'),
    path('update-status/<int:appointment_id>/', views.update_status, name='update_status'),

    path('doctor-profile/', views.doctor_profile, name='doctor_profile'),
]