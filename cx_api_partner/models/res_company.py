from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    contact_forward_enabled = fields.Boolean(
        string="Contact forwarding enabled",
        default=False,
    )

    def get_contact_forward_settings(self):
        """
        Returns a dictionary with contact forwarding settings.
        
        Returns:
            dict: Dictionary with 'enabled' key indicating if forwarding is active
        """
        return {
            "enabled": self.contact_forward_enabled,
        }
