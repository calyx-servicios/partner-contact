from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    contact_forward_enabled = fields.Boolean(
        string="Contact forwarding enabled",
        default=False,
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
            dict: Dictionary with 'enabled' key indicating if forwarding is active
        """
        return {
            "enabled": self.contact_forward_enabled,
        }
