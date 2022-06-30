from odoo import models, fields
from datetime import timedelta


class Lead(models.Model):

    _inherit = "crm.lead"

    next_leads = fields.One2many(
        comodel_name="res.partner", string="Next leads", compute="_compute_next_leads"
    )

    def _compute_next_leads(self):

        lead_model = self.env["crm.lead"]
        partner_model = self.env["res.partner"]
        users_model = self.env["res.users"]

        partners_with_leads = lead_model.search([]).mapped("partner_id.id")
        partners_with_leads_older_28_d = lead_model.search(
            [("create_date", "<", fields.Date.today() - timedelta(days=28))]
        ).mapped("partner_id.id")
        partners_internal_users = users_model.search(
            [
                (
                    "groups_id",
                    "in",
                    [
                        self.env.ref("base.group_user").id,
                    ],
                )
            ]
        ).mapped("partner_id.id")
        new_lead_partners = partner_model.search(
            [
                "&",
                ("id", "not in", partners_internal_users),
                "|",
                ("id", "not in", partners_with_leads),
                ("id", "in", partners_with_leads_older_28_d),
            ]
        )
        for rec in self:

            rec.next_leads = new_lead_partners


class Partner(models.Model):

    _inherit = 'res.partner'

    never_had_leads = fields.Boolean(compute='_compute_never_had_leads')
    has_lead_older_28 = fields.Boolean(compute='_compute_has_lead_older_28')

    def _compute_never_had_leads(self):
        lead_model = self.env["crm.lead"]
        partners_with_leads = lead_model.search([]).mapped("partner_id.id")
        for rec in self:
            rec.never_had_leads = rec.id not in partners_with_leads

    def _compute_has_lead_older_28(self):
        lead_model = self.env["crm.lead"]
        partners_with_leads_older_28_d = lead_model.search(
            [("create_date", "<", fields.Date.today() - timedelta(days=28))]
        ).mapped("partner_id.id")
        for rec in self:
            rec.has_lead_older_28 = rec.id in partners_with_leads_older_28_d
