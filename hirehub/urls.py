"""
URL configuration for hirehub project.

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
  
urlpat  2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include  # Importamos 'include' para incluir las URLs de recruitment
from recruitment import views  # Importamos las vistas desde la app recruitment

urlpatterns = [
    path('admin/', admin.site.urls),  # Ruta para el panel de administración
    path('accounts/', include('django.contrib.auth.urls')),  # Rutas predeterminadas de login/logout
    path('accounts/', include('recruitment.urls')),  # Incluir las rutas de la app recruitment
    path('', views.home, name='home'),  # Ruta para la página principal
]
