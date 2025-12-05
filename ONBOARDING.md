# 📚 On-boarding: Calyx Services Partner API

> Última actualización: 1 de diciembre de 2025  
> Generado por: GitHub Copilot On-boarding Assistant

---

##  Descripción General

### ¿Qué hace este proyecto?
Este repositorio contiene el módulo **`cx_api_partner`** para Odoo 13.0. Su objetivo es exponer un endpoint JSON-RPC protegido con JWT que permita a aplicaciones externas crear o actualizar registros de `res.partner` (contactos y compañías) dentro de Odoo sin necesidad de acceder a la interfaz. Enfoca especialmente necesidades de localizaciones de Argentina y Chile (tipos de identificación y responsabilidades fiscales), aunque la arquitectura admite extenderse a otros países.

El módulo añade un validador JWT dedicado, un usuario técnico con permisos de configuración y un controlador HTTP que se encarga de normalizar los datos entrantes (traducción de nombres de países, manejo de tipos de identificación, responsabilidad fiscal) antes de persistirlos. Está pensado para integrarse con herramientas corporativas o portales externos que administran cartera de clientes o partners y necesitan sincronizar información con Odoo.

### Tipo de Proyecto
- **Categoría**: Módulo Odoo (backend técnico)
- **Propósito**: Automatizar la creación/actualización de partners mediante API autenticada
- **Usuarios**: Desarrolladores Odoo, integradores externos y administradores funcionales que gestionan validadores JWT

### Información Clave
- **Repositorio**: https://github.com/calyx-servicios/partner-contact
- **Ambiente de producción**: No provisto en el repo (consultar a infraestructura)
- **Ambiente de staging**: No provisto
- **Documentación adicional**:
  - `README.rst` (uso básico y ejemplo de request)
  - `doc/changelog.rst`

---

## 🛠️ Stack Tecnológico

### Backend
- **Lenguaje**: Python 3 (Odoo 13.0)
- **Framework**: Odoo HTTP Controllers + ORM
- **ORM**: Odoo ORM
- **Autenticación**: JWT utilizando el módulo `auth_jwt`

### Frontend
- No aplica (no hay vistas ni assets incluidos)

### Base de Datos
- **Motor**: PostgreSQL (requerimiento estándar de Odoo 13)
- **Migraciones**: Administradas por Odoo (no hay scripts adicionales)

### Infraestructura
- **Containerización**: No definida; se puede integrar en instancias Odoo existentes
- **CI/CD**: No configurado en el repositorio
- **Hosting**: Dependiente del despliegue de Odoo (on-premise o nube)

### Herramientas de Desarrollo
- **Testing**: Se puede usar `odoo-bin --test-enable` (actualmente sin tests incluidos)
- **Linting**: Se observan cabeceras `pylint` (no hay config incluida)
- **Formatting**: Estilo estándar Odoo (PEP8)

---

## 🏗️ Arquitectura del Proyecto

### Patrón Arquitectónico
Arquitectura en capas simple típica de un módulo Odoo:
1. **HTTP Controller** (exposición del endpoint JSON)
2. **Helpers** (traducciones y normalización de datos)
3. **ORM** (creación/actualización de `res.partner` y localización)
4. **Datos declarativos** (usuarios técnicos y validador JWT)

### Diagrama de Arquitectura (ASCII)
```
[Cliente externo]
      |
      v
[JWT (auth.jwt.validator: cx_api_partner)]
      |
      v
[Controller ApiPartnerControllers.create_partner]
      |
      v
[Helpers (get_partner_values, translate_*)]
      |
      v
[Odoo ORM -> res.partner + l10n_ar/cl modelos]
```

### Capas de la Aplicación
1. **Capa de Presentación**: `controllers/main.py` define la ruta `/contacts/create/partner` (tipo JSON-RPC, autenticación JWT personalizada).
2. **Capa de Lógica de Negocio**: Funciones utilitarias en el mismo archivo normalizan datos, validan obligatoriedad y manejan responsabilidades fiscales.
3. **Capa de Acceso a Datos**: Interacciones con modelos estándar (`res.partner`, `res.country`, `l10n_latam.identification.type`, etc.) vía ORM.
4. **Capa de Infraestructura**: Archivos en `data/` crean usuario técnico y validador JWT; dependencias declaradas en `__manifest__.py`.

### Flujo de una Request Típica
```
Cliente → POST /contacts/create/partner
          (JWT Bearer)
            ↓
   Controller valida datos
            ↓
  Helpers traducen país/ID/responsabilidad
            ↓
  ORM crea/actualiza res.partner
            ↓
 Respuesta con campos clave o error
```

