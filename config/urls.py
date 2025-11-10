"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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

from votaciones2025.views import loginvotaciones,Home  # importa la nueva vista
#from votaciones2025.views import login  # importa la nueva vista

urlpatterns = [
    #path('admin/', admin.site.urls),
    #path('', login, name='login'),  # usa la nueva función
    path('', loginvotaciones().login, name='baselogin'),
    path('homejurado/', Home().homejurado, name='homejurado'),
    path('homeadministrador/', Home().homeadministrador, name='homeadministrador'),
<<<<<<< HEAD
    path("registrar_voto/", Home().registrar_voto, name="registrar_voto"),
=======
    path('resultadosadmin/', Home().resultadosadmin, name='resultadosadmin')
>>>>>>> c19d82ee843ace16090e466cd71322af2248b5a4
]
#urlpatterns = [
#    #path('', loginvotaciones().login, name='login'), # usa la nueva función
#]