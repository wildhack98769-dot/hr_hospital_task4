from odoo import api, fields, models
from odoo.exceptions import ValidationError


class HospitalDoctor(models.Model):
    """Hospital Doctor personnel records."""

    _name = 'hr.hospital.doctor'
    _description = 'Hospital Doctor'

    _inherit = 'hr.hospital.medic.info'

    name = fields.Char(string='Full Name', required=True)
    specialization = fields.Char(string='Specialization')
    photo = fields.Binary(string='Photo')

    category_id = fields.Many2one(
        comodel_name='hr.hospital.doctor.category',
        string='Category',
        ondelete='restrict',
    )

    user_id = fields.Many2one(
        comodel_name='res.users',
        string='System User',
    )

    is_intern = fields.Boolean(
        string='Is Intern',
        compute='_compute_is_intern',
        store=True,
    )

    mentor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string='Mentor Doctor',
        help='Only non-intern doctors can be mentors.',
        domain="[('is_intern', '=', False)]",
    )

    intern_ids = fields.One2many(
        comodel_name='hr.hospital.doctor',
        inverse_name='mentor_id',
        string='Interns',
    )

    @api.depends('category_id')
    def _compute_is_intern(self):
        """Визначаємо статус інтерна на основі зовнішнього ID категорії."""
        for rec in self:
            rec.is_intern = rec.category_id.is_intern_category if rec.category_id else False

    @api.constrains('mentor_id', 'is_intern')
    def _check_mentor_intern_status(self):
        """Перевірка обмежень для менторів та інтернів."""
        for rec in self:
            if rec.is_intern:
                if rec.mentor_id:
                    if rec.mentor_id.is_intern:
                        raise ValidationError(self.env._('A mentor cannot be an intern!'))
                    if rec.mentor_id == rec:
                        raise ValidationError(self.env._('A doctor cannot be their own mentor!'))
            else:
                if rec.mentor_id:
                    raise ValidationError(self.env._('Only interns can have a mentor.'))
