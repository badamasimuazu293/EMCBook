from django.contrib import admin
from .models import User, Doctor, Patient, Appointment, Availability, MedicalRecord

# user admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'role', 'is_staff')
    list_filter = ('role', 'is_staff')
    search_fields = ('username', 'email')

admin.site.register(User, UserAdmin)

# docter admin
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialty', 'department')
    search_fields = ('user__username', 'specialty')

admin.site.register(Doctor, DoctorAdmin)

# patient admin
class PatientAdmin(admin.ModelAdmin):
    list_display = ('user', 'date_of_birth')
    search_fields = ('user__username',)

admin.site.register(Patient, PatientAdmin)

# appointment admin
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'date', 'time', 'status')
    list_filter = ('status', 'date')
    search_fields = ('patient__user__username', 'doctor__user__username')

admin.site.register(Appointment, AppointmentAdmin)

# availability admin
class AvailabilityAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'date', 'start_time', 'end_time', 'is_available')
    list_filter = ('date', 'is_available')

admin.site.register(Availability, AvailabilityAdmin)

# medical record admin
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'created_at')

admin.site.register(MedicalRecord, MedicalRecordAdmin)