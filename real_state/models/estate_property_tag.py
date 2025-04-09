from odoo import models, fields

class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Etiqueta de Propiedad Inmobiliaria'
    _order = "name"
    
    # SQL constraints para asegurar nombres únicos
    _sql_constraints = [
        ('check_name', 'UNIQUE(name)', 'El nombre de la etiqueta debe ser único.')
    ]
    
    name = fields.Char(string="Nombre", required=True)
    color = fields.Integer(string="Color")

   