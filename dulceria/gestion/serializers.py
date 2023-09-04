# los serializers son como los dto 
from rest_framework import serializers
from .models import CategoriaModel, GolosinaModel

class CategoriaSerializer(serializers.ModelSerializer):
    # siver para basarme en un modelo que haga todas las validadciones correspondientes
    class Meta:
        model = CategoriaModel
        # si utiliza todos loa atributos del modelo, usa la sgte forma
        fields = '__all__'
        # fields = ['id','name','nivelAzucar']
        # si quieres utlizar todos los atributos menos uno o la minoria
        # exclude = ['id']
        # NOTA : O se usa el atrib field o exclude pero no se usan al mismo 
        # tiempo

class GolosinaSerializer(serializers.ModelSerializer):

    class Meta:
        model = GolosinaModel
        fields = '__all__'

class GolosinaResponseSerializer(serializers.ModelSerializer):

    class Meta:
        model = GolosinaModel
        fields = '__all__'    
        # depth es para mostrar cuantos niveles de join se puede mostrar 
        depth = 1

class CategoriaResponseSerializer(serializers.ModelSerializer):


    #aca se coloca el related_name que esta en GolosinaModel dentro de models

                        #es importante poner many=True porque sabemos que seran muchos registros
    golosinass = GolosinaSerializer(many=True, source='golosinas')

    class Meta:
        model = CategoriaModel
        fields = '__all__'   
        # no se puede usar depth si esta tabla no tiene la llave foranea
        # depth = 1