---

## 📁 Estructura de Directorios

```
cx_api_partner/
├── __init__.py                # Registra submódulos
├── __manifest__.py            # Metadatos, dependencias y datos cargados
├── README.rst                 # Guía de uso y ejemplo de consumo
├── controllers/
│   ├── __init__.py
│   └── main.py                # Controller + helpers del endpoint
├── models/
│   ├── __init__.py
│   └── res_config_settings.py # Campos de compañía + ajustes en General Settings
├── data/
│   ├── auth_jwt_validators.xml  # Validador JWT "cx_api_partner"
│   └── res_users_data.xml       # Usuario técnico y partner asociado
├── security/
│   └── ir.model.access.csv    # Permisos
├── views/
│   └── res_config_settings_views.xml  # Sección en Ajustes Generales
├── doc/
│   └── changelog.rst
├── i18n/
│   └── es.po                  # Traducciones al español
└── static/
    └── description/icon.png   # Icono para Apps

cx_api_partner_forward_queue/      # Módulo complementario (NUEVO)
├── __init__.py                     # Registra submódulos
├── __manifest__.py                 # Metadatos con dependencia a cx_api_partner
├── README.rst                      # Documentación de la cola de forwards
├── models/
│   ├── __init__.py
│   └── forward_queue.py            # Modelo para cola de requests
├── views/
│   └── forward_queue_views.xml     # Acciones y vistas para la cola
├── security/
│   └── ir.model.access.csv         # Permisos (solo admin)
├── i18n/
│   └── es.po                       # Traducciones al español
└── static/
    └── description/icon.png        # Icono para Apps
```

### Descripción de Carpetas Principales

#### `controllers/`
**Propósito**: Define los endpoints HTTP y funciones auxiliares.
**Archivos importantes**:
- `main.py`: Contiene `ApiPartnerControllers.create_partner` y helpers para traducir países/tipos de identificación, validar datos y escribir en `res.partner`.

#### `data/`
**Propósito**: Datos iniciales cargados al instalar el módulo.
**Archivos importantes**:
- `res_users_data.xml`: Crea el usuario técnico `jwt_cx_api_partner_static_user`.
- `auth_jwt_validators.xml`: Configura el validador `auth.jwt.validator` utilizado por el endpoint.

### Archivos de Configuración Clave
- **`__manifest__.py`**: Define dependencias (`base`, `contacts`, `auth_jwt`, `base_address_extended`) y datos a cargar.
- **`views/res_config_settings_views.xml`**: Expone los campos de configuración del reenvío (URL, JWT, timeout, reintentos) en Ajustes.
- **`.env`**: No incluido; el módulo aprovecha configuración estándar de Odoo.
- **`doc/changelog.rst`**: Historial (versión inicial 1.0.0).

### Módulo Complementario: `cx_api_partner_forward_queue`

**Propósito**: Gestionar una cola de requests pendientes de reenvío a endpoints externos.

**Archivos principales**:
- `models/forward_queue.py`: Modelo `cx_api_partner_forward_queue.forward_queue` que almacena requests fallidos con su estado (pending, success, failed, retry_pending).
- `views/forward_queue_views.xml`: Vistas tree, form y search para visualizar la cola (acceso solo para admin).
- `security/ir.model.access.csv`: Permisos restringidos a `base.group_system`.
- `i18n/es.po`: Traducciones completas al español.

**Relación con `cx_api_partner`**:
- Este módulo es una **dependencia recomendada** de `cx_api_partner`.
- Cuando el reenvío falla en `cx_api_partner`, se inserta un registro en esta cola en lugar de crear un log descartable.
- Preparado para integración futura con job scheduler de Odoo para reintentos automáticos.

---

## ⚙️ Configuración del Entorno

### Pre-requisitos
- Odoo 13.0 con Python 3.7+ y PostgreSQL 11+
- Módulos base: `base`, `contacts`, `auth_jwt`, `base_address_extended`
- Localizaciones opcionales pero recomendadas: `l10n_ar`, `l10n_cl`
- Acceso a la base de datos donde se instalará el módulo y privilegios para instalar módulos

### Variables de Entorno y Ajustes
No se requiere `.env` específico. Asegúrate de que la instancia Odoo tenga configuradas las credenciales habituales (`db_host`, `db_user`, etc.).

Configuraciones clave dentro de Odoo:

