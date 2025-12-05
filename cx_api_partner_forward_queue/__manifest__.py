{
    "name": "API Partner - Forward Queue",
    "version": "13.0.1.0",
    "category": "Tools",
    "author": "Calyx Servicios",
    "website": "https://odoo.calyx-cloud.com.ar/",
    "license": "AGPL-3",
    "depends": ["cx_api_partner"],
    "data": [
        "security/ir.model.access.csv",
        "views/forward_queue_views.xml",
        "views/menus.xml",
    ],
    "i18n": [
        "i18n/es_AR.po",
    ],
    "installable": True,
    "auto_install": False,
    "application": True,
    "sequence": 1,
    "images": [
        "static/description/icon.png"
    ],
}
