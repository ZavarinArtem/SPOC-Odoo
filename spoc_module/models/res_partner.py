from odoo import fields, models


class Partner(models.Model):
    _inherit = "res.partner"

    parent_group_id = fields.Many2one(comodel_name="res.partner", string="Group")
    child_group_ids = fields.One2many(
        "res.partner",
        "parent_group_id",
        string="Elements",
        domain=[("active", "=", True)],
    )
    _parent_name = "parent_group_id"
    _parent_store = True

    parent_path = fields.Char(index=True)
    is_group = fields.Boolean("It's a group")
