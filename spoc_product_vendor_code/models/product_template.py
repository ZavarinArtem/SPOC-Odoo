from odoo import fields, models


class ProductTemplate(models.Model):

    _inherit = "product.template"

    vendor_code = fields.Char("Vendor code")