1. **JWT Validator** (`Usuarios y Compañías > JWT Validators > cx_api_partner`): define el secreto usado para validar las llamadas entrantes.
2. **Contact Forwarding** (`Ajustes > General Settings > Contact Forwarding`):
    - Habilita o deshabilita el reenvío cuando el payload incluye `contactos-redirect`.
    - Define `Forward Base URL`, `Forward Endpoint`, `JWT Audience`, `JWT Issuer` y `JWT Secret Key` para generar el JWT hacia el servicio destino.
    - Configura `Timeout`, `Enable Retries`, `Retry Attempts` y `Retry Backoff` (por defecto deshabilitado).
    - Los requests que fallan se encolan en **CX API Partner > Forward Queue** (solo visible para admin).
3. **Forward Queue** (`CX API Partner > Forward Queue`):
    - Visualización centralizada de todos los requests pendientes, fallidos o exitosos.
    - Solo accesible por administradores del sistema.
    - Preparado para integración futura con job scheduler para reintentos automáticos.

### Instalación Local

#### Opción 1: Integrado en instancia Odoo existente
```bash
# 1. Clonar el repo dentro de la ruta de addons
cd /opt/odoo/custom/addons
git clone https://github.com/calyx-servicios/partner-contact.git

# 2. Actualizar lista de apps
./odoo-bin -d <tu_db> -u base

# 3. Instalar el módulo
./odoo-bin -d <tu_db> -i cx_api_partner
```

#### Opción 2: Docker Compose Odoo (genérico)
```bash
# Asumiendo un stack de Odoo 13 ya preparado
git clone https://github.com/calyx-servicios/partner-contact.git addons/partner-contact
# Actualiza el archivo de configuración para añadir la ruta al addon
# Reinicia los servicios para cargar el módulo
```

### Configuración de Debugging en VS Code
No se incluye configuración `launch.json`. Se recomienda usar una sesión "Python: Remote Attach" apuntando al proceso `odoo-bin` con `--dev=all` para debugging.

---

## 🚀 Funcionalidades Principales

### 1. Creación/Actualización de Partners vía `/contacts/create/partner`
**Descripción**: Endpoint JSON-RPC autenticado con JWT que recibe datos básicos de empresas/personas, traduce nombres de países/estados, detecta responsabilidades fiscales y crea o actualiza un `res.partner` existente.
**Ubicación**: `controllers/main.py` → `ApiPartnerControllers.create_partner`
**Endpoints relacionados**:
- `POST /contacts/create/partner`

Snippet relevante:
```python
class ApiPartnerControllers(http.Controller):
    @http.route(
        "/contacts/create/partner",
        type="json",
        auth="jwt_cx_api_partner",
        methods=["POST"],
        website=True,
    )
    def create_partner(self, **kwargs):
        partner_id = get_partner_id("id", kwargs.get("id"))
        values = get_partner_values(kwargs)
        if partner_id:
            partner_id.write(values)
        else:
            partner_id = request.env["res.partner"].with_user(SUPERUSER_ID).create(values)
        return {"SUCCESS": partner_id.read(easy_access_fields)}
```

### 2. Reenvío configurable de requests
**Descripción**: Cuando la carga útil incluye `contactos-redirect` y el reenvío está habilitado en configuraciones, el módulo replica el request (headers/body/método) hacia una URL externa firmando un JWT propio. Maneja timeout, reintentos opcionales. Los requests fallidos se encolan en el módulo `cx_api_partner_forward_queue` para procesamiento posterior.
**Ubicación**: `controllers/main.py` (helpers de forward) + `models/res_config_settings.py` (configuración) + referencias a `cx_api_partner_forward_queue.forward_queue`.
**Cola de Reenvíos**: `cx_api_partner_forward_queue/models/forward_queue.py` (gestión centralizada de requests pendientes).

### 3. Traducción dinámica de países y tipos de identificación
**Descripción**: Funciones `translate_country` y `translate_identification_type` consultan `ir.translation` para mapear valores en español a claves en inglés antes de consultar `res.country` o `l10n_latam.identification.type`.
**Ubicación**: `controllers/main.py`

### 4. Resolución de responsabilidad fiscal según país
**Descripción**: `get_responsability_type` aplica reglas específicas de Argentina (`l10n_ar.afip.responsibility.type`) y Chile (`l10n_cl_sii_taxpayer_type`).
**Ubicación**: `controllers/main.py`

---

## 🔄 Flujos de Negocio Clave

