from django.shortcuts import render
from rest_framework.decorators  import api_view
from rest_framework.response import Response
from datetime import datetime
from rest_framework import request
from rest_framework.views import APIView
from .models import CategoriaModel, GolosinaModel


#import serializers
from .serializers import (CategoriaSerializer, 
                        GolosinaSerializer, 
                        GolosinaResponseSerializer,
                        CategoriaResponseSerializer)

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
        # print(categoriaEncontrada.golosinas.all())
        serializador = CategoriaResponseSerializer(instance=categoriaEncontrada)
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

        categoriaEncontrada = CategoriaModel.objects.filter(id=id).first()
        if not categoriaEncontrada:
            return Response(data={
                'message': 'Categoria no encontrada'
            }, status= status.HTTP_404_NOT_FOUND)
        
        CategoriaModel.objects.filter(id=id).delete()

        return Response(data={
            'message': 'Categoria eliminada exitosamente'
        })
    
class GolosinasController(APIView):
    def get(self, request: request):        
        print(request.query_params)
        # paginacion

        #Operador ternario
        #       sucede si es verdadero                  --condicional                                                                              
        # page = request.query_params.get('page') if request.query_params.get('page') is not None else 1
        #forma mas simple que ternarios
        #       si existe page guarda, sino devuelve 1
        page = int(request.query_params.get('page',1))  # esto devuelve un string y lo convertimos a int
        # por pagina quiero solo 5
        perPage = int(request.query_params.get('perPage',5)) 

        # para ordenamiento asc y desc, se convierte en string
        ordering = request.query_params.get('ordering')
        orderingType = request.query_params.get('orderingType')  #asc o desc
        
        orderingType = '-' if orderingType == 'desc' else ''


        # cuantos elementos me voy a saltar(offset) 
        skip = (page - 1) * perPage
        # cuantos elementos voy a tomar(limit)
        take = perPage * page

        consulta = GolosinaModel.objects
        #si existe ordering entonces ..
        if ordering:
            golosinas = GolosinaModel.objects.order_by(orderingType + ordering).all()[
                skip:take]
        else:
            golosinas = GolosinaModel.objects.all()[skip:take]

        totalGolosinas = GolosinaModel.objects.count()
        # para manejar la base de datos         
        # se llama al serializer
        serializador = GolosinaSerializer(instance=golosinas, many= True) # many  > itera el arreglo 

        pagination = helperPagination(totalGolosinas,page,perPage)
        return Response(data={
            'content': serializador.data,
            'pagination': pagination
        })
    
    def post(self, request):
        #Implementar la creacion de una nueva golosina
        pass

class GolosinaController(APIView):
    def get(self, request:request,id:str):
        golosinaEncontrada = GolosinaModel.objects.filter(id=id).first()
        if golosinaEncontrada is None:
            return Response(data={
                'message': 'La golosina no existe'
            }, status=status.HTTP_404_NOT_FOUND_)
        serializador = GolosinaResponseSerializer(instance=golosinaEncontrada)
        return Response(data={
            'content': serializador.data
        })

from math import ceil

def helperPagination(total: int, page: int, perPage:int):
    itemsPerPage = perPage if total >= perPage else total
    #calcular cuantas paginas deberiamos tener
    #se usa ceil para redondear al int mas cercano
    totalPages = ceil(total / itemsPerPage) if itemsPerPage > 0 else None
    #calcular cua          pagina actia es > 1 y pagina menor al total de paginas                                        
    prevPage = page - 1 if page > 1 and page <= totalPages else None
    #comprueba si hay una pagina siguiente
    nextPage = page + 1 if totalPages > 1 and page < totalPages else None
    return{
        'itemsPerPage': itemsPerPage,
        'totalPages': totalPages,
        'prevPage': prevPage,
        'nextPage': nextPage
    }