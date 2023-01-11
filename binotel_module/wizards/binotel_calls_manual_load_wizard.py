# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class BinotelCallsManualLoadWizard(models.TransientModel):

    _name = "binotel.calls.manual.load.wizard"
    _description = "Calls Manual Load Wizard"

    start_date = fields.Date("Start Date")
    end_date = fields.Date("End Date")

    def load_calls(self):
        self.env["binotel.calls"].sudo()._load_calls(self.start_date, self.end_date)
        return None
