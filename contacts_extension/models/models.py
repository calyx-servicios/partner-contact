from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.tools.safe_eval import safe_eval


class ResPartnerIdNumber(models.Model):

    _inherit = "res.partner.id_number"

    @api.constrains('name', 'category_id')
    def check(self):
        for rec in self:
            if rec.category_id.code == 'CUIT' and rec.name[0:2] in ['55', '51', '50']:
                return True
        super(ResPartnerIdNumber, self).check ()