from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *
from django.core.exceptions import ValidationError

# Crear un formulario de registro personalizado
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser  # Usamos el modelo de usuario personalizado
        fields = ('username', 'first_name', 'last_name', 'email', 'user_type')  # Solo los campos que necesitamos

    # Validar que el nombre no contenga números
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if any(char.isdigit() for char in first_name):
            raise ValidationError("El nombre no debe contener números.")
        return first_name

from django import forms
from django.core.exceptions import ValidationError

# Formulario para el perfil del becario con preguntas tipo CV
class InternProfileForm(forms.ModelForm):
    # Campos personalizados para obtener la información del CV con validaciones y mejor diseño
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Nombre'}))
    last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Apellido'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Correo electrónico'}))

    education = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Describe tu formación académica, títulos obtenidos, etc.'}),
        help_text="Describe tu formación académica."
    )
    work_experience = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Detalla tu experiencia laboral, empresas, roles, fechas.'}),
        help_text="Describe tu experiencia laboral."
    )
    skills = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Lista tus habilidades, ej: trabajo en equipo, liderazgo, Python.'}),
        help_text="Lista tus habilidades relevantes."
    )
    certifications = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Menciona certificaciones o cursos que hayas completado.'}),
        help_text="Menciona certificaciones o cursos que hayas completado."
    )
    languages = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Idiomas que dominas y nivel de competencia.'}),
        help_text="Idiomas que dominas y nivel de competencia."
    )
    
    class Meta:
        model = CustomUser  # Usamos el modelo de usuario personalizado
        fields = ['first_name', 'last_name', 'education', 'work_experience', 'skills', 'certifications', 'languages']  # Campos a completar

    # Validación adicional para verificar que el campo de educación no esté vacío
    def clean_education(self):
        education = self.cleaned_data.get('education')
        if not education:
            raise ValidationError("Debes proporcionar información sobre tu educación.")
        return education



    
#Formulario para la empresa
class CompanyProfileForm(forms.ModelForm):
    company_name = forms.CharField(help_text="Nombre de la empresa")
    sector = forms.CharField(help_text="Sector de la empresa")
    description = forms.CharField(widget=forms.Textarea, help_text="Describe la empresa.")
    website = forms.URLField(required=False, help_text="Página web de la empresa (opcional)")
    
    class Meta:
        model = CustomUser
        fields = ['company_name', 'sector', 'description', 'website']

class JobPostingForm(forms.ModelForm):
    class Meta:
        model = JobPosting
        fields = ['title', 'description', 'location']  # Campos que pueden rellenar las empresas

