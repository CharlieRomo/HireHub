from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .forms import JobPostingForm, CompanyProfileForm, CustomUserCreationForm, InternProfileForm # Importar formularios personalizados
from .models import *  # Importar el modelo CustomUser
from django.contrib.auth.decorators import login_required
from .models import JobPosting, JobApplication
from django.http import HttpResponseForbidden
from django.urls import reverse
#hola
# Vista para solicitar restablecimiento de contraseña
def request_password_reset(request):
    if request.method == "POST":
        email = request.POST['email']
        try:
            user = CustomUser.objects.get(email=email)
            user.set_password_reset_code()  # Generar el código de restablecimiento
            request.session['reset_code'] = user.password_reset_code  # Guardar el código en la sesión
            messages.success(request, "Se ha generado un código de restablecimiento.")
            return redirect('confirm_reset_code')  # Redirigir para confirmar el código
        except CustomUser.DoesNotExist:
            messages.error(request, "No existe un usuario con ese correo.")
    return render(request, 'registration/request_password_reset.html')

# Vista para confirmar el código de restablecimiento
def confirm_reset_code(request):
    reset_code = request.session.get('reset_code', None)  # Obtener el código guardado en la sesión

    if not reset_code:
        return redirect('request_password_reset')  # Si no hay código, redirigir a la solicitud

    if request.method == "POST":
        email = request.POST['email']
        code = request.POST['code']
        try:
            user = CustomUser.objects.get(email=email)
            if user.is_password_reset_code_valid(code):  # Validar el código
                request.session['reset_user_id'] = user.id  # Guardar el ID del usuario temporalmente
                return redirect('set_new_password')  # Redirigir a la vista para establecer nueva contraseña
            else:
                messages.error(request, "El código es inválido o ha expirado.")
        except CustomUser.DoesNotExist:
            messages.error(request, "No existe un usuario con ese correo.")
    return render(request, 'registration/confirm_reset_code.html', {'reset_code': reset_code})

# Vista para establecer nueva contraseña
def set_new_password(request):
    user_id = request.session.get('reset_user_id')
    if not user_id:
        return redirect('request_password_reset')  # Si no hay usuario en sesión, redirigir

    user = get_object_or_404(CustomUser, id=user_id)

    if request.method == "POST":
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        if new_password == confirm_password:
            user.set_password(new_password)  # Establecer nueva contraseña
            user.password_reset_code = None  # Limpiar el código de restablecimiento
            user.password_reset_code_expiration = None
            user.save()
            messages.success(request, "Contraseña restablecida con éxito.")
            return redirect('login')  # Redirigir al login
        else:
            messages.error(request, "Las contraseñas no coinciden.")

    return render(request, 'registration/set_new_password.html')

# Vista para el registro de usuarios
def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)  # Procesar el formulario
        if form.is_valid():
            user = form.save(commit=False)  # Guardar el usuario
            login(request, user)  # Loguear automáticamente
            # Redirigir según el tipo de usuario
            if user.user_type == 'company':
                return redirect('company_home')  # Página de empresa
            else:
                return redirect('intern_home')  # Página de becario
    else:
        form = CustomUserCreationForm()  # Crear formulario vacío
    return render(request, 'registration/register.html', {'form': form})  # Mostrar el formulario

# Vista personalizada para iniciar sesión y redirigir según el tipo de usuario
def custom_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # Redirigir según el tipo de usuario
            if user.user_type == 'company':
                return redirect('company_home')  # Redirigir a empresa
            elif user.user_type == 'intern':
                return redirect('intern_home')  # Redirigir a becario
        else:
            messages.error(request, "Credenciales incorrectas.")
    
    return render(request, 'registration/login.html')

# Vista para la página de inicio de empresas
@login_required
def company_home(request):
    # Obtener todas las vacantes publicadas por la empresa logueada
    job_postings = JobPosting.objects.filter(company=request.user)
    
    return render(request, 'company_home.html', {'job_postings': job_postings})

# Vista para la página principal
@login_required
def home(request):
    return render(request, 'home.html')  # Renderizar la página principal

# Vista para editar el perfil de becario
@login_required
def edit_intern_profile(request):
    if request.method == 'POST':
        form = InternProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Perfil actualizado con éxito.")
            return redirect('intern_home')
        else:
            print(form.errors)  # Añadir esto para imprimir los errores
            messages.error(request, "Hubo un error al actualizar el perfil.")
    else:
        form = InternProfileForm(instance=request.user)
    return render(request, 'edit_intern_profile.html', {'form': form})

#vista para editar empresa
@login_required
def edit_company_profile(request):
    if request.method == 'POST':
        form = CompanyProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Perfil de empresa actualizado con éxito.")
            return redirect('company_home')
        else:
            print(form.errors)  # Añadir esto para imprimir los errores
            messages.error(request, "Hubo un error al actualizar el perfil.")
    else:
        form = CompanyProfileForm(instance=request.user)
    return render(request, 'edit_company_profile.html', {'form': form})

