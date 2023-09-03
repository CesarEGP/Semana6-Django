from django.db import models
#acá se import la libreria para usar uuid
from uuid import uuid4

# Create your models here.
class CategoriaModel(models.Model):
    opcionesNivelAzucar = (
        # si se usara form dentro de django
        # bd, lo que se mostraria en el formulario
        ['MA','MUY_ALTO'],
        ['ALTO','ALTO'],
        ['MEDIO','MEDIO'],
        ['BAJO','BAJO'],
        ['MUY_BAJO','MUY_BAJO'],
        ['CERO','CERO']
    )
    #toda la doc de los field estan aqui:
    #https://docs.djangoproject.com/en/4.2/ref/models/fields/#field-types
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    #primary_key asigna la primary key 
    #default > asigna un valor por defecto
    #editable > su valor no se puede cambiar una vez creado
    #null > si es false significa que no puede ser null
    nombre = models.TextField(null=False)
    nivelAzucar = models.TextField(db_column='nivel_azucar', null=False, 
        choices=opcionesNivelAzucar)
    

    # acá se crean las tablas 
    class Meta:
        db_table = 'categorias'

class GolosinaModel(models.Model):
    opcionProcedencia = (
        ['NACIONAL','NACIONAL'],
        ['IMPORTADO','IMPORTADO']
    )


    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    nombre = models.TextField(null=False)
    fechaVencimiento = models.DateField(editable=False, null=False, db_column='fecha_vencimiento')
    precio = models.FloatField(null=False)
    procedencia = models.TextField(choices=opcionProcedencia, default='NACIONAL')

    #RELACIONES
    # on_delete > cuando se elimine un registro de la categoria  y esta tenga  golosinas
    # como deberia actuar los datos?
    # CASCADE > eliminar la cateogir y eliminar sus golosinas
    # PROTECT > evitar la eliminacion y lanzará un error de tipo Protected error(evita la elimacion de las golosinas)
    # RESTRICT > evitara la eliminacion pero lanzara un error de tipo RestrictedError
    # SET_NULL > eliminara la categoria y este cambio cambiara el id por null, (no se puede colocar null=false)
    # SET_DEFAULT > eliminara la categoria y cambiarel valor de sus golosinas a un valor por defecto
    # DO_NOTHING > no se debe utilizar esto, deja el id en esta columna a pesar que ya no exista, genera incongruencias
    categoria = models.ForeignKey(to=CategoriaModel,db_column='categoria_id', on_delete=models.PROTECT,
    # related_name >  crea un atributo virtual en otro modelo para poder acceder a todas las
    # golosinas desde la categoria, sino se define este parametro usara el siguiente formato
    # NOMBRE_MODEL_set  >  GolosinaModel_set
    related_name='golosinas')

    class Meta:
        db_table='golosinas'
        # unicidad entre dos o mas columnas
        # jamas se podra repetir en un registro el nombre y la fecha de venc
        # constraint - restriccion
        unique_together = [['nombre', 'fechaVencimiento']]