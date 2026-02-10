# API: Crear o Actualizar Partner

## Descripción General

Este endpoint permite crear un nuevo partner (contacto/empresa) o actualizar uno existente en el sistema. Los datos se procesan validando información obligatoria y realizando búsquedas de registros relacionados según el país especificado.

---

## Endpoint

```
POST /contacts/create/partner
```

---

## Autenticación

Este endpoint requiere autenticación mediante **JWT** con el validador `jwt_cx_api_partner`.

### Headers requeridos:

```
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json
```

---

## Formato de Solicitud

El endpoint utiliza el formato **JSON-RPC 2.0**. La solicitud debe incluir la estructura estándar.

### Estructura General

```json
{
  "jsonrpc": "2.0",
  "params": {
    // parámetros aquí
  }
}
```

---

## Parámetros de Entrada

### Body (JSON) - dentro de `params`

| Parámetro | Tipo | Requerido | Descripción |
|-----------|------|-----------|-------------|
| `name` | string | **Sí** | Nombre del partner (persona o empresa) |
| `country` | string/integer | **Sí** | País. Puede ser el nombre del país o su ID en el sistema |
| `vat` | string | No | Número de VAT/CUIT/RFC del partner |
| `company` | string/integer | No | Empresa asociada. Puede ser VAT, nombre de empresa o ID |
| `state` | string/integer | No | Estado/Provincia/Región. Nombre o ID |
| `city` | string | No | **[IGNORADO POR EL SISTEMA]** Campo aceptado pero no procesado actualmente |
| `street_name` | string | No | Nombre de la calle |
| `street_number` | string | No | Número de calle |
| `street_number2` | string | No | Número de calle complementario |
| `zip` | string | No | Código postal |
| `phone` | string | No | Teléfono |
| `mobile` | string | No | Teléfono móvil |
| `email` | string | No | Correo electrónico |
| `website` | string | No | Sitio web |
| `ref` | string | No | Referencia o código interno del partner |
| `identification_type` | string/integer | No | Tipo de identificación (Ej: "VAT", "CUIT", "Passport"). Por defecto: "VAT" |
| `responsibility_type` | string/integer | No | Tipo de responsabilidad fiscal AFIP (obligatorio para empresas en Argentina) |
| `is_company` | boolean | No | Indica si el partner es una empresa (true) o persona (false). Por defecto: false |
| `id` | integer | No | ID del partner existente para actualizar. Si se proporciona, se actualiza en lugar de crear |

---

## Parámetros de Salida

### Respuesta Exitosa

#### HTTP Status: 200 OK

```json
{
  "jsonrpc": "2.0",
  "id": null,
  "result": {
    "SUCCESS": [
      {
        "id": 1459,
        "name": "Empresa ABC S.A.",
        "country_id": [10, "Argentina"],
        "state_id": [5, "Buenos Aires"],
        "l10n_latam_identification_type_id": [4, "CUIT (AR)"],
        "company_id": [5, "Mi Empresa"],
        "company_type": "company",
        "l10n_ar_afip_responsibility_type_id": [1, "IVA Responsable Inscripto"]
      }
    ]
  }
}
```

**Estructura de respuesta:**

| Campo | Descripción |
|-------|-------------|
| `jsonrpc` | Versión del protocolo JSON-RPC (siempre "2.0") |
| `id` | Identificador de la solicitud (normalmente null) |
| `result` | Objeto con la respuesta de la API |
| `result.SUCCESS` | Array con un objeto contendo los datos del partner creado o actualizado |

**Descripción de campos del partner (dentro de SUCCESS):**

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | integer | ID único del partner creado o actualizado |
| `name` | string | Nombre del partner |
| `country_id` | array | [ID, Nombre] del país |
| `state_id` | array/false | [ID, Nombre] del estado/provincia, o false si no tiene |
| `l10n_latam_identification_type_id` | array | [ID, Nombre] del tipo de identificación |
| `company_id` | array/false | [ID, Nombre] de la empresa asociada, o false si no tiene |
| `company_type` | string | Tipo de entidad: "company" (empresa) o "person" (persona) |
| `l10n_ar_afip_responsibility_type_id` | array/false | [ID, Nombre] del tipo de responsabilidad AFIP, o false si no tiene |

---

### Respuesta con Error

#### HTTP Status: 200 OK (la API devuelve 200 incluso en errores)

```json
{
  "jsonrpc": "2.0",
  "id": null,
  "result": {
    "ERROR": "Descripción del error"
  }
}
```

**Posibles errores:**

| Mensaje de Error | Causa |
|-----------------|-------|
| `Name not found` | El parámetro `name` no fue proporcionado |
| `Country not found` | El país no se encontró en el sistema o no fue proporcionado |
| `Multiple Partners Found` | Se encontraron múltiples partners con el criterio de búsqueda |
| `Error finding correct identification type. Is localization installed?` | El tipo de identificación no existe o la localización no está instalada |
| Otro mensaje de error | Validación fallida o error interno del sistema |

---

## Ejemplos de Uso

### Ejemplo 1: Crear una Empresa en Argentina con Categoría

