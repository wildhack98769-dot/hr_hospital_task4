from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class HospitalVisit(models.Model):
    """Model for managing visits."""

    _name = 'hr.hospital.visit'
    _description = 'Patient Visit'
    _rec_name = 'name'

    name = fields.Char(string='Visit', compute='_compute_name', store=True)

    state = fields.Selection(
        [
            ('planned', 'Planned'),
            ('done', 'Done'),
            ('cancelled', 'Cancelled'),
        ],
        string='Status',
        default='planned',
        required=True,
    )

    planned_date = fields.Datetime(
        string='Planned Date/Time',
        required=True,
        help="Scheduled time for the doctor's appointment",
    )
    actual_date = fields.Datetime(string='Actual Date/Time', help='The time when the visit actually took place')

    doctor_id = fields.Many2one('hr.hospital.doctor', string='Doctor', required=True)
    patient_id = fields.Many2one('hr.hospital.patient', string='Patient', required=True)

    summary = fields.Html(string='Epicrisis / Conclusion')
    disease_id = fields.Many2one('hr.hospital.disease', string='Disease')

    active = fields.Boolean(string='Active', default=True)
    same_disease_visit_count = fields.Integer(
        string='Visits with This Disease',
        compute='_compute_same_disease_visit_count',
    )

    @api.depends('patient_id', 'doctor_id', 'planned_date')
    def _compute_name(self):
        for rec in self:
            parts = []
            if rec.patient_id:
                parts.append(rec.patient_id.display_name)
            if rec.doctor_id:
                parts.append(rec.doctor_id.display_name)
            if rec.planned_date:
                parts.append(fields.Datetime.to_string(rec.planned_date))
            rec.name = ' - '.join(parts) if parts else _('New Visit')

    @api.depends('disease_id')
    def _compute_same_disease_visit_count(self):
        for rec in self:
            if rec.disease_id:
                rec.same_disease_visit_count = self.search_count([('disease_id', '=', rec.disease_id.id)])
            else:
                rec.same_disease_visit_count = 0

    def write(self, vals):
        """Override write method to prevent changes to completed visits."""
        for rec in self:
            if rec.state == 'done':
                readonly_fields = [
                    'planned_date',
                    'actual_date',
                    'doctor_id',
                    'patient_id',
                ]
                if any(f in vals for f in readonly_fields):
                    raise ValidationError(
                        _('You cannot change the date, time, or doctor for a visit that has already taken place.')
                    )
        return super().write(vals)

    def unlink(self):
        """Override unlink method to prevent deleting completed visits."""
        for rec in self:
            if rec.state == 'done':
                raise ValidationError(_('You cannot delete a completed visit.'))
        return super().unlink()

    def toggle_active(self):
        """Validate archive attempts from the interface."""
        for rec in self:
            if rec.active and rec.state == 'done':
                raise ValidationError(_('You cannot archive a completed visit.'))
        return super().toggle_active()

    def action_done(self):
        """Set the visit state to 'done' and record the actual date if not set."""
        for rec in self:
            rec.state = 'done'
            if not rec.actual_date:
                rec.actual_date = fields.Datetime.now()

    def action_open_same_disease_visits(self):
        """Opens a list of visits with the same disease."""
        self.ensure_one()
        if not self.disease_id:
            return False
        action = self.env.ref('hr_hospital.action_hr_hospital_visit').read()[0]
        action['domain'] = [('disease_id', '=', self.disease_id.id)]
        action['context'] = dict(self.env.context, default_disease_id=self.disease_id.id)
        return action

    def action_cancel(self):
        """Cancels the visit."""
        for rec in self:
            if rec.state == 'done':
                raise ValidationError(_('You cannot cancel a completed visit.'))
            rec.state = 'cancelled'

    def action_planned(self):
        """Sets the visit state back to 'planned'."""
        for rec in self:
            if rec.state == 'done':
                raise ValidationError(_('You cannot set a completed visit to planned.'))
            rec.state = 'planned'

    def action_create_new_visit_from_patient(self):
        """Creates a new visit for the current patient."""
        self.ensure_one()
        action = self.env.ref('hr_hospital.action_hr_hospital_visit').read()[0]
        action['views'] = [(self.env.ref('hr_hospital.view_hr_hospital_visit_form').id, 'form')]
        action['context'] = dict(
            self.env.context,
            default_patient_id=self.patient_id.id,
            default_doctor_id=self.doctor_id.id,
        )
        return action
