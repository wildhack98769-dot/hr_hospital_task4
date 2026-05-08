from odoo import _, fields, models


class HrHospitalDashboard(models.TransientModel):
    """Navigation dashboard for the hospital application."""

    _name = "hr.hospital.dashboard"
    _description = "Hospital Dashboard"
    _rec_name = "name"

    name = fields.Char(
        default=lambda self: _("Hospital"), readonly=True, copy=False, translate=True
    )
    patient_count = fields.Integer(compute="_compute_counts")
    doctor_count = fields.Integer(compute="_compute_counts")
    visit_count = fields.Integer(compute="_compute_counts")
    disease_count = fields.Integer(compute="_compute_counts")
    doctor_category_count = fields.Integer(compute="_compute_counts")
    doctor_history_count = fields.Integer(compute="_compute_counts")

    # region Compute methods

    def _compute_counts(self):
        counts = {
            "patient_count": self.env["hr.hospital.patient"].search_count([]),
            "doctor_count": self.env["hr.hospital.doctor"].search_count([]),
            "visit_count": self.env["hr.hospital.visit"].search_count([]),
            "disease_count": self.env["hr.hospital.disease"].search_count([]),
            "doctor_category_count": self.env[
                "hr.hospital.doctor.category"
            ].search_count([]),
            "doctor_history_count": self.env[
                "hr.hospital.doctor.history"
            ].search_count([]),
        }
        for dashboard in self:
            for field_name, count in counts.items():
                dashboard[field_name] = count

    # endregion

    # region Actions

    def _open_action(self, xmlid):
        """Helper to open a specific action by XML ID."""
        return self.env["ir.actions.actions"]._for_xml_id(xmlid)

    def action_open_patients(self):
        """Opens the list view for patients."""
        return self._open_action("hr_hospital.action_hr_hospital_patient")

    def action_open_doctors(self):
        """Opens the list view for doctors."""
        return self._open_action("hr_hospital.action_hr_hospital_doctor")

    def action_open_visits(self):
        """Opens the list view for visits."""
        return self._open_action("hr_hospital.action_hr_hospital_visit")

    def action_open_diseases(self):
        """Opens the list view for diseases."""
        return self._open_action("hr_hospital.action_hr_hospital_disease")

    def action_open_doctor_categories(self):
        """Opens the list view for doctor categories."""
        return self._open_action("hr_hospital.action_hr_hospital_doctor_category")

    def action_open_doctor_history(self):
        """Opens the list view for doctor history."""
        return self._open_action("hr_hospital.action_hr_hospital_doctor_history")

    # endregion
