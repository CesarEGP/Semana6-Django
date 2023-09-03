# aca declararemos todas las rutas pertenecientes a esta aplicacion
from django.urls import path
# cuando colocamos el punto, indicamos que se trata de un archivo en el mismo nivel
# y sino colo camos el punto estaremos indicando el mismo que sera o una liberia o un archivo
# externo
from .views import (paginaInicio, 
                    devolverHoraServidor, 
                    CategoriasController, 
                    CategoriaController,
                    GolosinasController)


urlpatterns = [
    # (separa la ruta, vista que va a utilizar)
    path('inicio', paginaInicio),
    path('status', devolverHoraServidor),
    path('categorias', CategoriasController.as_view()),  # as_view() se tranforma a una vista
    path('categoria/<id>', CategoriaController.as_view()),
    path('golosinas', GolosinasController.as_view())
]