```bash
curl -X POST https://api.ejemplo.com/contacts/create/partner \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "params": {
      "name": "NANCY MARICEL KATO",
      "country": "Argentina",
      "vat": "27317997952",
      "identification_type": "CUIT",
      "company": "27317997952",
      "email": "farmaciakato@gmail.com",
      "phone": "+542213040105",
      "mobile": "+542213040105",
      "street_name": "Calle 186 esq. 475",
      "state": "Buenos Aires",
      "zip": "B1903",
      "responsibility_type": "IVA Responsable Inscripto",
      "is_company": true,
      "id": 187193
    }
  }'
```

**Respuesta esperada:**
```json
{
  "jsonrpc": "2.0",
  "id": null,
  "result": {
    "SUCCESS": [
      {
        "id": 187193,
        "name": "NANCY MARICEL KATO",
        "country_id": [10, "Argentina"],
        "state_id": [5, "Buenos Aires"],
        "l10n_latam_identification_type_id": [4, "CUIT (AR)"],
        "company_id": [5, "Mi Empresa"],
        "company_type": "company",
        "l10n_ar_afip_responsibility_type_id": [1, "IVA Responsable Inscripto"]
      }
    ]
  }
}
```

---

### Ejemplo 2: Crear una Persona con Contacto Simple

```bash
curl -X POST https://api.ejemplo.com/contacts/create/partner \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "params": {
      "name": "Juan Perez",
      "country": "Argentina",
      "vat": "20123456789",
      "identification_type": "DNI",
      "state": "Buenos Aires",
      "email": "juan@ejemplo.com",
      "phone": "+54 221 1234567",
      "is_company": false
    }
  }'
```

**Respuesta esperada:**
```json
{
  "jsonrpc": "2.0",
  "id": null,
  "result": {
    "SUCCESS": [
      {
        "id": 789,
        "name": "Juan Perez",
        "country_id": [10, "Argentina"],
        "state_id": [5, "Buenos Aires"],
        "l10n_latam_identification_type_id": [3, "DNI"],
        "company_id": false,
        "company_type": "person"
      }
    ]
  }
}
```

---

### Ejemplo 3: Actualizar un Partner Existente

```bash
curl -X POST https://api.ejemplo.com/contacts/create/partner \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "params": {
      "id": 187193,
      "phone": "+542213040105",
      "mobile": "+542213040105",
      "email": "nuevomail@gmail.com",
      "street_name": "Calle 186 esq. 487"
    }
  }'
```

**Respuesta esperada:**
```json
{
  "jsonrpc": "2.0",
  "id": null,
  "result": {
    "SUCCESS": [
      {
        "id": 187193,
        "name": "NANCY MARICEL KATO",
        "country_id": [10, "Argentina"],
        "state_id": [5, "Buenos Aires"],
        "l10n_latam_identification_type_id": [4, "CUIT (AR)"],
        "company_id": [5, "Mi Empresa"],
        "company_type": "company",
        "l10n_ar_afip_responsibility_type_id": [1, "IVA Responsable Inscripto"]
      }
    ]
  }
}
```

---

## Notas Importantes

### Validación de Requisitos

- El parámetro `responsibility_type` es requerido para empresas en Argentina

### Búsqueda de Registros

- Los parámetros como `country`, `state`, `company` pueden especificarse tanto por **ID** como por **nombre**
- La búsqueda por nombre es **case-insensitive**
- Si se proporciona un `id` para actualización, se buscará primero un partner con ese ID

### Criterio de Actualización

- Si proporciona el parámetro `id`, el sistema actualizará el partner existente
- Si no proporciona `id` pero la configuración de la empresa está habilitada, se intentará buscar por `vat` o `id` según la configuración

### Formato JSON-RPC 2.0

Todas las solicitudes al endpoint deben incluir la envolvente JSON-RPC 2.0 con:
- `jsonrpc`: Siempre debe ser "2.0"
- `params`: Objeto JSON con los parámetros del partner (ver tabla anterior)

### Campos No Soportados

Algunos campos pueden ser incluidos en la solicitud pero **no son procesados por el sistema**:

- **`city`**: Se acepta en la solicitud pero se ignora. Use `state` para ubicación geográfica.
- **`category`**: No está soportado actualmente. Esta funcionalidad está deshabilitada en el código.

---

## Consideraciones de Integración

1. **Formato JSON-RPC 2.0**: Asegúrese de enviar la solicitud dentro de la estructura `{"jsonrpc": "2.0", "params": {...}}`
2. **Almacenar JWT Token**: Obtenga un token JWT válido con autenticación `jwt_cx_api_partner` y úselo en el header `Authorization`
3. **Validar Datos Antes de Enviar**: Asegúrese de que los datos obligatorios (`name`, `country`) sean enviados
4. **Manejar Errores**: Implemente lógica para procesar respuestas de error y reintentos si es necesario
5. **Tipo de Responsabilidad (Argentina)**: Los valores válidos de `responsibility_type` son: "IVA Responsable Inscripto", "IVA Responsable No Inscripto", "Monotributista", etc. Consulte con el equipo de administración sobre los valores disponibles en su sistema.

---

## Soporte

Para consultas técnicas sobre la integración, contacte al equipo de soporte técnico con:
- Ejemplos de las peticiones que genere
- Mensajes de error recibidos (si aplica)
- Información sobre el país y tipo de localización que utiliza
