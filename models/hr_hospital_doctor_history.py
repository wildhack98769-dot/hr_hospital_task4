from odoo import _, api, fields, models


class HospitalDoctorHistory(models.Model):
    """Модель Історія персональних лікарів."""

    _name = "hr.hospital.doctor.history"
    _description = "Doctor Appointment History"

    _order = "appointment_date desc"

    patient_id = fields.Many2one(
        comodel_name="hr.hospital.patient",
        string="Patient",
        required=True,
        ondelete="cascade",
    )
    doctor_id = fields.Many2one(
        comodel_name="hr.hospital.doctor",
        string="Doctor",
        required=True,
        ondelete="restrict",
    )
    appointment_date = fields.Date(
        string="Appointment Date", required=True, default=fields.Date.context_today
    )
    change_date = fields.Date(string="Change Date")
    active = fields.Boolean(string="Active", default=True)

    @api.onchange("appointment_date", "change_date")
    def _onchange_dates(self):
        if self.appointment_date and self.change_date:
            if self.change_date < self.appointment_date:
                return {
                    "warning": {
                        "title": _("Date Error"),
                        "message": _(
                            "Дата зміни лікаря не може бути раніше ніж дата призначення"
                        ),
                    }
                }
        return None

    @api.depends("patient_id", "doctor_id", "appointment_date")
    def _compute_display_name(self):
        for rec in self:
            patient_name = rec.patient_id.display_name or _("Unknown Patient")
            doctor_name = rec.doctor_id.display_name or _("Unknown Doctor")
            category = (
                rec.doctor_id.category_id.name
                if rec.doctor_id.category_id
                else _("No Category")
            )
            date_str = (
                rec.appointment_date.strftime("%Y-%m-%d")
                if rec.appointment_date
                else ""
            )

            rec.display_name = f"{patient_name} - {doctor_name} ({category}) {date_str}"
