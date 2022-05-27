from odoo import fields, models


class Partner(models.Model):
    _inherit = 'res.partner'

    instructor = fields.Boolean("Instructor", default=False)
    sessions = fields.Many2many('openacademy.session', string="Attended Sessions", readonly=True)
