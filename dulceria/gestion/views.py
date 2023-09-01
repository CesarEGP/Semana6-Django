from django.shortcuts import render

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