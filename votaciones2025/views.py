# Create your views here.


from django.shortcuts import render
from firebase_admin import credentials, db

import firebase_admin

import os, requests, json
import time

#from django.contrib.auth import authenticate, login

from django.contrib import messages

#Experimentacion
#url = os.path.join(os.path.dirname(os.path.abspath(__file__)),"static/keys/credencialt.json")
#excProduccion
url = json.loads(os.environ["FIREBASE_CREDENTIALS"])

cred = credentials.Certificate(url)

firebase_admin.initialize_app(cred, {"databaseURL": "https://votacionesguambia2025-default-rtdb.firebaseio.com/" })

FIREBASE_API_KEY = "AIzaSyCLLBDHkY01khL_fys_cQJ9vFReyzK_PAE"
#def login(request):
#    return render(request, "login_test.html")

class loginvotaciones:
    def login(self,request):
        #return render(request, 'login.html')

        if request.method == 'POST':
    
            self.username = request.POST.get('username')

            self.password = request.POST.get('password')

            self.tipo_user = request.POST.get('opcionesid')

            tipos_de_usuarios={"JUR":"JURADO","ADMIN":"ADMINISTRADOR/A"}

            print(self.username,self.password,self.tipo_user)

            ref_respnsables = db.reference("usuariosresponsables")


            # Leer todos los datos del nodo
            data_responsables = ref_respnsables.get()

            print("Data responsables=",data_responsables)

            if self.tipo_user == "":
                messages.warning(
                request, 'Seleccionar tipo de usuario')
                return render(request, 'alert_nofile.html')

            #self.user = authenticate(
            #    request, username=self.username.lower(), password=self.password)

            #print(self.user)

            api_key =FIREBASE_API_KEY# getattr(settings, "FIREBASE_API_KEY", os.getenv("FIREBASE_API_KEY", ""))
            url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}"
            payload = {"email": self.username, "password": self.password, "returnSecureToken": True}
            
            
            
            r = requests.post(url, json=payload, timeout=10)
            
            data = r.json()
            
            
            context = {'contenido': self.username.lower(),'tipo_usuario_completo':tipos_de_usuarios[self.tipo_user]}
            
       

            
            
            error_info = data.get("error", {})
            error_msg = error_info.get("message", "")

            print(error_info,error_msg)



            if error_msg == "EMAIL_NOT_FOUND":
                messages.warning(
                    request, "El usuario no existe en el sistema.")
                return render(request, 'alert_nofile.html')
            elif error_msg == "INVALID_PASSWORD":
                messages.warning(
                    request, "Contraseña incorrecta.")
                return render(request, 'alert_nofile.html')
            elif error_msg == "USER_DISABLED":
                
                messages.warning(
                    request, "La cuenta de usuario está deshabilitada.")
                return render(request, 'alert_nofile.html')

            elif error_msg == "TOO_MANY_ATTEMPTS_TRY_LATER":
                
                messages.warning(
                    request, "Demasiados intentos fallidos. Inténtalo más tarde o restablece tu contraseña.")
                return render(request, 'alert_nofile.html')
            
            elif error_msg == "INVALID_LOGIN_CREDENTIALS":
                
                messages.warning(
                    request, "Validar credencialesde usuario.")
                return render(request, 'alert_nofile.html')
            
            if self.tipo_user=="JUR":
                role_user=ref_respnsables.get()[data["localId"]]["role"]

                print("Roles=",role_user)
                request.session['correo'] = self.username.lower()
                request.session['tipouser'] =self.tipo_user
                request.session['tipousercompleto'] = tipos_de_usuarios[self.tipo_user]
                request.session["iduserjurado"]=data["localId"]

                context["mesa"]=ref_respnsables.get()[data["localId"]]["mesa"]
                context["nombrejurado"]=ref_respnsables.get()[data["localId"]]["nombre"]
                context["iduserjurado"]=data["localId"]

                if role_user != "JURADO":
                    messages.warning(
                        request, 'Tú no eres un usuario JURADO, ¡compruébelo!')
                    return render(request, 'alert_nofile.html')
                else:
                    return render(request, 'homejurado.html', context)

            
            elif self.tipo_user=="ADMIN":
                role_user=ref_respnsables.get()[data["localId"]]["role"]

                print("Roles=",role_user)
                request.session['correo'] = self.username.lower()
                request.session['tipouser'] =self.tipo_user
                request.session['tipousercompleto'] = tipos_de_usuarios[self.tipo_user]
                if role_user != "ADMIN":
                    messages.warning(
                        request, 'Tú no eres un usuario ADMINISTRADOR, ¡compruébelo!')
                    return render(request, 'alert_nofile.html')
                else:
                    return render(request, 'homeadministrador.html', context)

            else:
                messages.warning(
                    request, 'Contraseña o nombre de usuario incorrecto, ¡compruébelo!')
                return render(request, 'alert_nofile.html')

            
        
        return render(request, 'login.html')
                


    


