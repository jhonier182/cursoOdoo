from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    _order = "sequence,name"

    name = fields.Char(required=True)
    property_ids = fields.One2many("estate.property", "property_type_id")
    sequence = fields.Integer()

    _sql_constraints = [
        ('unique_name', 'UNIQUE(name)', 'El nombre del tipo de propiedad debe ser único.')
    ]
    