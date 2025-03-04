from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import datetime


class RentalSalesProductTemplate(models.Model):
    _inherit = 'sale.order'

    is_rental_order = fields.Boolean()
    # rental_start_date = fields.Date(copy=False, default=fields.Date.today)
    # rental_return_date = fields.Date(copy=False, default=lambda self: datetime.datetime.now() + datetime.timedelta(days=1))
    rental_start_date = fields.Date(copy=False)
    rental_return_date = fields.Date(copy=False)
    duration_days = fields.Integer(compute='_count_rent_duration')
    rental_status = fields.Selection([
      ('draft', 'Draft'),
      ('reserved', 'Reserve'),
      ('returned', 'Return'),
      ('cancelled', 'Cancel'),
    ], default='draft', readonly=True)
    rental_active = fields.Boolean(store=False)

    @api.depends('rental_start_date', 'rental_return_date')
    def _count_rent_duration(self):
      for rec in self:
        rec.duration_days = (rec.rental_return_date - rec.rental_start_date).days if rec.rental_return_date and rec.rental_start_date and (
            rec.rental_return_date > rec.rental_start_date) else 0
    
    # @api.model_create_multi
    # def create(self, vals_list):
    #     for vals in vals_list:
    #       if self.env.context.get('in_order_rent'):
    #         if vals.get('is_rental_order', True):
    #           vals['is_rental_order'] = True
    #     return super().create(vals_list)

    def action_confirm(self):
      result = super().action_confirm()
      today = fields.Date.today()
      if self.env.context.get('in_order_rent'):
        if self.order_line:
          for record in self:
              if record.rental_start_date and record.rental_return_date:
                  if record.rental_start_date > record.rental_return_date:
                    raise ValidationError(
                        _("Start Date and Return Date are not valid"))
                  else:
                    if record.rental_start_date <= today <= record.rental_return_date:
                        record.rental_status = "reserved"
              else:
                  raise ValidationError(
                      _("Start Date and Return Date can not be empty"))
        else:
          raise ValidationError(_("Product is empty"))
      return result

    def rentalsales__reserved_order_action(self):
        for record in self:
          record.rental_status = 'reserved'

    def rentalsales__returned_order_action(self):
        for record in self:
          record.rental_status = 'returned'