from odoo import models, fields


class ResPartnerBank(models.Model):

    _inherit = 'res.partner.bank'

    bank_SWIFT_Code = fields.Char(string='SWIFT Code')

    corr_bank_id = fields.Many2one(comodel_name='res.bank', string='Correspondent bank')
    corr_account = fields.Char(string='Account in the correspondent bank')
    corr_SWIFT_code = fields.Char(string='SWIFT-code of the correspondent bank')