### Flujo 1: Alta de Partner por servicio externo
**Descripción**: Aplicaciones externas registran un nuevo partner completando datos mínimos y autenticándose con JWT.
**Pasos**:
1. **Generación de token**: El sistema externo firma un JWT HS256 usando las credenciales configuradas en el validador `cx_api_partner`. → Referencia: `README.rst`.
2. **Invocación del endpoint**: Se envía `POST /contacts/create/partner` con `jsonrpc=2.0` y `params` que incluyen `name`, `country`, `vat`, `responsibility_type`, etc. → Archivo: `controllers/main.py`.
3. **Normalización y persistencia**: El controlador valida campos obligatorios, busca país/estado/categorías y crea o actualiza el registro. → Archivo: `controllers/main.py`.
4. **Respuesta**: Devuelve `SUCCESS` con campos esenciales (nombre, país, tipo de identificación, responsabilidades) o `ERROR` con el mensaje capturado.

Diagrama:
```
[App externa]
   ↓ (JWT)
/contacts/create/partner
   ↓
[get_partner_values]
   ↓
[res.partner ORM]
   ↓
Respuesta JSON
```

Código de ejemplo (desde README):
```python
TOKEN = jwt.encode({"aud": "cx_api_partner", "iss": "issuer", "exp": time.time() + 600, "email": "admin"}, key="secretkey", algorithm="HS256")
requests.post("http://localhost:8069/contacts/create/partner", json={
    "jsonrpc": "2.0",
    "params": {
        "name": "Chile Company SRL",
        "company": 5,
        "country": "Chile",
        "vat": "123456789",
        "identification_type": "RUT",
        "responsibility_type": "Emisor de boleta 2da categoria"
    }
}, headers={"Authorization": f"Bearer {TOKEN}"})
```

---

## 🗄️ Base de Datos

### Modelos Principales

#### Modelo: `res.partner`
**Ubicación**: Modelo estándar Odoo.
**Propósito**: Representa contactos y compañías.
**Campos principales usados**: `name`, `company_id`, `country_id`, `state_id`, `street_name`, `zip`, `vat`, `l10n_latam_identification_type_id`, `l10n_ar_afip_responsibility_type_id`, `l10n_cl_sii_taxpayer_type`, `company_type`.

#### Modelo: `auth.jwt.validator`
**Ubicación**: Módulo `auth_jwt`.
**Propósito**: Define parámetros del validador JWT que protege el endpoint.
**Campos relevantes**: `audience`, `issuer`, `signature_type`, `secret_algorithm`, `secret_key`, `user_id_strategy`, `static_user_id`.

#### Modelo: `res.users`
**Propósito**: Usuario técnico creado para ejecutar las operaciones asociadas al validador.

### Migraciones
- **Sistema**: Odoo maneja migraciones automáticamente.
- **Crear migración**: No aplica en este módulo.
- **Ejecutar migraciones**: Instalando/actualizando el módulo (`-i` / `-u`).

### Queries Importantes
Se interactúa únicamente mediante ORM; no hay SQL manual.

---

## 🔌 Integraciones Externas

### 1. JWT (auth_jwt_validator)
- **Propósito**: Autenticar llamadas externas usando tokens HS256.
- **Documentación**: https://github.com/OCA/server-auth/tree/13.0/auth_jwt
- **Autenticación**: JWT HS256 con `aud=issuer=cx_api_partner` por defecto.
- **Configuración**: Menu *Usuarios y Compañías → JWT Validators*. Registro creado automáticamente (`data/auth_jwt_validators.xml`) con secretos que deben rotarse en producción.
- **Ubicación en código**: `__manifest__.py` (dependencia) y `controllers/main.py` (decorador `auth="jwt_cx_api_partner"`).
- **Limitaciones conocidas**: El secreto y emisor se cargan desde XML; es imprescindible modificarlos tras la instalación para evitar fugas.

### 2. Localizaciones l10n_ar / l10n_cl
- **Propósito**: Resolver responsabilidades fiscales y tipos de identificación.
- **Configuración**: Deben estar instaladas para que los modelos `l10n_ar.afip.responsibility.type` y campos `l10n_cl_sii_taxpayer_type` existan.
- **Limitaciones**: Si no están presentes, `get_responsability_type` puede fallar; se captura con `ValidationError`.

---

## 🧪 Testing

### Estructura de Tests
No existen directorios de tests en el repositorio.

### Ejecutar Tests
```bash
# Todos los tests del módulo (si se agregan en el futuro)
odoo-bin -d <db> -i cx_api_partner --test-enable
```

### Cobertura Actual
- **Líneas cubiertas**: 0% (sin tests)
- **Objetivo recomendado**: Agregar pruebas unitarias/integración mínimas sobre helpers y endpoint

