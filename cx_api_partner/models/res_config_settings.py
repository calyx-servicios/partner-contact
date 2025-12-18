from odoo import fields, models, api
from odoo.exceptions import ValidationError


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    contact_forward_enabled = fields.Boolean(
        string="Enable contact forwarding",
        related="company_id.contact_forward_enabled",
        readonly=False,
    )

    @api.constrains("contact_forward_enabled")
    def _check_forward_queue_module(self):
        """Validate that cx_api_partner_forward_queue module is installed before enabling"""
        for record in self:
            if record.contact_forward_enabled:
                # Check if cx_api_partner_forward_queue module is installed
                forward_queue_module = self.env["ir.module.module"].search(
                    [
                        ("name", "=", "cx_api_partner_forward_queue"),
                        ("state", "=", "installed"),
                    ]
                )
                if not forward_queue_module:
                    raise ValidationError(
                        "The module 'cx_api_partner_forward_queue' must be installed to enable contact forwarding. "
                        "Please install it first from the Apps menu."
                    )

    def execute(self):
        """Override execute to trigger constraint before saving"""
        self._check_forward_queue_module()
        return super().execute()
    