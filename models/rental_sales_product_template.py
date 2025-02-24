from odoo import models, fields, api

class RentalSalesProductTemplate(models.Model):
    _inherit = 'product.template'
    
    is_rent = fields.Boolean()
    count_rent = fields.Integer(compute='_compute_unit_rented')
    
    @api.depends('is_rent')
    def _compute_unit_rented(self):
      for rec in self:
        rec.count_rent = 0