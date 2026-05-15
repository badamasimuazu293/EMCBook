from django.db import models
from django.contrib.auth.models import AbstractUser

# custom user model
class User(AbstractUser):
    ROLE_CHOICES = (
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
        ('admin', 'Admin'),
    )

    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    phone = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.username
    # docter model
class Doctor(models.Model):

    SPECIALTY_CHOICES = [
        ('cardiology', 'Cardiology'),
        ('neurology', 'Neurology'),
        ('dermatology', 'Dermatology'),
        ('pediatrics', 'Pediatrics'),
        ('orthopedics', 'Orthopedics'),
    ]

    DEPARTMENT_CHOICES = [
        ('general', 'General'),
        ('emergency', 'Emergency'),
        ('surgery', 'Surgery'),
        ('outpatient', 'Outpatient'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialty = models.CharField(max_length=50, choices=SPECIALTY_CHOICES)
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Dr. {self.user.username}"

    # patients model
class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.user.username
    # availability
class Availability(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.doctor} - {self.date}"
    # appointment
class Appointment(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient} -> {self.doctor} ({self.date})"
    # medical records
class MedicalRecord(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    notes = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Record for {self.patient}"
def create_superuser(self, username, email=None, password=None, **extra_fields):
    extra_fields.setdefault('is_staff', True)
    extra_fields.setdefault('is_superuser', True)
    extra_fields.setdefault('is_active', True)

    return self.create_user(username, email, password, **extra_fields)
