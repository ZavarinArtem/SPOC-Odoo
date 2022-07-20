from odoo import fields, models


class Partner(models.Model):
    _inherit = "res.partner"

    full_name = fields.Char(string="Full Name", translate=True)

    def write(self, vals):

        if self.is_company and (
            (
                (self.full_name == "" or self.full_name == False)
                and ("full_name" not in vals)
            )
            or (
                "full_name" in vals
                and (vals["full_name"] == "" or vals["full_name"] == False)
            )
        ):
            vals["full_name"] = self.name

        return super().write(vals)
