from odoo import fields, models


class Partner(models.Model):
    _inherit = "res.partner"

    full_name = fields.Char(string="Full Name", translate=True)

    street = fields.Char(translate=True)
    street2 = fields.Char(translate=True)
    city = fields.Char(translate=True)

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


class CountryState(models.Model):

    _inherit = "res.country.state"

    name = fields.Char(translate=True)


class Currency(models.Model):

    _inherit = "res.currency"
    name = fields.Char(translate=True)


class Bank(models.Model):

    _inherit = "res.bank"
    name = fields.Char(translate=True)
