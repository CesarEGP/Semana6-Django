from django.shortcuts import render
from rest_framework.decorators  import api_view
from rest_framework.response import Response
from datetime import datetime
from rest_framework import request
from rest_framework.views import APIView
from .models import CategoriaModel

# acá se crean los controladores


# ejemplo de como renderizar plantillas 

def paginaInicio(request):
    print(request)
    data={
        'usuario':{
            'nombre':'Cesar',
            'apellido':'Garcia Pizarro'
        },
        'hobbies':[
            {
                'description': 'Ir al cine'
            },
            {
                'description': 'Ir a la piscina'
            }
        ]
    }
    return render(request, 'inicio.html', {'data': data})


#El decorador api_view solo sirve en funciones, en class no funciona
@api_view(http_method_names=['GET', 'POST'])
def devolverHoraServidor(request: request):
    print(request.method)

    if request.method == 'GET':

        return Response(data={
            'content': datetime.now()
        })
    elif request.method == 'POST':
        return Response(data={
            'content': 'Para saber la hora, relaizar un GET'
        })

#este es importante
class CategoriasController(APIView):
    def get(self, request: request):
        # select * from categorias
        categorias = CategoriaModel.objects.all()
        print(categorias)

        return Response(data={
            'message': 'La categoria es',
        })
    
    def post(self, request: request):
        # a qui se guarda la info proveniente del cleinte
        data = request.data