class Home:
    
    def leer_documentos_coleccion(self,correo,key_search):
        docs = db.collection('cirujanos').document(correo).collection("pacientes").document(key_search)
        return docs.get().to_dict()
        
    def buscar_usuario_admin(self,key):
        
        correokey=db.collection('pacientes').document(key).collection("info_paciente").document("paciente").get().to_dict()["correo_cir"]
        #db.collection('pacientes').document(key).get().to_dict()["correo"]
        #print("urldoc",correokey)
        docs = db.collection('cirujanos').document(correokey).collection("pacientes").document(key)
        return docs.get().to_dict()

    def buscar_responsable_usuario(self,key):
        
        responsabledicc=db.collection('pacientes').document(key).collection("info_paciente").document("responsable")
        return responsabledicc.get().to_dict()
    
    def buscar_historico_usuario(self,key):
        
        historicodb = db.collection('pacientes').document(key).collection("historico")
        docs = historicodb.stream()

        for doc in docs:
            print(f"Document ID: {doc.id}")
            print("Data:", doc.to_dict())

        return docs#.get().to_dict()

    
    # BUSCARDORES DE USUARIOS

    def homejurado(self, request):
        id_numer = request.GET.get('buscadorid')
        tipo_id = request.GET.get('opcionesid')

        correouser =request.session.get('correo')
        tipousercompleto=request.session.get('tipousercompleto')


        iduserjuradoin =request.session.get('iduserjurado')
        #tipousercompleto=request.session.get('tipousercompleto')


        key_search=str(tipo_id)+str(id_numer)
        print("testt",key_search,correouser)




        resultadoss={}

        try:
            ref_respnsablesdb = db.reference("usuariosresponsables")

            #print("RESPONSABLES JURADOS",ref_respnsablesdb.get(),iduserjuradoin)
            ref_encuentas = db.reference("usuariosencuestados")
            # Leer todos los datos del nodo           

            data_user=ref_encuentas.get()[key_search]

            
            #print(data_user)#resultadosdatosusuario=self.buscar_usuario_admin(key_search)
            #resultadosresponsable=self.buscar_responsable_usuario(key_search)

            resultadoss = {**data_user}#, **resultadosresponsable}           
            resultadoss['tipo_usuario_completo']=tipousercompleto
            resultadoss["mesajurado"]=ref_respnsablesdb.get()[iduserjuradoin]["mesa"]
            resultadoss["nombrejurado"]=ref_respnsablesdb.get()[iduserjuradoin]["nombre"]


            #print("RESULTADOS:-----",resultadoss)
        except:
            
            resultadoss={"tipo_usuario_completo":"JURADO","noexistuser":"1"}#['tipo_usuario_completo']="MÉDICO CIRUJANO"
            

        return render(request, 'homejurado.html', resultadoss)

    def homejurados(self, request):
        resultadoss={"tipo_usuario_completo":"JURADO","noexistuser":"0"}#['tipo_usuario_completo']="MÉDICO CIRUJANO"
            

        return render(request, 'homejurado.html', resultadoss)
    
    def homeadministrador(self, request):
    
        id_numer = request.GET.get('buscadorid')
        tipo_id = request.GET.get('opcionesid')

        tipousercompleto=request.session.get('tipousercompleto')
        
        key_search=str(tipo_id)+'_'+str(id_numer)

        print(key_search,tipousercompleto)

        try:
            resultadosdatosusuario=self.buscar_usuario_admin(key_search)
            resultadosresponsable=self.buscar_responsable_usuario(key_search)

            resultadoss = {**resultadosdatosusuario, **resultadosresponsable}
            
            resultadoss['tipo_usuario_completo']=tipousercompleto
        except:
            resultadoss={'tipo_usuario_completo':"ADMINISTRADOR/A"}

        #print("resultados",resultadoss)
        return render(request, 'homeadministrador.html', resultadoss)
    

    def registrar_voto(self, request):
        if request.method == "POST":
            tipo_id = request.POST.get("tipo_doc")   # leer variable voto
            id_numer = request.POST.get("num_doc")   # leer variable mesa
            mesarregistro = request.POST.get("mesajurado")   # leer variable mesa

            key_search=str(tipo_id)+str(id_numer)
            print("KEYS_USERS",key_search)
            try:
                ref_encuentas = db.reference("usuariosencuestados")
                ref_encuentas.child(key_search).update({"voto": "si"})
                ref_encuentas.child(key_search).update({"mesa": mesarregistro})
                # Leer todos los datos del nodo           

                #data_user=ref_encuentas.get()[key_search]
                #print("DATA USER",data_user)
                data_user=ref_encuentas.get()[key_search]

            #print(data_user)#resultadosdatosusuario=self.buscar_usuario_admin(key_search)
            #resultadosresponsable=self.buscar_responsable_usuario(key_search)

                resultadoss = {**data_user}
                resultadoss={"tipo_usuario_completo":"JURADO"}
                messages.warning(
                    request, 'VOTO REGISTRADO EXITOSAMENTE')
                return render(request, 'alert_nofile_voto.html')
            
            except:
                resultadoss={"tipo_usuario_completo":"JURADO"}

        return render(request, 'homejurado.html', resultadoss)


    def resultadosadmin(self, request):
        resultadoss={'tipo_usuario_completo':"ADMINISTRADOR/A"}
        return render(request, 'resultadosadmin.html', resultadoss) 


    

    
