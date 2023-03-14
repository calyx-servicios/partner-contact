# pylint: disable=missing-module-docstring,pointless-statement
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Calyx Services Partner API",
    "summary": """
        This module allows to integrate external services to create Partners.
        This module works with l10n_ar,l10n_cl yet does not depend on them
    """,
    "author": "Calyx Servicios S.A.",
    "maintainers": ["marcooegg"],
    "website": "https://odoo.calyx-cloud.com.ar/",
    "license": "AGPL-3",
    "category": "Technical Settings",
    "version": "13.0.1.0.0",
    "development_status": "Production/Stable",
    "application": False,
    "installable": True,
    "external_dependencies": {
        "python": [],
        "bin": [],
    },
    "depends": ["base", "contacts", "auth_jwt","base_address_extended"],
    'data': [
        'data/res_users_data.xml',
        'data/auth_jwt_validators.xml',
    ],
}
