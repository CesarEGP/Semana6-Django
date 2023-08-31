# aca declararemos todas las rutas pertenecientes a esta aplicacion
from django.urls import path
# cuando colocamos el punto, indicamos que se trata de un archivo en el mismo nivel
# y sino colo camos el punto estaremos indicando el mismo que sera o una liberia o un archivo
# externo
from .views import paginaInicio

urlpatterns = {
    # (separa la ruta, vista que va a utilizar)
    path('inicio', paginaInicio)
}