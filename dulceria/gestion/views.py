from django.shortcuts import render
from rest_framework.decorators  import api_view
from rest_framework.response import Response
from datetime import datetime
from rest_framework import request
from rest_framework.views import APIView
from .models import CategoriaModel

from .serializers import CategoriaSerializer

# ayuda a designar los estados 
from rest_framework import status

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
        serializador = CategoriaSerializer(instance=categorias, many=True)

        return Response(data={
            'message': 'La categoria es',
            'content': serializador.data
        })
    
    def post(self, request: request):
        # a qui se guarda la info proveniente del cliente
        data = request.data

        # data > validar la informacion entrante y ver que cumpla los parametro necsarios
        serializador = CategoriaSerializer(data = data)

        validacion = serializador.is_valid()

        if validacion == True:
            nuevacategoria = serializador.save()
            print(nuevacategoria)
            return Response(data={
                'message':'Categoria creada exitosamente'
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(data={
                'message':'Error al crear la categoria',
                'content': serializador.errors # me da un listado con lo errores
            }, status=status.HTTP_400_BAD_REQUEST)
        
class CategoriaController(APIView):
    def get(self, request: request, id: str):
        # consulta para saber si existe el id
        categoriaEncontrada = CategoriaModel.objects.filter(id = id).first()  #first devuelve la primera coincidencia
        # si no hay una categoria encontrada entonces return response
        if not categoriaEncontrada:
            return Response(data={
                'message': 'Categoria no encontrada'
            }, status= status.HTTP_404_NOT_FOUND)
        
        serializador = CategoriaSerializer(instance=categoriaEncontrada)
        return Response(data={
            'content': serializador.data
        })
    
    def put(self, request: request, id: str):
        categoriaEncontrada = CategoriaModel.objects.filter(id=id).first()
        if not categoriaEncontrada:
            return Response(data={
                'message': 'Categoria no encontrada'
            }, status= status.HTTP_404_NOT_FOUND)
        
        data = request.data
        serializador = CategoriaSerializer(data=data)
        dataValida = serializador.is_valid()
        if dataValida:
            serializador.validated_data  # la data convertida a un diccionario con los campos
            # que necesita el modelo, si se llega a pasar un campo que no utiliza, este no se guradaria
            # en este atributo
            serializador.update(categoriaEncontrada, serializador.validated_data)

            return Response(data={
                'message': 'Categoria actualizada exitosamente',
            })
        
        else:
            return Response(data={
                'message':'Error al actualizar la categoria',
                'content':serializador.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        

    def delete(self, request: request, id: str):
        pass