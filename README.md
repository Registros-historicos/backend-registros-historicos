# Proyecto Django - Sistema de Registros Historicos

## 📂 Estructura principal

    PROYECTO-DJANGO/
    │── config/          # Configuración del proyecto (settings modularizados)
    │── core/            # Utilidades y lógica compartida
    │── apps/            # Aplicaciones del sistema (auth, tableros, etc.)
    │── requirements/    # Dependencias por entorno
    │── manage.py

## Estructura de las aplicaciones

Para cada modulo/funcionalidad, deberan crear su app usando el comando:

```bash
    python manage.py startapp <nombre_app>
```

### Estructura recomendada de la app

Dentro de cada app, organizar el código así:

```bash
    <nombre_app>/
    ├── apps.py                 # Configuración de la app para Django (siempre requerido)
    ├── admin.py                # (vacío si no hay modelos ORM)
    ├── models.py               # (vacío si usas funciones de Postgres en lugar de ORM)
    ├── domain/                 # Entidades, reglas de negocio y puertos
    │   ├── entities.py         # Dataclasses con el modelo de dominio
    │   └── ports.py            # Interfaces (repos, gateways)
    ├── application/            # Casos de uso
    │   ├── services/           # Comandos (create, update, delete)
    │   │   └── <nombre_service>.py
    │   └── selectors/          # Consultas de solo lectura
    │       └── <nombre_selector>.py
    ├── infrastructure/         # Implementaciones técnicas
    │   ├── repositories/       # Adaptadores a funciones Postgres u otros servicios
    │   │   ├── pg_utils.py
    │   │   └── <nombre_repo>.py
    │   └── web/                # Capa de exposición (API REST / DRF)
    │       ├── serializers.py
    │       ├── views.py
    │       └── urls.py
    └── tests/                  # Tests unitarios e integración
        ├── unit/               # Pruebas de domain/ y application/
        └── integration/        # Pruebas de repositories/ y web/
```



-----------------------------------------------------------------------
## Instalación y Ejecución del proyecto

1.  Clonar el repositorio:

    ``` bash
    git clone https://github.com/DanielaaER/backend-registros-historicos.git
    cd PROYECTO-DJANGO
    ```

2.  Crear entorno virtual:

    ``` bash
    python -m venv venv
    source venv/bin/activate   # Linux
    venv\Scripts\activate      # Windows
    ```

3.  Instalar dependencias de desarrollo:

    ``` bash
    pip install -r requirements/dev.txt
    ```

4.  Crear archivo `.env` en la raíz del proyecto:

    ``` ini
    SECRET_KEY= # Clave secreta de Django (proporcionada por el equipo)
    DEBUG=True
    ALLOWED_HOSTS=localhost,127.0.0.1

    DEV_DB_NAME= # Nombre de la base de datos
    DEV_DB_USER= # Usuario de la base de datos
    DEV_DB_PASSWORD= # Contraseña de la base de datos
    DEV_DB_HOST= # Host de la base de datos
    DEV_DB_PORT=5432


    ```

5.  Ejecutar migraciones y correr el servidor:

    ``` bash
    python manage.py migrate
    python manage.py runserver
    ```

------------------------------------------------------------------------

## Entornos

El proyecto maneja settings separados:

-   `config.settings.dev` → Desarrollo
-   `config.settings.prod` → Producción
-   `config.settings.test` → Pruebas

Por defecto, en `manage.py` se carga **`config.settings.dev`**.\
En producción puedes usar:

``` bash
DJANGO_SETTINGS_MODULE=config.settings.prod python manage.py runserver
```

------------------------------------------------------------------------

## Dependencias

-   Django\
-   Django REST Framework\
-   JWT (SimpleJWT)\
-   OAuth Toolkit\
-   Redis\
-   psycopg2 (PostgreSQL)\
-   Django CORS Headers

------------------------------------------------------------------------

## Actualización de dependencias

Cada que instales una nueva librería, **actualiza los requirements**
con:

``` bash
pip freeze > requirements/dev.txt
```

Ejemplo:

``` bash
pip install django-debug-toolbar
pip freeze > requirements/dev.txt
```

------------------------------------------------------------------------

## Buenas prácticas

-   Mantener el `.env` **fuera de git** (`.gitignore` ya lo incluye).
-   Separar lógica en capas: `domain/`, `application/`,
    `infrastructure/`.
-   Cada app debe tener sus propios tests en `apps/<app>/tests/`.

