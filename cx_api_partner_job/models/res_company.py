from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    api_base_url = fields.Char(string="Forward API Base URL")
    api_endpoint = fields.Char(string="Forward API Endpoint")
    api_audience = fields.Char(string="Forward API Audience")
    api_issuer = fields.Char(string="Forward API Issuer")
    api_key = fields.Char(string="Forward API Key")
    api_timeout = fields.Integer(string="Forward API Timeout (s)", default=120)
