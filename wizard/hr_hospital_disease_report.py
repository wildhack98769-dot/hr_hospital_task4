from odoo import fields, models
from odoo.exceptions import UserError


class HospitalDiseaseReport(models.TransientModel):
    """Wizard for generating disease reports based on various criteria."""
    _name = 'hr.hospital.disease.report'
    _description = 'Hospital Disease Report Wizard'

    start_date = fields.Date(string='Start Date', required=True)
    end_date = fields.Date(string='End Date', required=True)
    doctor_ids = fields.Many2many('hr.hospital.doctor', string='Doctors')
    disease_ids = fields.Many2many('hr.hospital.disease', string='Diseases')

    def generate_report(self):
        """Generates a report of hospital visits based on the selected criteria."""
        self.ensure_one()

        domain = [
            ('planned_date', '>=', self.start_date),
            ('planned_date', '<=', self.end_date),
        ]
        if self.doctor_ids:
            domain.append(('doctor_id', 'in', self.doctor_ids.ids))
        if self.disease_ids:
            domain.append(('disease_id', 'in', self.disease_ids.ids))

        records = self.env['hr.hospital.visit'].search(domain)

        if not records:
            raise UserError("За обраними критеріями візитів не знайдено.")

        return self.env.ref('hr_hospital.action_report_disease_statistics').report_action(records)
