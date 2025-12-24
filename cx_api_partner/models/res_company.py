from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    contact_forward_enabled = fields.Boolean(
        string="Contact forwarding enabled",
        default=False,
    )
    
    contact_forward_by_vat = fields.Boolean(
        string="Forward updates by VAT",
        default=False,
        help="When enabled, the 'id' field will be removed from forwarded payloads, "
             "forcing the external system to search/update by VAT instead of ID. "
             "Use this for systems like Metafar that identify contacts by VAT.",
    )

    def write(self, vals):
        """Log when contact_forward_enabled is changed"""
        for record in self:
            if "contact_forward_enabled" in vals:
                old_value = record.contact_forward_enabled
                new_value = vals["contact_forward_enabled"]
                
                if old_value != new_value:
                    action = "enabled" if new_value else "disabled"
                    message = f"Contact forwarding {action} for company {record.name}"
                    self.env["ir.logging"].create({
                        "name": "Contact Forwarding",
                        "type": "client",
                        "dbname": self.env.cr.dbname,
                        "level": "INFO",
                        "message": message,
                        "path": f"res.company/{record.id}",
                        "func": "write",
                        "line": 1,
                    })
        
        return super().write(vals)

    def get_contact_forward_settings(self):
        """
        Returns a dictionary with contact forwarding settings.
        
        Returns:
            dict: Dictionary with:
                - 'enabled': bool indicating if forwarding is active
                - 'forward_by_vat': bool indicating if id should be removed from payload
        """
        return {
            "enabled": self.contact_forward_enabled,
            "forward_by_vat": self.contact_forward_by_vat,
        }
