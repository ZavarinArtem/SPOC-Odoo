
from odoo import fields, models


class ProjectProjectStage(models.Model):

    _inherit = 'project.project.stage'

    project_ids = fields.One2many('project.project', 'stage_id', 'Projects')
    