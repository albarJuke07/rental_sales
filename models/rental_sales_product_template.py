from odoo import models, fields, api, _

class RentalSalesProductTemplate(models.Model):
    _inherit = 'product.template'
    
    is_rent = fields.Boolean()
    count_rent = fields.Integer(compute='_compute_unit_rented')
    
    @api.depends('is_rent')
    def _compute_unit_rented(self):
      for rec in self:
        counter_is_rent = self.env['sale.order'].search_count([('order_line.product_template_id.is_rent', '=', True), ("order_line.product_template_id.id", "=", self.id)]) if self.id else 0
        rec.count_rent = counter_is_rent
        
    def action_rental_products(self):

      return {
          "name": _("Rental Sale Order"),
          "type": "ir.actions.act_window",
          "view_mode": "tree,form",
          "res_model": "sale.order",
          "target": "current",
          # 'views': [(False, 'tree'), (self.env.ref('rental_sales.sale_order_form_view_inherit_rentalsales').id, 'form')],
          "domain": [("order_line.product_template_id.is_rent", "=", True), ("order_line.product_template_id.id", "=", self.id), ("rental_status", "=", "reserved")],
          'context': {'in_order_rent': True, 'selected_product_id': self.id},
      }