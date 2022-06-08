from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import timedelta


class Session(models.Model):
    _name = 'openacademy.session'
    _description = 'Open academy Session'

    def _default_active(self):
        return True

    name = fields.Char(required=True)
    start_date = fields.Date(default=fields.Date.today())
    duration = fields.Float(digits=(6, 2), help="Duration in days")
    seats = fields.Integer()
    instructor_id = fields.Many2one('res.partner', ondelete='set null', string="Instructor",
                                    domain=['|', ('instructor', '=', True), ('category_id.name', 'like', "Teacher")])
    course_id = fields.Many2one('openacademy.course', ondelete='cascade', string="Course", required=True)
    participant = fields.Many2many('res.partner', string="Participant")
    taken_seats = fields.Float(string="Taken seats", compute='_taken_seats')
    active = fields.Boolean(string="Active", default=_default_active)

    end_date = fields.Date(string="End Date", store=True, compute='_get_end_date', inverse='_set_end_date')
    hours = fields.Float(string="Duration in hours", compute='_get_hours', inverse='_set_hours')
    participants_count = fields.Integer(string="Participants count", store=True, compute='_get_participants_count')
    color = fields.Integer()

    @api.depends('seats', 'participant')
    def _taken_seats(self):
        for rec in self:
            if not rec.seats:
                rec.taken_seats = 0.0
            else:
                rec.taken_seats = 100.0 * len(rec.participant) / rec.seats

    @api.onchange('seats', 'participant')
    def _verify_valid_seats(self):
        if self.seats < 0:
            return {
                'warning': {
                    'title': _("Incorrect 'seats' value"),
                    'message': _("The number of available seats may not be negative"),
                },
            }
        if self.seats < len(self.participant):
            return {
                'warning': {
                    'title': _("Too many attendees"),
                    'message': _("Increase seats or remove excess participants"),
                },
            }

    @api.constrains('instructor_id', 'participant')
    def _check_instructor(self):
        for rec in self:
            if rec.instructor_id and rec.instructor_id in rec.participant:
                raise ValidationError(_("A session's instructor can't be a participant"))

    @api.depends('start_date', 'duration')
    def _get_end_date(self):
        for rec in self:
            if not (rec.start_date and rec.duration):
                rec.end_date = rec.start_date
                continue

            start = fields.Datetime.from_string(rec.start_date)
            duration = timedelta(days=rec.duration, seconds=-1)
            rec.end_date = start + duration

    def _set_end_date(self):
        for rec in self:
            if not (rec.start_date and rec.end_date):
                continue

            start_date = fields.Datetime.from_string(rec.start_date)
            end_date = fields.Datetime.from_string(rec.end_date)
            rec.duration = (end_date - start_date).days + 1

    @api.depends('duration')
    def _get_hours(self):
        for rec in self:
            rec.hours = rec.duration * 24

    def _set_hours(self):
        for rec in self:
            rec.duration = rec.hours / 24

    @api.depends('participant')
    def _get_participants_count(self):
        for rec in self:
            rec.participants_count = len(rec.participant)



