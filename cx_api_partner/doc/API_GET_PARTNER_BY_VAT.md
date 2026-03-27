# API: Consulta de Partner por VAT/CUIT

## Descripción General

Este endpoint permite consultar la información de un partner (contacto/empresa) mediante su número de VAT/CUIT.

---

## Endpoint

```
GET /contacts/partner/by-vat
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

## Formato de Request (JSON-RPC 2.0)

El endpoint utiliza el protocolo JSON-RPC 2.0. El cuerpo del request debe tener la siguiente estructura:

```json
{
  "jsonrpc": "2.0",
  "params": {
    "vat": "23908677064"
  }
}
```

### Parámetros en `params`

| Parámetro | Tipo | Requerido | Descripción |
|-----------|------|-----------|-------------|
| `vat` | string | Sí | Número de VAT/CUIT del partner a consultar |

---

## Respuesta Exitosa (JSON-RPC 2.0)

### HTTP Status: 200 OK

```json
{
  "jsonrpc": "2.0",
  "id": null,
  "result": {
    "SUCCESS": {
      "id": 42,
      "name": "ABSHIRE, RORY",
      "vat": "23908677064",
      "country": "Argentina",
      "state": "Buenos Aires",
      "street": "Avenida Santa Fe 1234",
      "street_name": "Avenida Santa Fe 1234",
      "zip": "C1425BGK",
      "phone": false,
      "email": "Trycia30@gmail.com",
      "company_type": "company",
      "identification_type": "CUIT",
      "afip_responsibility_type": "Consumidor Final"
    }
  }
}
```

### Campos de la Respuesta

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | integer | ID interno del partner en Odoo |
| `name` | string | Nombre del partner |
| `vat` | string | Número de VAT/CUIT |
| `country` | string | Nombre del país |
| `state` | string | Nombre de la provincia/estado |
| `street` | string | Dirección completa guardada en Odoo (`street`) |
| `street_name` | string | Dirección completa guardada en Odoo (`street`) |
| `zip` | string | Código postal |
| `phone` | string \| false | Teléfono (puede ser `false` si no está definido) |
| `email` | string \| false | Correo electrónico (puede ser `false` si no está definido) |
| `company_type` | string | Tipo: `"company"` o `"person"` |
| `identification_type` | string | Tipo de identificación (ej: "CUIT", "DNI", "Passport") |
| `afip_responsibility_type` | string | **(Solo Argentina)** Tipo de responsabilidad AFIP |
| `sii_taxpayer_type` | string | **(Solo Chile)** Tipo de contribuyente SII |

---

## Respuestas de Error (JSON-RPC 2.0)

### VAT no proporcionado

```json
{
  "jsonrpc": "2.0",
  "id": null,
  "result": {
    "ERROR": "VAT not provided"
  }
}
```

### Partner no encontrado

```json
{
  "jsonrpc": "2.0",
  "id": null,
  "result": {
    "ERROR": "Partner not found"
  }
}
```

### Error de autenticación

**HTTP Status: 401 Unauthorized**

Si el token JWT es inválido o ha expirado.

---

## Ejemplos de Uso

### cURL

```bash
curl -X GET "https://your-odoo-instance.com/contacts/partner/by-vat" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "params": {
      "vat": "23908677064"
    }
  }'
```

### Python (requests)

```python
import requests
import json

url = "https://your-odoo-instance.com/contacts/partner/by-vat"
headers = {
    "Authorization": "Bearer YOUR_JWT_TOKEN",
    "Content-Type": "application/json"
}
data = {
    "jsonrpc": "2.0",
    "params": {
        "vat": "23908677064"
    }
}

response = requests.get(url, headers=headers, json=data)
result = response.json()

if "result" in result and "SUCCESS" in result["result"]:
    partner = result["result"]["SUCCESS"]
    print(f"Partner encontrado: {partner['name']}")
    print(f"Email: {partner['email']}")
elif "result" in result and "ERROR" in result["result"]:
    print(f"Error: {result['result']['ERROR']}")
else:
    print(f"Error inesperado: {result}")
```

### JavaScript (fetch)

```javascript
const url = "https://your-odoo-instance.com/contacts/partner/by-vat";
const token = "YOUR_JWT_TOKEN";

const data = {
  jsonrpc: "2.0",
  params: {
    vat: "23908677064"
  }
};

fetch(url, {
  method: "GET",
  headers: {
    "Authorization": `Bearer ${token}`,
    "Content-Type": "application/json"
  },
  body: JSON.stringify(data)
})
  .then(response => response.json())
  .then(result => {
    if (result.result && result.result.SUCCESS) {
      console.log("Partner encontrado:", result.result.SUCCESS);
    } else if (result.result && result.result.ERROR) {
      console.error("Error:", result.result.ERROR);
    } else {
      console.error("Error inesperado:", result);
    }
  })
  .catch(error => console.error("Error de conexión:", error));
```

---

## Casos de Uso

Este endpoint es útil para:

1. **Validación de datos**: Verificar si un partner ya existe antes de crear uno nuevo
2. **Sincronización**: Comparar datos locales con los de Odoo para detectar cambios
3. **Consulta de información**: Obtener datos actualizados de un partner conocido
4. **Integración con sistemas externos**: Permitir que otros sistemas consulten información de partners

---

## Notas Importantes

### Protocolo JSON-RPC 2.0

Este endpoint utiliza el estándar **JSON-RPC 2.0**:
- Todos los requests deben incluir `"jsonrpc": "2.0"` y los parámetros en `"params"`
- Todas las respuestas incluyen `"jsonrpc": "2.0"`, `"id": null` y el resultado en `"result"`
- Para acceder a los datos, debe usar `response.result.SUCCESS` o `response.result.ERROR`

### Localización

- Los campos `afip_responsibility_type` y `sii_taxpayer_type` solo aparecen si el módulo de localización correspondiente está instalado
- **Argentina**: Requiere `l10n_ar` instalado para `afip_responsibility_type`
- **Chile**: Requiere `l10n_cl` instalado para `sii_taxpayer_type`

### Formato de VAT

- El VAT debe proporcionarse tal como está almacenado en Odoo
- No se realiza normalización automática (sin guiones, espacios, etc.)
- Ejemplo: `"30123456789"` no `"30-12345678-9"`

### Múltiples Partners

- Si existen múltiples partners con el mismo VAT, el endpoint devuelve solo el primero encontrado
- Se recomienda mantener valores de VAT únicos en el sistema

---

## Relación con Otros Endpoints

### POST /contacts/create/partner

El endpoint de creación/actualización de partners permite modificar la información. Use este endpoint GET para:

1. Verificar el estado actual antes de actualizar
2. Comparar qué campos han cambiado
3. Decidir si es necesario llamar al endpoint POST

**¿Cuándo usar cada uno?**

- **GET /contacts/partner/by-vat**: Para consultar información existente
- **POST /contacts/create/partner**: Para crear o actualizar información

---

## Soporte

Para más información sobre el módulo `cx_api_partner`, consulte el README principal del módulo.
