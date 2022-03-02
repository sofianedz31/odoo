from odoo import fields, models, api, exceptions
from odoo.tools.float_utils import float_compare, float_is_zero


class Property(models.Model):
    _name = "estate.property"
    _description = "odoo"

    _order = "id desc"


    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(string='Available From',
                                    copy=False, default=lambda self: fields.Date.add(fields.Date.today(), months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()

    garage = fields.Boolean()

    garden = fields.Boolean('garden')
    garden_area = fields.Integer('garden_area')
    garden_orientatin = fields.Selection([
        ('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')
    ], string='garden_orientatin', default=False)
    active = fields.Boolean(default=True)
    state = fields.Selection([('new', 'New',), ('offer_received', 'Offer Received'),
                              ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'), ('canceled', 'Canceled')],
                             required=True, copy=False, default='new')
    property_type_id = fields.Many2one('estate.property.type')
    

    buyer_id = fields.Many2one('res.partner', copy=False)
    salesman_id = fields.Many2one(
        'res.users', default=lambda self: self.env.user)
    tag_ids = fields.Many2many('estate.property.tag')
    offer_ids = fields.One2many('estate.property.offer', 'property_id')
    total_area = fields.Float(compute="_compute_total_area")
    best_price = fields.Float(compute="_compute_best_price")
    company_id = fields.Many2one('res.company',default=lambda self: self.env.user.company_id,required=True)

    @api.depends('garden_area', 'living_area')
    def _compute_total_area(self):

        for property in self:
            area = 0
            if property.garden_area:
                area += property.garden_area
            if property.living_area:
                area += property.living_area
            property.total_area = area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):

        for property in self:
            if property.offer_ids:
                property.best_price = max(property.offer_ids.mapped("price"))
            else:
                property.best_price = 0

    @api.onchange("garden")
    def _onchange_garden(self):
        self.garden_area = 10
        self.garden_orientatin = "north"

    def action_sold(self):
        for property in self:
            if property.state!="offer_accepted":
                raise exceptions.UserError("no accepted offers on it")

            elif property.state == "canceled":
                raise exceptions.UserError(
                    ' a sold property cannot be canceled.')
            property.state = "sold"
        return True

    def action_canceled(self):
        for property in self:
            if property.state == "sold":
                raise exceptions.UserError(
                    ' A canceled property cannot be set as sold.')
            property.state = "canceled"
        return True

    _sql_constraints = [
        ('check_propery_expected_price', 'CHECK(expected_price  > 0)',
         'The price  should be positive.'),
        ('check_proprety_selling_price', 'CHECK(selling_price  >= 0)',
         'The selling_price  should be positive.'),

    ]

    @api.constrains('selling_price', 'expected_price')
    def _check_price(self):
        for property in self:
            if not float_is_zero(property.selling_price, precision_digits=1) and float_compare(property.selling_price, property.expected_price*0.9, precision_rounding=1) < 0:
                raise exceptions.ValidationError(
                    "the selling price cannot be lower than 90 precent of the expected price.")


    @api.onchange("offer_ids")
    def _onchange_offer_ids(self):
        if self.offer_ids : 
            self.state = "offer_received"


    @api.ondelete(at_uninstall=False)
    def _unlink_new_or_canceled(self):
        for property in self : 
            if property.state not in ('new','canceled'):
                raise exceptions.UserError("Can't delete a property if its state is not ‘New’ or ‘Canceled’!")
        

    