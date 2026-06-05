# Consulta Dietética API

API RESTful desarrollada en **Django** y **Django REST Framework** para la gestión integral de consultas dietéticas, perfiles de pacientes, nutricionistas, planes nutricionales personalizados y el registro de alimentos programados.

---

## 🚀 Características del Proyecto

- **Base de Datos Relacional**: Conexión nativa con **PostgreSQL**.
- **Seguridad**: Autenticación basada en JSON Web Tokens (JWT) mediante `django-rest-framework-simplejwt`.
- **Arquitectura RESTful**: Endpoints CRUD completos para más de 5 entidades con serializadores detallados y validaciones personalizadas.
- **Paginación y Filtros**: Paginación estándar de 10 elementos por página, filtros dinámicos (estado, actividad, planes) y búsqueda avanzada por texto.
- **Control de Excepciones**: Respuestas en formato JSON consistentes para errores del cliente (400/401/403/404) y del servidor (500).

---

## 🛠️ Requisitos e Instalación

### 1. Clonar el repositorio y acceder a la carpeta
```bash
cd DIETETIC_BACKEND
```

### 2. Configurar el Entorno Virtual
Crea y activa el entorno virtual de Python (se requiere Python 3.12+):
```bash
# Crear entorno virtual
python -m venv .venv

# Activar en Windows (PowerShell)
.venv\Scripts\Activate.ps1

# Activar en Linux/macOS
source .venv/bin/activate
```

### 3. Instalar dependencias
Instala los paquetes necesarios desde `requirements.txt`:
```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno (`.env`)
Crea un archivo `.env` en la raíz del proyecto (o edita el existente) con la configuración de tu PostgreSQL:
```env
SECRET_KEY=tu_secreto_django_seguro
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Configuración PostgreSQL
DB_NAME=dietetic
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
```

---

## 💾 Migraciones y Ejecución

Asegúrate de que PostgreSQL está activo y de que existe la base de datos configurada en tu `.env`. Luego ejecuta:

```bash
# Realizar migraciones
python manage.py migrate

# (Opcional) Ejecutar pruebas automatizadas
python manage.py test

# Iniciar servidor de desarrollo
python manage.py runserver
```
El servidor estará disponible en [http://127.0.0.1:8000](http://127.0.0.1:8000).

---

## 🔐 Autenticación y Permisos

El sistema utiliza **SimpleJWT** para la protección de rutas.
- **Rutas Públicas**:
  - `POST /api/auth/register/` (Registra un usuario paciente nuevo).
  - `POST /api/auth/login/` (Obtiene el Token de Acceso).
  - `GET /api/alimentos/available/` (Ver alimentos activos sin token).
  - `GET /api/health/` (Endpoint público de estado del backend).
- **Rutas Protegidas**:
  - Todos los endpoints CRUD de creación (`POST`), actualización (`PUT`/`PATCH`) y eliminación (`DELETE`) requieren cabecera `Authorization: Bearer <su_access_token>`.
  - **Permisos**:
    - **Usuarios Administradores (`is_staff=True`)**: Acceso CRUD total en todas las entidades, acceso a estadísticas agregadas (`/stats/`) y actualización forzosa de secuencias.
    - **Usuarios Normales (Pacientes)**: Acceso seguro a sus consultas asignadas, y a ver la información pública general.

---

## 📌 Listado de Endpoints Principales

| Entidad / Función | Método | Endpoint | Descripción |
| :--- | :--- | :--- | :--- |
| **Autenticación** | `POST` | `/api/auth/register/` | Registro de nuevo usuario (crea perfil paciente). |
| | `POST` | `/api/auth/login/` | Obtención de tokens Access y Refresh JWT. |
| | `POST` | `/api/auth/token/refresh/` | Refrescar token de acceso. |
| | `POST` | `/api/auth/logout/` | Blacklist del token para cierre de sesión seguro. |
| **Usuarios** | `GET` | `/api/users/profile/` | Ver perfil del usuario autenticado. |
| | `PATCH` | `/api/users/profile/` | Actualizar perfil del usuario autenticado. |
| | `POST` | `/api/users/change-password/` | Cambiar contraseña. |
| **Pacientes** | `GET` | `/api/pacientes/` | Listar pacientes (soporta filtro `?status=` e `?search=`). |
| | `POST` | `/api/pacientes/` | Crear registro de paciente. |
| | `GET` | `/api/pacientes/{id}/` | Detalle del paciente (incluye IMC y seguimientos). |
| | `PUT`/`PATCH` | `/api/pacientes/{id}/` | Actualizar paciente. |
| | `DELETE` | `/api/pacientes/{id}/` | Eliminar paciente. |
| **Nutricionistas** | `GET` | `/api/nutricionistas/` | Listar nutricionistas. |
| | `POST` | `/api/nutricionistas/` | Crear nutricionista. |
| | `GET` | `/api/nutricionistas/{id}/` | Detalle (incluye cálculo de bono y experiencia). |
| **Planes Nutricionales**| `GET` | `/api/planes/` | Listar planes nutricionales. |
| | `POST` | `/api/planes/` | Crear plan nutricional (valida nombre único). |
| | `GET` | `/api/planes/stats/` | Estadísticas cuantitativas de planes activos/inactivos. |
| **Alimentos Programados**| `GET`| `/api/alimentos/` | Listar alimentos de planes. |
| | `POST` | `/api/alimentos/` | Agregar alimento programado a un plan activo. |
| | `POST` | `/api/alimentos/{id}/update-order/`| Cambiar secuencia del alimento (solo admin). |
| **Consultas** | `GET` | `/api/consultas/` | Listar consultas (pacientes solo ven las suyas). |
| | `GET` | `/api/consultas/mine/` | Ver citas propias del paciente autenticado. |
| | `POST` | `/api/consultas/{id}/start-consultation/`| Cambiar estado a `en_curso` al iniciar la cita. |

---

## 📁 Colección de Postman

El proyecto incluye el archivo **`dietetic_api_postman_collection.json`** en la raíz del espacio de trabajo.

Para importarlo y probar todos los endpoints:
1. Abre Postman o Thunder Client.
2. Haz clic en **Import** y selecciona el archivo `dietetic_api_postman_collection.json`.
3. Configura la variable de entorno `base_url` a `https://paz-dietetica.uaeftt-ute.site`.
4. Los endpoints están organizados secuencialmente en carpetas (desde el registro/login hasta las estadísticas y acciones avanzadas).
5. Tras el Login exitoso, copia el valor de `access` del cuerpo de la respuesta y guárdalo en la variable de colección `token` de Postman para autorizar las peticiones protegidas.
