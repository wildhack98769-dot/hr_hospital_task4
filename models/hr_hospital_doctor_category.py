
from odoo import fields, models


class HospitalDoctorCategory(models.Model):
    """Model for managing doctor qualification levels."""

    _name = "hr.hospital.doctor.category"
    _description = "Doctor Category"
    _order = "sequence, id"

    name = fields.Char(string="Category Name", required=True, translate=True)

    sequence = fields.Integer(
        string="Sequence",
        default=10,
        help="Used to order categories. Lower values come first.",
    )

    is_intern_category = fields.Boolean(string="Is Intern Category")

    doctor_ids = fields.One2many(
        comodel_name="hr.hospital.doctor",
        inverse_name="category_id",
        string="Doctors",
        help="List of doctors belonging to this category",
    )

    _unique_name = models.Constraint(
        "unique(name)",  # 'check(age > 18)' or/and 'check(activity = True)'
        "The category name must be unique!",
    )
