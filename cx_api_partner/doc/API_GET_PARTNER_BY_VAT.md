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

## Parámetros

### Query Parameters / JSON Body

| Parámetro | Tipo | Requerido | Descripción |
|-----------|------|-----------|-------------|
| `vat` | string | Sí | Número de VAT/CUIT del partner a consultar |

---

## Respuesta Exitosa

### HTTP Status: 200 OK

```json
{
  "SUCCESS": {
    "id": 123,
    "name": "Empresa XYZ S.A.",
    "vat": "30123456789",
    "country": "Argentina",
    "state": "Buenos Aires",
    "street_name": "Av. Corrientes",
    "zip": "1043",
    "phone": "+54 11 4321-8765",
    "email": "contacto@empresa.com",
    "company_type": "company",
    "identification_type": "CUIT",
    "afip_responsibility_type": "Responsable Inscripto"
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
| `street_name` | string | Nombre de la calle |
| `zip` | string | Código postal |
| `phone` | string | Teléfono |
| `email` | string | Correo electrónico |
| `company_type` | string | Tipo: `"company"` o `"person"` |
| `identification_type` | string | Tipo de identificación (ej: "CUIT", "DNI", "Passport") |
| `afip_responsibility_type` | string | **(Solo Argentina)** Tipo de responsabilidad AFIP |
| `sii_taxpayer_type` | string | **(Solo Chile)** Tipo de contribuyente SII |

---

## Respuestas de Error

### VAT no proporcionado

```json
{
  "ERROR": "VAT not provided"
}
```

### Partner no encontrado

```json
{
  "ERROR": "Partner not found"
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
    "vat": "30123456789"
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
    "vat": "30123456789"
}

response = requests.get(url, headers=headers, json=data)
result = response.json()

if "SUCCESS" in result:
    partner = result["SUCCESS"]
    print(f"Partner encontrado: {partner['name']}")
    print(f"Email: {partner['email']}")
else:
    print(f"Error: {result.get('ERROR')}")
```

### JavaScript (fetch)

```javascript
const url = "https://your-odoo-instance.com/contacts/partner/by-vat";
const token = "YOUR_JWT_TOKEN";

const data = {
  vat: "30123456789"
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
    if (result.SUCCESS) {
      console.log("Partner encontrado:", result.SUCCESS);
    } else {
      console.error("Error:", result.ERROR);
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
