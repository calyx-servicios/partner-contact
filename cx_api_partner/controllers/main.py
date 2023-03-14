import logging
from datetime import datetime

from odoo import http, models, fields, SUPERUSER_ID, _
from odoo.http import request
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


def translate_country(country: str) -> str:
    """Returns english value for Countries writen in Spanish

    Args:
        country (str): Country name in spanish

    Returns:
        str: Country name in English
    """
    translation_obj = request.env["ir.translation"].with_user(SUPERUSER_ID)
    domain = [
        ("module", "=", "base"),
        ("lang", "in", ["es_AR", "es_CL", "es_PY", "es_UY", "es"]),
        ("value", "=", country),
    ]
    translated_country = translation_obj.search(domain, limit=1)
    return translated_country.src if translated_country else country


def translate_identification_type(identification_type: str) -> str:
    """Returns english value for l10n_latam.identification.type writen in Spanish.

    Args:
        identification_type (str): identification_type name in spanish

    Returns:
        str: identification_type name in English
    """
    # possibly overkill since the only translated identification type is Passport
    translation_obj = request.env["ir.translation"].with_user(SUPERUSER_ID)
    domain = [
        ("module", "=", "l10n_latam_base"),
        ("lang", "in", ["es_AR", "es_CL", "es_PY", "es_UY", "es"]),
        ("value", "=", identification_type),
    ]
    translated_identification_type = translation_obj.search(domain, limit=1)
    return (
        translated_identification_type.src
        if translated_identification_type
        else identification_type
    )


def get_partner_values(data: dict) -> dict:
    """Prepares the values for partner creation

    * Name: Mandatory. [name]

    * Company: Mandatory (vat, name or id). [company]

    * Country: Mandatory (name or id). [country]

    * State: Optional [state]

    * City: Optional [city]

    * Street Name: Optional [street_name]

    * Zip Code: Optional [zip]

    * Street Name: Optional [street_name]

    * Phone: Optional [phone]

    * Mobile: Optional [mobile]

    * Email: Optional [email]

    * Website: Optional [website]

    * Category: Optional (name or id) [category]

    * Reference: Optional. Default is empty string. [ref]

    * Vat: Optional [vat]

    * Identification Type: Optional (name or id). Default is VAT. [journal]

    * Responsibility Type: Mandatory depending on the Country (name or id). [responsibility_type]

    * Is Company : Optional (True/False) [is_company]

    Args:
        data (dict): Data received from external service.

    Returns:
        dict: Values for partner creation
    """
    name = data.get("name")
    if not name:
        raise ValidationError("Name not found")

    company = data.get("company")
    if company:
        company = (
            request.env["res.company"]
            .sudo()
            .search([])
            .filtered(
                lambda c: c.vat == str(company)
                or c.name.lower() == str(company).lower()
                or c.id == company
            )
        )
    country = data.get("country")
    if not country:
        raise ValidationError("Country not found")
    if type(country) == str:
        country = translate_country(country)
    country = (
        request.env["res.country"]
        .sudo()
        .search([])
        .filtered(lambda c: c.name.lower() == str(country).lower() or c.id == country)
    )
    state = data.get("state")
    if state:
        state = (
            request.env["res.country.state"]
            .sudo()
            .search([("country_id", "=", country.id)])
            .filtered(lambda c: c.name.lower() == str(state).lower() or c.id == state)
        )

    category = data.get("category")
    if category:
        category = (
            request.env["res.partner.category"]
            .sudo()
            .search([])
            .filtered(lambda c: c.name.lower() == str(category).lower() or c.id == category)
        )

    values = {
        "name": name,
        "company_id": company.id if company else False,
        "ref": data.get("ref"),
        "country_id": country.id,
        "state_id": state.id if state else False,
        "street_name": data.get("street_name"),
        "zip": data.get("zip"),
        "phone": data.get("phone"),
        "mobile": data.get("mobile"),
        "email": data.get("email"),
        "website": data.get("website"),
        "category_id": category.id if category else False,
        "vat": str(data.get("vat")),
        "l10n_latam_identification_type_id": get_identification_type_id(data, country),
        "company_type": "company" if data.get("is_company") else "person",
    }
    responsability_type = get_responsability_type(data, country)
    if responsability_type:
        values.update(responsability_type)

    return values


