from odoo import models, fields, api, _

class RentalSalesProductTemplate(models.Model):
    _inherit = 'product.template'
    
    is_rent = fields.Boolean()
    count_rent = fields.Integer(compute='_compute_unit_rented')
    
    @api.depends('is_rent')
    def _compute_unit_rented(self):
      for rec in self:
        rec.count_rent = 0
        
    def action_rental_products(self):
      return {
          "name": _("Rental Product"),
          "type": "ir.actions.act_window",
          "view_mode": "tree,form",
          "res_model": "product.template",
          "target": "current",
          "domain": [("is_rent", "=", True)],
          "context": {"default_is_rent": self.id}
      }