### Escribir Tests
- Crear carpeta `tests/` siguiendo convenciones Odoo (`tests/test_partner_api.py`).
- Usar `HttpCase` para probar el endpoint y `TransactionCase` para helpers.

---

## 📐 Convenciones y Buenas Prácticas

### Naming Conventions
- Variables y funciones: `snake_case`
- Clases: `PascalCase`
- Constantes: `UPPER_SNAKE_CASE`
- Archivos: `snake_case` (excepto manifiestos estándar)

### Estructura de Código
1. Imports estándar de Python
2. Imports Odoo
3. Constantes / logger
4. Helpers
5. Clases de controller

### Comentarios y Documentación
- Docstrings detallados en helpers (`translate_country`, `get_partner_values`, etc.)
- Mantener comentarios en español/inglés coherentes (proyecto está mixto)

### Manejo de Errores
- Uso de `ValidationError` para entradas inválidas
- `try/except` en el controller para devolver `{"ERROR": e}` y `rollback`

### Git Workflow
- Repositorio de la organización Calyx (seguir políticas internas)
- Convención sugerida para ramas: `feature/<tema>`, `fix/<tema>`
- Commits siguiendo estilo `feat: ...`, `fix: ...`

---

## 🔧 Troubleshooting Común

### JWT inválido
**Síntomas**: Respuesta 401 antes de llegar al controller.
**Causa**: Audiencia/issuer/secret no coinciden con el validador `cx_api_partner`.
**Solución**: Revisar configuración en *Usuarios y Compañías → JWT Validators* y regenerar token con los nuevos parámetros.

### Error "Name not found" o "Country not found"
**Síntomas**: Respuesta `{"ERROR": ValidationError('Name not found')}`.
**Causa**: Falta `params.name` o `params.country`.
**Solución**: Validar payload JSON-RPC y asegurar que `country` sea nombre o ID existente.

### "Error finding correct identification type"
**Síntomas**: ValidationError al usar `identification_type` distinto de "VAT".
**Causa**: Localizaciones no instaladas o valor mal escrito.
**Solución**: Instalar `l10n_latam_base` + localización correspondiente y confirmar que el string coincide con la traducción inglesa.

### Múltiples partners encontrados
**Síntomas**: ValidationError("Multiple Partners Found").
**Causa**: Búsqueda por campo (`id`, `vat`, etc.) devolvió más de un registro.
**Solución**: Ajustar criterio de búsqueda o limpiar datos duplicados.

---

## 📚 Recursos Adicionales
- **README del módulo**: `cx_api_partner/README.rst`
- **Changelog**: `cx_api_partner/doc/changelog.rst`
- **Documentación auth_jwt (OCA)**: https://github.com/OCA/server-auth/tree/13.0/auth_jwt
- **API JWT (pyjwt/jose)**: https://python-jose.readthedocs.io/

---

## 👥 Contactos y Soporte

### Equipo de Desarrollo
- **Tech Lead / Maintainer**: Marco Oegg (Calyx Servicios S.A.)
- **Organización**: Calyx Servicios S.A. (https://odoo.calyx-cloud.com.ar/)

### Para Nuevos Desarrolladores
1. ✅ Leer este documento y el `README.rst`
2. ✅ Configurar entorno Odoo 13 con el módulo instalado
3. ✅ Probar el endpoint desde un script o herramienta (Postman)
4. ✅ Revisar helpers en `controllers/main.py`
5. ✅ Identificar oportunidades de pruebas automatizadas
6. ✅ Participar de dailies y revisar backlog relacionado a integraciones

Preguntas frecuentes: consultar canal interno de Calyx (Slack/Teams) correspondiente a Odoo Integrations.

---

## 🎯 Siguientes Pasos
1. **Setup inicial**: Instala el módulo en un ambiente de desarrollo y actualiza los secretos del validador JWT.
2. **Explora el código**: Navega `controllers/main.py` y entiende cada helper.
3. **Ejecuta pruebas manuales**: Reproduce el script del README y valida la aplicación en Odoo.
4. **Agrega tests**: Considera escribir casos para traducciones y responsabilidad fiscal.
5. **Propón mejoras**: Documenta features pendientes (soporte para más países, categorías, etc.).
6. **Únete al equipo**: Coordina con el Tech Lead para tu primera tarea (ej. extender el endpoint o agregar validaciones).

---

*Este documento debe actualizarse ante cualquier cambio funcional o de infraestructura.*
