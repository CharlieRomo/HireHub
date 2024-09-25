from django.urls import path
from django.contrib.auth import views as auth_views  # Importa las vistas de autenticación de Django
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),  # Ruta para el registro
    path('login/', views.custom_login, name='login'),  # Usamos la vista personalizada de login
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # Rutas para el restablecimiento de contraseña con código
    path('password-reset/', views.request_password_reset, name='request_password_reset'),
    path('password-reset/confirm/', views.confirm_reset_code, name='confirm_reset_code'),
    path('password-reset/new/', views.set_new_password, name='set_new_password'),

    path('intern-home/', views.intern_home, name='intern_home'),  # Ruta para becarios
    path('company-home/', views.company_home, name='company_home'),  # Ruta para empresas

    path('edit-intern-profile/', views.edit_intern_profile, name='edit_intern_profile'),  # Ruta para editar el perfil de becario
    path('list-jobs/', views.list_jobs, name='list_jobs'),  # Ruta para listar empleos
    path('edit-company-profile/', views.edit_company_profile, name='edit_company_profile'),  # Ruta para editar perfil de empresa
    path('create-job-posting/', views.create_job_posting, name='create_job_posting'),
    path('mis-vacantes/', views.my_job_postings, name='my_job_postings'),
    path('vacante/<int:job_id>/', views.job_detail, name='job_detail'),

    path('apply-job/<int:job_id>/', views.apply_job, name='apply_job'),
]

