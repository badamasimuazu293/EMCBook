from django.shortcuts import render, redirect, get_object_or_404,
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages,
from .models import User, Doctor, Patient, Appointment, Availability
from django.utils import timezone
from django.http import HttpResponse
# register view
# def register_view(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         role = request.POST['role']

#         user = User.objects.create_user(username=username, password=password, role=role)

#         if role == 'patient':
#             Patient.objects.create(user=user)
#         elif role == 'doctor':
#             Doctor.objects.create(user=user)

#         messages.success(request, "Account created successfully")
#         return redirect('login')

#     return render(request, 'register.html')
# # 
import traceback

def register_view(request):
    try:
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']

            user = User.objects.create_user(
                username=username,
                password=password
            )

            return redirect('login')

    except Exception as e:
        return HttpResponse(f"ERROR: {str(e)} <br><br> {traceback.format_exc()}")
# login view
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid credentials")

    return render(request, 'login.html')
# logout view
@login_required
def logout_view(request):
    logout(request)
    return redirect('login')
# dashbord view role based
@login_required
def dashboard(request):
    if request.user.role == 'patient':
        return render(request, 'patient/dashboard.html')
    elif request.user.role == 'doctor':
        return redirect('doctor_dashboard')
    else:
        return render(request, 'admin/dashboard.html')
# doctor dashboard
@login_required
def doctor_dashboard(request):
    
    doctor = Doctor.objects.get(user=request.user)
    

    appointments = Appointment.objects.filter(doctor=doctor).order_by('-date')

    total = appointments.count()
    pending = appointments.filter(status='pending').count()
    completed = appointments.filter(status='completed').count()

    context = {
        'appointments': appointments,
        'total': total,
        'pending': pending,
        'completed': completed,
        'doctor': doctor,
        'specialties': Doctor.SPECIALTY_CHOICES,
        'departments': Doctor.DEPARTMENT_CHOICES
}
    

    return render(request, 'doctor/dashboard.html', context)
# admin dashboard
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import User, Doctor, Patient, Appointment

@login_required
def admin_dashboard(request):
    if request.user.role != 'admin':
        return render(request, '403.html')  # optional security page

    users_count = User.objects.count()
    doctors_count = Doctor.objects.count()
    patients_count = Patient.objects.count()
    appointments_count = Appointment.objects.count()

    recent_appointments = Appointment.objects.all().order_by('-date')[:10]

    context = {
        'users_count': users_count,
        'doctors_count': doctors_count,
        'patients_count': patients_count,
        'appointments_count': appointments_count,
        'recent_appointments': recent_appointments
    }

    return render(request, 'admin/dashboard.html', context)
    # search doctor view
@login_required
def search_doctor(request):
    doctors = Doctor.objects.all()

    specialty = request.GET.get('specialty')
    if specialty:
        doctors = doctors.filter(specialty__icontains=specialty)

    return render(request, 'patient/search.html', {'doctors': doctors})
# book appointment view
@login_required
def book_appointment(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    patient = Patient.objects.get(user=request.user)

    if request.method == 'POST':
        date = request.POST['date']
        time = request.POST['time']

        # 🚫 Prevent double booking
        exists = Appointment.objects.filter(
            doctor=doctor,
            date=date,
            time=time
        ).exists()

        if exists:
            messages.error(request, "Slot already booked!")
            return redirect('search_doctor')

        Appointment.objects.create(
            patient=patient,
            doctor=doctor,
            date=date,
            time=time
        )

        messages.success(request, "Appointment booked successfully!")
        return redirect('booking_history')

    return render(request, 'patient/book.html', {'doctor': doctor})
# booking history view
@login_required
def booking_history(request):
    patient = Patient.objects.get(user=request.user)
    appointments = Appointment.objects.filter(patient=patient)

    return render(request, 'patient/history.html', {'appointments': appointments})
# cancel appointment view
@login_required
def cancel_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)

    if appointment.patient.user != request.user:
        messages.error(request, "Unauthorized action")
        return redirect('dashboard')

    appointment.status = 'cancelled'
    appointment.save()

    messages.success(request, "Appointment cancelled")
    return redirect('booking_history')
# docter manage avilability
@login_required
def manage_availability(request):
    doctor = Doctor.objects.get(user=request.user)

    if request.method == 'POST':
        date = request.POST['date']
        start = request.POST['start_time']
        end = request.POST['end_time']

        Availability.objects.create(
            doctor=doctor,
            date=date,
            start_time=start,
            end_time=end
        )

        messages.success(request, "Availability added")

    availability = Availability.objects.filter(doctor=doctor)
    return render(request, 'doctor/availability.html', {'availability': availability})
# docter update appointment
@login_required
def update_status(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)

    status = request.POST.get('status')
    appointment.status = status
    appointment.save()

    return redirect('dashboard')
# doctor prfile
def doctor_profile(request):
    doctor = Doctor.objects.get(user=request.user)

    specialties = ["Cardiology", "Neurology", "Dermatology", "Pediatrics", "Orthopedics"]
    departments = ["Outpatient", "Emergency", "Surgery", "Radiology"]

    if request.method == 'POST':
        doctor.specialty = request.POST['specialty']
        doctor.department = request.POST['department']
        doctor.bio = request.POST.get('bio')
        doctor.save()

        messages.success(request, "Profile updated successfully!")
        return redirect('doctor_dashboard')

    return render(request, 'doctor/profile.html', {
        'doctor': doctor,
        'specialties': specialties,
        'departments': departments
    })