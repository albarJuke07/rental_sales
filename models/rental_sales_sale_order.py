from odoo import models, fields, api, _

class RentalSalesProductTemplate(models.Model):
    _inherit = 'sale.order'
    
    is_rental_order = fields.Boolean(default=True)
    rental_start_date = fields.Date(copy=False, default=fields.Date.today)
    rental_return_date = fields.Date(copy=False, default=fields.Date.today)
    duration_days = fields.Integer(compute='_count_rent_duration')
    rental_status = fields.Selection([
      ('draft', 'Draft'),
      ('reserved', 'Reserve'),
      ('returned', 'Return'),
      ('cancelled', 'Cancel'),
    ])
    
    
    @api.depends('rental_start_date', 'rental_return_date')
    def _count_rent_duration(self):
      for rec in self:
        rec.duration_days = (rec.rental_return_date - rec.rental_start_date).days if rec.rental_return_date > rec.rental_start_date else 0