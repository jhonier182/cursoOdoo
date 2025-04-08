from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name="estate.property.tag"
    _description ="Estate property tag"
    _order = "name"

    # Restricciones SQL para garantizar integridad de datos
    _sql_constraints = [
        ('unique_name', 'UNIQUE(name)', 'El nombre de la etiqueta debe ser único.')
    ]

    name= fields.Char(required=True)