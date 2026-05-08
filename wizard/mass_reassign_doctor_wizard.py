from odoo import fields, models


class MassReassignDoctorWizard(models.TransientModel):
    """Wizard for mass reassigning doctors to patients."""

    _name = 'mass.reassign.doctor.wizard'
    _description = 'Mass Reassign Doctor Wizard'
    _rec_name = 'name'

    name = fields.Char(default='Перепризначити лікаря', readonly=True)
    doctor_id = fields.Many2one('hr.hospital.doctor', string='Новий Лікар', required=True)
    change_date = fields.Date(string='Дата зміни', default=fields.Date.context_today)

    def action_reassign_doctor(self):
        """Reassigns the selected doctor to the active patients."""
        patient_ids = self.env.context.get('active_ids')
        patients = self.env['hr.hospital.patient'].browse(patient_ids)
        patients.write({'personal_doctor_id': self.doctor_id.id})
