import logging
from datetime import datetime

from odoo import http, models, fields, SUPERUSER_ID, _
from odoo.http import request
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


def translate_country(country: str) -> str:
    translation_obj = request.env["ir.translation"].with_user(SUPERUSER_ID)
    domain = [
        ("module", "=", "base"),
        ("lang", "in", ["es_AR", "es_CL", "es_PY", "es_UY", "es"]),
        ("value", "=", country),
    ]
    translated_country = translation_obj.search(domain, limit=1)
    return translated_country.src if translated_country else country


def get_partner_values(data: dict) -> dict:
    """Prepares the values for partner creation

    Args:
        data (dict): Data received from external service.

    Returns:
        dict: Values for partner creation
    """
    name = data.get("name")
    if not name:
        raise ValidationError("Name not found")

    company = data.get("company")
    if not company:
        raise ValidationError("Company not found")
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
    _logger.info(country)
    country = (
        request.env["res.country"]
        .sudo()
        .search([])
        .filtered(lambda c: c.name.lower() == str(country).lower() or c.id == country)
    )
    state = data.get("state")
    if state:
        state = (
            request.env["res.state"]
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
            .filtered(
                lambda c: c.name.lower() == str(category).lower() or c.id == category
            )
        )

    values = {
        "name": name,
        "company_id": company.id,
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
    }
    _logger.info(values)
    responsability_type = get_responsability_type(data, country)
    if responsability_type:
        values.update(responsability_type)

    return values


def get_identification_type_id(data: dict, country: int) -> int:
    identification_type = data.get("identification_type")
    if not identification_type:
        raise ValidationError("identification_type not found")
    identification_type = (
        request.env["l10n_latam.identification.type"]
        .sudo()
        .search(["|", ("country_id", "=", country.id), ("country_id", "=", False)])
        .filtered(
            lambda c: c.name.lower() == str(identification_type).lower()
            or c.id == identification_type
        )
    )
    if not identification_type:
        raise ValidationError(
            "Error finding correct identification type. Is localization installed?"
        )

    return identification_type.id


def get_responsability_type(data: dict, country: models.Model) -> dict or None:
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
                    or r.name.lower() == responsibility_type.lower()
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
            if type(responsibility_type) == str:
                responsibility_type = cl_resp_dict.get(responsibility_type)
            return {"l10n_cl_sii_taxpayer_type": responsibility_type}
    except Exception as e:
        raise ValidationError(e)


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
            values = get_partner_values(data)
            partner_id = (
                request.env["res.partner"].with_user(SUPERUSER_ID).create(values)
            )
            easy_access_fields = [
                "name",
                "country_id",
                "state_id",
                "l10n_latam_identification_type_id",
                "company_id",
            ]
            return {"SUCCESS": partner_id.read(easy_access_fields)}
        except Exception as e:
            _logger.error(e)
            return {"ERROR": e}
