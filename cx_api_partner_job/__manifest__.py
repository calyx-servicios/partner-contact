# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Calyx Partner API Forward Queue Job",
    "summary": "Processes pending forward queue entries and sends them to external API",
    "version": "13.0.1.0",
    "author": "Calyx Servicios S.A.",
    "website": "https://odoo.calyx-cloud.com.ar/",
    "license": "AGPL-3",
    "category": "Technical Settings",
    "depends": ["cx_api_partner", "cx_api_partner_forward_queue"],
    "data": [
        "data/ir_cron.xml",
        "security/ir.model.access.csv",
        "views/res_config_settings_views.xml",
    ],
    "i18n": [
        "i18n/es_AR.po",
    ],
    "installable": True,
}
