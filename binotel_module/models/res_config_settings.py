# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    api_host = fields.Char("ARI Host", config_parameter="binotel.api_host")
    api_key = fields.Char("ARI Key", config_parameter="binotel.api_key")
    secret = fields.Char("Secret", config_parameter="binotel.secret")

    min_call_duration = fields.Integer(
        "Min Call Duration", config_parameter="binotel.min_call_duration"
    )
