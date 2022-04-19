# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductTemplate(models.Model):

    _inherit = 'product.template'

    lot_info_usage = fields.Selection(
        [('no', 'No'),
         ('optional', 'Optional'),
         ('required', 'Required')],
        default='no',
        string='Lot information usage')
