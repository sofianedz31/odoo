from odoo import fields, models

class Type(models.Model):
    _name = "estate.property.type"

    _sql_constraints = [
        ('check__type_name', 'UNIQUE(name)',
         'The name  should be unique.')
    ] 


    name = fields.Char(required=True)

    
    sequence = fields.Integer('Sequence', default=1)




    property_ids = fields.One2many('estate.property', 'property_type_id')
    offer_ids = fields.One2many('estate.property.offer','property_type_id')
    offer_count =fields.Integer(compute="_compute_offer_count")
   
   
    def _compute_offer_count(self):
        for type in self:
            type.offer_count = len(type.offer_ids)



      




