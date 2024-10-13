from django.contrib.auth.models import AbstractUser, User
from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.conf import settings

# Extender el modelo de usuario predeterminado de Django
class CustomUser(AbstractUser):
    # Definir los tipos de usuarios
    USER_TYPE_CHOICES = (
        ('company', 'Empresa'),  # Opción para empresas
        ('intern', 'Becario'),   # Opción para becarios
    )
    # Campo para almacenar el tipo de usuario (empresa o becario)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)

    # Campos específicos para la empresa
    company_name = models.CharField(max_length=255, blank=True, null=True)
    sector = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)

    # Campos específicos que forman parte del perfil (CV) del becario
    education = models.TextField(blank=True, null=True)  # Campo para educación
    work_experience = models.TextField(blank=True, null=True)  # Campo para experiencia laboral
    skills = models.TextField(blank=True, null=True)  # Campo para habilidades
    languages = models.TextField(blank=True, null=True)  # Campo para idiomas
    certifications = models.TextField(blank=True, null=True)  # Campo para certificaciones

    # Campo para almacenar el código de restablecimiento de contraseña
    password_reset_code = models.CharField(max_length=6, blank=True, null=True)

    # Campo para la fecha de expiración del código de restablecimiento
    password_reset_code_expiration = models.DateTimeField(blank=True, null=True)

    # Método para generar un código de restablecimiento de contraseña y asignarlo al usuario
    def set_password_reset_code(self):
        import random
        code = ''.join(random.choices('0123456789', k=6))  # Generar un código de 6 dígitos
        self.password_reset_code = code
        self.password_reset_code_expiration = timezone.now() + timedelta(minutes=10)
        self.save()

    # Método para validar si el código es válido y no ha expirado
    def is_password_reset_code_valid(self, code):
        if self.password_reset_code == code and timezone.now() < self.password_reset_code_expiration:
            return True
        return False

#guardar la información de los trabajos
class JobPosting(models.Model):
    title = models.CharField(max_length=255)
    company = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'user_type': 'company'})
    description = models.TextField()
    requirements = models.TextField()
    location = models.CharField(max_length=255, null=True, blank=True)  # Agregar campo 'location'
    created_at = models.DateTimeField(auto_now_add=True)

class JobApplication(models.Model):
    job = models.ForeignKey(JobPosting, on_delete=models.CASCADE)
    intern = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Relación corregida
    status = models.CharField(max_length=20, choices=[
        ('applied', 'Applied'),
        ('interview', 'Interview'),
        ('rejected', 'Rejected'),
        ('hired', 'Hired')
    ], default='applied')
    applied_at = models.DateTimeField(auto_now_add=True)