from odoo import models, fields, api


class StockMove(models.Model):
    _inherit = "stock.move"

    lot_info = fields.Char('Lot/Serial Number info')
    lot_info_usage = fields.Selection(
        [('no', 'No'),
         ('optional', 'Optional'),
         ('required', 'Required')],
        related='product_id.product_tmpl_id.lot_info_usage')

    # this is not working as wanted
    @api.onchange('lot_info')
    def _onchange_lot_info(self):
        for rec in self:
            for move_line in rec.move_line_ids:
                move_line.lot_info = rec.lot_info


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    lot_info = fields.Char('Lot/Serial Number info')
    lot_info_usage = fields.Selection(
        [('no', 'No'),
         ('optional', 'Optional'),
         ('required', 'Required')],
        related='product_id.product_tmpl_id.lot_info_usage')