def get_identification_type_id(data: dict, country: int) -> int:
    """Returns id for l10n_latam.identification_type_id according to country selected

    Args:
        data (dict): full external service request
        country (int): country_id recovered on get_partner_values()

    Raises:
        ValidationError: If an identification_type different than "VAT" is sent but not found
        (Error finding correct indentification type. Is localization installed?)

    Returns:
        int: l10n_latam.identification_type_id
    """
    identification_type = data.get("identification_type") or "VAT"
    translated_identification_type = translate_identification_type(identification_type)
    identification_type = (
        request.env["l10n_latam.identification.type"]
        .sudo()
        .search(["|", ("country_id", "=", country.id), ("country_id", "=", False)])
        .filtered(
            lambda c: c.name.lower() == str(identification_type).lower()
            or c.name.lower() == translated_identification_type.lower()
            or c.id == identification_type
        )
    )
    if not identification_type:
        raise ValidationError(
            "Error finding correct identification type. Is localization installed?"
        )

    return identification_type.id


def get_responsability_type(data: dict, country: models.Model) -> dict or None:
    """Finds correct responsibility type for Argentina (l10n_ar_afip_responsibility_type_id) or
     Chile (l10n_cl_sii_taxpayer_type).
     Method should be edited to support further localizations

    Args:
        data (dict): full external service request
        country (models.Model): country_id recovered on get_partner_values()

    Raises:
        ValidationError: Error ocurred while finding values

    Returns:
        dict or None: key/value pair to update creation dictionary
    """
    responsibility_type = data.get("responsibility_type")
    if not responsibility_type:
        return None
    try:
        if country.id == request.env.ref("base.ar").id:
            responsibility_type = (
                request.env["l10n_ar.afip.responsibility.type"]
                .with_user(SUPERUSER_ID)
                .search([])
                .filtered(
                    lambda r: r.id == responsibility_type
                    or r.name.lower() == str(responsibility_type).lower()
                )
            )
            return {"l10n_ar_afip_responsibility_type_id": responsibility_type.id}
        if country.id == request.env.ref("base.cl").id:
            cl_resp_dict = {
                "IVA afecto 1ra categoría": "1",
                "Emisor de boleta 2da categoria": "2",
                "Consumidor Final": "3",
                "Extranjero": "4",
            }
            if len(responsibility_type) > 1:
                responsibility_type = cl_resp_dict.get(responsibility_type)
            return {"l10n_cl_sii_taxpayer_type": str(responsibility_type)}
    except Exception as e:
        raise ValidationError(e)


def get_partner_id(field, value):
    partner_obj = request.env["res.partner"].with_user(SUPERUSER_ID)
    partner_id = partner_obj.search([(field, "=", value)])
    if len(partner_id) > 1:
        raise ValidationError("Multiple Partners Found")
    return partner_id


class ApiPartnerControllers(http.Controller):
    @http.route(
        "/contacts/create/partner",
        type="json",
        auth="jwt_cx_api_partner",
        methods=["POST"],
        website=True,
    )
    def create_partner(self, **kwargs):
        data = kwargs
        try:
            partner_id = get_partner_id("id", data.get("id"))
            if partner_id:
                values = get_partner_values(data)
                partner_id.write(values)
            else:
                partner_obj = request.env["res.partner"].with_user(SUPERUSER_ID)
                values = get_partner_values(data)
                partner_id = partner_obj.create(values)
            easy_access_fields = [
                "name",
                "country_id",
                "state_id",
                "l10n_latam_identification_type_id",
                "company_id",
                "company_type",
            ]
            if hasattr(partner_id, "l10n_ar_afip_responsibility_type_id"):
                easy_access_fields.append("l10n_ar_afip_responsibility_type_id")
            if hasattr(partner_id, "l10n_cl_sii_taxpayer_type"):
                easy_access_fields.append("l10n_cl_sii_taxpayer_type")
            return {"SUCCESS": partner_id.read(easy_access_fields)}
        except Exception as e:
            _logger.error(e)
            return {"ERROR": e}
