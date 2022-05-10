# pylint: disable=missing-module-docstring,pointless-statement
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{

    "name": "Argentinian Accountability translations",
    "summary": """
        This Module contains custom translations for the
        Argentinian Accountability.
    """,
    "author": "Calyx Servicios S.A.",
    "maintainers": ["lucianobaleani"],
    "website": "https://odoo.calyx-cloud.com.ar/",
    "license": "AGPL-3",

    "category": "Technical Settings",
    "version": "11.0.1.0.0",

    "development_status": "Production/Stable",
    "application": False,
    "installable": True,
    "external_dependencies": {
        "python": [],
        "bin": [],
    },

    "depends": [ "base", "contacts", "l10n_ar_partner","l10n_ar_account"],

    'data': [
        "views/l10n_ar_account_partner_views.xml",
    ],

}
