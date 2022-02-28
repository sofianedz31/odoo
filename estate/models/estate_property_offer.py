from odoo import fields, models, api,exceptions
from datetime import timedelta
from datetime import date
from odoo.tools.float_utils import float_compare, float_is_zero


class Offer(models.Model):
    _name = "estate.property.offer"
    _order = "price desc"

    property_type_id = fields.Many2one(related="property_id.property_type_id")
    price = fields.Float(required=True)
    status = fields.Selection([
        ('accepted', 'Accepted'), ('refused', 'Refused')
    ], copy=False)
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        compute="_compute_date_deadline", inverse="_compute_inverse_date_deadline", store=True)

    @api.depends('validity')
    def _compute_date_deadline(self):
        for offer in self:
            if offer.create_date:

                offer.date_deadline = offer.create_date + \
                    timedelta(days=offer.validity)
            else:
                offer.date_deadline = date.today() + timedelta(days=offer.validity)

    def _compute_inverse_date_deadline(self):
        for offer in self:
            if offer.create_date:

                offer.validity = (offer.date_deadline -
                                  offer.create_date.date()).days
            else:
                offer.validity = (offer.date_deadline - date.today()).days

    def action_accepted(self):
        for offer in self:
            offer.property_id.buyer_id = offer.partner_id
            offer.status = "accepted"
            offer.property_id.selling_price = offer.price
            offer.property_id.state = "offer_accepted"

        return True

    def action_refused(self):
        for offer in self:

            offer.status = "refused"

        return True

    _sql_constraints = [
        ('check_offer_price', 'CHECK(price  >= 0)',
         'The offre price  should be positive.')
    ]

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            property_id = self.env['estate.property'].browse(vals.get('property_id'))

        if float_compare(vals.get('price'), property_id.best_price, precision_digits=1) < 0:
            raise exceptions.UserError("ower amount than an existing offer.!")
        else:
            property_id.state = 'offer_received'

        return super().create(vals_list)
