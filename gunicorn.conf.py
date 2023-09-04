# Ejemplo de gunicorn_config.py

bind = '0.0.0.0:8000'
workers = 4
# ...

# El nombre del módulo WSGI debe ser 'dulceria.wsgi'
module = 'dulceria.wsgi'
