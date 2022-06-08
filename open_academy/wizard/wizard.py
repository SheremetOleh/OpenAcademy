from odoo import models, fields


class Wizard(models.TransientModel):
    _name = 'openacademy.wizard'
    _description = "Wizard: Quick registration of participants to sessions"

    def _default_session(self):
        return self.env['openacademy.session'].browse(self._context.get('active_id'))

    # session_id = fields.Many2one('openacademy.session', string="Session", required=True, default=_default_session)
    sessions = fields.Many2many('openacademy.session', string="Sessions", required=True, default=_default_session)
    participants = fields.Many2many('res.partner', string="Participants")

    def reg_participants(self):
        # self.session_id.participant |= self.participants
        for session in self.sessions:
            session.participant |= self.participants
        return {}
