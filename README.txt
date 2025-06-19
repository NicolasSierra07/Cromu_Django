
==============================
ENTREGABLES - PROYECTO CROMU
==============================

1. Código fuente completo del proyecto
--------------------------------------
Incluye la estructura de directorios típica de un proyecto Django:

Cromu/
├── cromu/                  # Configuración del proyecto
├── ahorros/                # App de Ahorros
├── prestamos/              # App de Préstamos
├── templates/              # Plantillas HTML
├── static/                 # Archivos estáticos (opcional)
├── manage.py
└── README.md

2. requirements.txt
-------------------
Dependencias necesarias para ejecutar el proyecto:

Django>=5.2.3
djangorestframework>=3.15.1
pandas>=2.2.2
matplotlib>=3.9.0
mysqlclient>=2.2.4  # o psycopg2>=2.9.9 si usas PostgreSQL

Comando para generarlo automáticamente:
pip freeze > requirements.txt

3. README.md (Documentación)
-----------------------------

# Sistema de Gestión de Ahorros y Préstamos - CROMU

Este sistema permite a los usuarios gestionar sus ahorros y préstamos, registrar pagos y visualizar estadísticas gráficas.

## Cómo configurar y ejecutar el proyecto

1. Clona el repositorio del proyecto o copia el código fuente.
2. Crea y activa un entorno virtual:
   python -m venv venv
   source venv/bin/activate (Linux/macOS) o venv\Scripts\activate (Windows)
3. Instala las dependencias:
   pip install -r requirements.txt
4. Configura la base de datos en settings.py (MySQL o PostgreSQL).
5. Ejecuta las migraciones:
   python manage.py makemigrations
   python manage.py migrate
6. Crea un superusuario:
   python manage.py createsuperuser
7. Ejecuta el servidor de desarrollo:
   python manage.py runserver

## Descripción de las librerías utilizadas

- Django: Framework principal para desarrollo web.
- Django REST Framework: Para crear APIs RESTful.
- Pandas: Para manipulación de datos y generación de gráficos.
- Matplotlib: Para crear visualizaciones en gráficos PNG.
- mysqlclient o psycopg2: Conectores de bases de datos (MySQL o PostgreSQL).

## Explicación de la estructura de base de datos

### Modelo Ahorro
- nombre: ForeignKey a User
- descripcion: Texto descriptivo del ahorro
- monto: Monto inicial
- cuota_mensual: Monto mensual a aportar
- dinero_total: Dinero acumulado
- meses_restantes: Número de meses restantes
- fecha_creacion: Fecha de creación del ahorro

### Modelo PagoMensual
- ahorro: ForeignKey a Ahorro
- mes: Nombre del mes
- año: Año del pago
- pagado: Booleano que indica si el mes está pagado
- fecha_pago: Fecha exacta del pago

### Modelo Prestamo
- nombre: ForeignKey a User
- descripcion: Motivo o descripción del préstamo
- monto: Valor total del préstamo
- cuota_mensual: Monto que se paga mensualmente
- cantidad_meses: Total de meses acordados
- fecha_creacion: Fecha en que se creó el préstamo

### Modelo PagoCuota
- prestamo: ForeignKey a Prestamo
- mes: Nombre del mes
- año: Año del pago
- pagado: Booleano que indica si la cuota fue pagada


