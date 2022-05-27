
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import timedelta


class Course(models.Model):
    _name = 'openacademy.course'
    _description = 'Open academy Course'

    name = fields.Char(required=True)
    description = fields.Text()
    responsible_id = fields.Many2one('res.users', ondelete='set null', string="Responsible")
    sessions = fields.One2many('openacademy.session', 'course_id', string="Sessions")

    _sql_constraints = [
        ('name_description_check',
         'CHECK(name != description)',
         "The title of the course should not be the description"),

        ('name_unique',
         'UNIQUE(name)',
         "The course title must be unique"),
    ]


class Session(models.Model):
    _name = 'openacademy.session'
    _description = 'Open academy Session'

    name = fields.Char(required=True)
    start_date = fields.Date(default=fields.Date.today())
    duration = fields.Float(digits=(6, 2), help="Duration in days")
    seats = fields.Integer()
    instructor_id = fields.Many2one('res.partner', ondelete='set null', string="Instructor",
                                    domain=['|', ('instructor', '=', True), ('category_id.name', 'like', "Teacher")])
    course_id = fields.Many2one('openacademy.course', ondelete='cascade', string="Course", required=True)
    participant = fields.Many2many('res.partner', string="Participant")
    taken_seats = fields.Float(string="Taken seats", compute='_taken_seats')
    active = fields.Boolean(string="Active", default='_default_active')

    end_date = fields.Date(string="End Date", store=True,
                           compute='_get_end_date', inverse='_set_end_date')

    @api.depends('seats', 'participant')
    def _taken_seats(self):
        for rec in self:
            if not rec.seats:
                rec.taken_seats = 0.0
            else:
                rec.taken_seats = 100.0 * len(rec.participant) / rec.seats

    def _default_active(self):
        return True

    @api.onchange('seats', 'participant')
    def _verify_valid_seats(self):
        if self.seats < 0:
            return {
                'warning': {
                    'title': "Incorrect 'seats' value",
                    'message': "The number of available seats may not be negative",
                },
            }
        if self.seats < len(self.participant):
            return {
                'warning': {
                    'title': "Too many attendees",
                    'message': "Increase seats or remove excess participants",
                },
            }

    @api.constrains('instructor_id', 'participant')
    def _check_instructor(self):
        for rec in self:
            if rec.instructor_id and rec.instructor_id in rec.participant:
                raise ValidationError("A session's instructor can't be a participant")

    @api.depends('start_date', 'duration')
    def _get_end_date(self):
        for r in self:
            if not (r.start_date and r.duration):
                r.end_date = r.start_date
                continue

            start = fields.Datetime.from_string(r.start_date)
            duration = timedelta(days=r.duration, seconds=-1)
            r.end_date = start + duration

    def _set_end_date(self):
        for r in self:
            if not (r.start_date and r.end_date):
                continue

            start_date = fields.Datetime.from_string(r.start_date)
            end_date = fields.Datetime.from_string(r.end_date)
            r.duration = (end_date - start_date).days + 1




















