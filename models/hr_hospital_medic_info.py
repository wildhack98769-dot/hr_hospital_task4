from datetime import date

from odoo import api, fields, models


class HospitalMedicInfo(models.AbstractModel):
    _name = 'hr.hospital.medic.info'
    _description = 'Medical Information Abstract'

    blood_group = fields.Selection(
        [
            ('0', 'O(I)'),
            ('A', 'A(II)'),
            ('B', 'B(III)'),
            ('AB', 'AB(IV)'),
        ],
        string='Blood Group',
    )

    rh_factor = fields.Selection(
        [
            ('plus', '+'),
            ('minus', '-'),
        ],
        string='Rh Factor',
    )

    phone = fields.Char(string='Phone')
    email = fields.Char(string='Email')
    photo = fields.Image(string='Photo')
    avatar_128 = fields.Image(related='photo', max_width=128, max_height=128)
    gender = fields.Selection(
        [('male', 'Male'), ('female', 'Female'), ('other', 'Other')],
        string='Gender',
        default='male',
    )

    date_of_birth = fields.Date(string='Date of Birth')
    age = fields.Integer(string='Age', compute='_compute_age', store=False)

    @api.depends('date_of_birth')
    def _compute_age(self):
        today = date.today()
        for rec in self:
            if rec.date_of_birth:
                rec.age = (
                    today.year
                    - rec.date_of_birth.year
                    - ((today.month, today.day) < (rec.date_of_birth.month, rec.date_of_birth.day))
                )
            else:
                rec.age = 0
