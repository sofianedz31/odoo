from odoo import fields, models

class Tag(models.Model):

    _name = "estate.property.tag"

    _order = "name desc"

    name = fields.Char(required = True)
    color = fields.Integer()





_sql_constraints = [
        ('check_tag_name', 'UNIQUE(name)',
         'The  name  should be unique.')
    ] 