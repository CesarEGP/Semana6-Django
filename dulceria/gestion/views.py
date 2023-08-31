from django.shortcuts import render

# acá se crean los controladores


# ejemplo de como renderizar plantillas 

def paginaInicio(request):
    print(request)
    # return recibe parametro como la solicitud, nombre de la plantilla
    return render(request, 'inicio.html')