# Vista para listar vacantes
@login_required
def list_jobs(request):
    jobs = JobPosting.objects.all()  # Obtener todas las vacantes
    return render(request, 'list_jobs.html', {'jobs': jobs})

#######################


@login_required
def create_job_posting(request):
    if request.method == 'POST':
        form = JobPostingForm(request.POST)
        if form.is_valid():
            job_posting = form.save(commit=False)
            job_posting.company = request.user  # Asocia la oferta de trabajo con la empresa logueada
            job_posting.save()
            return redirect('company_home')
    else:
        form = JobPostingForm()
    return render(request, 'create_job_posting.html', {'form': form})


@login_required
def my_job_postings(request):
    # Filtra las vacantes creadas por la empresa logueada
    job_postings = JobPosting.objects.filter(company=request.user)
    return render(request, 'my_job_postings.html', {'job_postings': job_postings})

@login_required
def job_detail(request, job_id):
    job_posting = get_object_or_404(JobPosting, id=job_id)
    return render(request, 'job_detail.html', {'job_posting': job_posting})


@login_required
def apply_job(request, job_id):
    job = get_object_or_404(JobPosting, id=job_id)
    
    # Verificar si ya ha postulado anteriormente
    if JobApplication.objects.filter(intern=request.user, job=job).exists():
        messages.error(request, "Ya has postulado a esta vacante.")
    else:
        # Crear una nueva postulación
        JobApplication.objects.create(
            intern=request.user,
            job=job,
            status='Pendiente'  # Puedes ajustar el estatus según tu lógica
        )
        messages.success(request, "Has postulado exitosamente a esta vacante.")

    return redirect('list_jobs')  # Redirige a la lista de trabajos después de postular

@login_required
def intern_home(request):
    applications = JobApplication.objects.filter(intern=request.user)
    return render(request, 'intern_home.html', {'applications': applications})

@login_required
def edit_job_posting(request, job_id):
    job_posting = get_object_or_404(JobPosting, id=job_id, company=request.user)

    if request.method == 'POST':
        form = JobPostingForm(request.POST, instance=job_posting)
        if form.is_valid():
            form.save()
            messages.success(request, "Vacante actualizada con éxito.")
            return redirect('my_job_postings')
    else:
        form = JobPostingForm(instance=job_posting)

    return render(request, 'edit_job_posting.html', {'form': form})

@login_required
def delete_job_posting(request, job_id):
    job_posting = get_object_or_404(JobPosting, id=job_id, company=request.user)

    if request.method == 'POST':
        job_posting.delete()
        messages.success(request, "Vacante eliminada con éxito.")
        return redirect('my_job_postings')

    return render(request, 'confirm_delete_job_posting.html', {'job_posting': job_posting})

@login_required
def job_detail_intern(request, job_id):
    # Busca la vacante o lanza un error 404 si no existe
    job_posting = get_object_or_404(JobPosting, id=job_id)
    return render(request, 'job_detail_intern.html', {'job_posting': job_posting})


########## yo como empresa puedo ver los que aplican
@login_required
def view_applicants(request):
    # Obtener todas las vacantes publicadas por la empresa
    job_postings = JobPosting.objects.filter(company=request.user)

    # Obtener todas las aplicaciones de estas vacantes
    applications = JobApplication.objects.filter(job__in=job_postings)

    return render(request, 'view_applicants.html', {'applications': applications})

##################################

@login_required
def delete_application(request, application_id):
    application = get_object_or_404(JobApplication, id=application_id, intern=request.user)
    
    if request.method == 'POST':
        application.delete()
        messages.success(request, 'Tu postulación ha sido eliminada exitosamente.')
        return redirect('intern_home')
    
    return redirect('intern_home')


@login_required
def advance_application(request, application_id):
    application = get_object_or_404(JobApplication, id=application_id)

    # Ciclo de los estados: avanzamos en el flujo lógico
    if application.status == 'applied':
        application.status = 'interview'  # Avanza de 'applied' a 'interview'
    elif application.status == 'interview':
        application.status = 'hired'  # Avanza de 'interview' a 'hired'
    elif application.status == 'rejected':
        application.status = 'applied'  # Si está rechazado, vuelve a 'applied'
    elif application.status == 'hired':
        # Si ya está en 'hired', no permitimos avanzar más
        messages.warning(request, 'El candidato ya ha sido contratado y no puede avanzar más.')
        return redirect('view_applicants')

    application.save()  # Guardar el cambio

    # Mensaje de éxito cuando se avanza correctamente
    messages.success(request, 'El estado de la postulación ha sido actualizado.')

    return redirect('view_applicants')

@login_required
def reject_application(request, application_id):
    application = get_object_or_404(JobApplication, id=application_id)
    application.status = 'rejected'
    application.save()
    return redirect('view_applicants')
