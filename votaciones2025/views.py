# Create your views here.


from django.shortcuts import render

import firebase_admin
from firebase_admin import credentials, firestore
import os


from django.contrib.auth import authenticate, login

from django.contrib import messages


url = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "static/keys/credencial.json")
cred = credentials.Certificate(url)
firebase_admin.initialize_app(cred)
db = firestore.client()

def login(request):
    return render(request, "login_test.html")

class loginvotaciones:
   def login(self,request):
        return render(request, 'login.html')

"""if request.method == 'POST':
    
            self.username = request.POST.get('username')

            self.password = request.POST.get('password')

            self.tipo_user = request.POST.get('opcionesid')

            tipos_de_usuarios={"MECI":"MÉDICO CIRUJANO","ENFER":"ENFERMERA/O","ADMIN":"ADMINISTRADOR/A"}

            #print(self.username,self.password,self.tipo_user)

            self.user = authenticate(
                request, username=self.username.lower(), password=self.password)

            context = {'contenido': self.username.lower(),'tipo_usuario_completo':tipos_de_usuarios[self.tipo_user]}
            

            if self.user is not None:

                if self.tipo_user == "":
                    messages.warning(
                    request, 'Seleccionar tipo de usuario')
                    return render(request, 'alert_nofile.html')
                
                elif self.tipo_user!= self.user.tipo_user:
                    messages.warning(
                    request, '{} no es tu tipo de usuario, ¡compruébelo!'.format(tipos_de_usuarios[self.tipo_user]))
                    return render(request, 'alert_nofile.html')
                
                login(request, self.user)

                if self.user.tipo_user=="MECI":
                    request.session['correo'] = self.username.lower()
                    request.session['tipouser'] =self.tipo_user
                    request.session['tipousercompleto'] = tipos_de_usuarios[self.tipo_user]
                    return render(request, 'homecirujano.html', context)

                elif self.user.tipo_user=="ENFER":
                    request.session['correo'] = self.username.lower()
                    request.session['tipouser'] =self.tipo_user
                    request.session['tipousercompleto'] = tipos_de_usuarios[self.tipo_user]
                    return render(request, 'homeenfermera.html', context)
                
                elif self.user.tipo_user=="ADMIN":
                    request.session['correo'] = self.username.lower()
                    request.session['tipouser'] =self.tipo_user
                    request.session['tipousercompleto'] = tipos_de_usuarios[self.tipo_user]
                    return render(request, 'homeadministrador.html', context)               

            else:
                # messages.error(request, 'Nombre de usuario o contraseña incorrectos.')
                messages.warning(
                    request, 'Contraseña o nombre de usuario incorrecto, ¡compruébelo!')
                return render(request, 'alert_nofile.html')

        return render(request, 'login.html')
    
    def contact(self, request):
        return render(request, "contact.html")"""