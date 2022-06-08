
from odoo import models, fields, _


class Course(models.Model):
    _name = 'openacademy.course'
    _description = 'Open academy Course'

    name = fields.Char(required=True, translate=True)
    description = fields.Text()
    responsible_id = fields.Many2one('res.users', ondelete='set null', string="Responsible")
    sessions = fields.One2many('openacademy.session', 'course_id', string="Sessions")

    _sql_constraints = [
        ('name_description_check',
         'CHECK(name != description)',
         _("The title of the course should not be the description")),

        ('name_unique',
         'UNIQUE(name)',
         _("The course title must be unique")),
    ]






















