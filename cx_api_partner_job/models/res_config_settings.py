from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    api_base_url = fields.Char(related="company_id.api_base_url", readonly=False)
    api_endpoint = fields.Char(related="company_id.api_endpoint", readonly=False)
    api_audience = fields.Char(related="company_id.api_audience", readonly=False)
    api_issuer = fields.Char(related="company_id.api_issuer", readonly=False)
    api_key = fields.Char(related="company_id.api_key", readonly=False)
    api_timeout = fields.Integer(related="company_id.api_timeout", readonly=False)

    def set_values(self):
        super().set_values()
        # Values stored via related fields
        return True
