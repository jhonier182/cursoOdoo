from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"

    # Restricciones SQL para garantizar integridad de datos
    _sql_constraints = [
        ('unique_name', 'UNIQUE(name)', 'El nombre del tipo de propiedad debe ser único.')
    ]

    name = fields.Char(required=True)
    