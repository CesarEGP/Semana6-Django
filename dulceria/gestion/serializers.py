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