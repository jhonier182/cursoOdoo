from odoo import fields, models, api


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Tipo de Propiedad Inmobiliaria"
    _order = "sequence,name"

    name = fields.Char(string="Nombre", required=True)
    property_ids = fields.One2many("estate.property", "property_type_id", string="Propiedades")
    sequence = fields.Integer(string="Secuencia")
    offer_ids = fields.One2many(
        'estate.property.offer', 
        'property_type_id', 
        string="Ofertas"
    )
    offer_count = fields.Integer(
        string="Número de Ofertas", 
        compute="_compute_offer_count"
    )

    _sql_constraints = [
        ('unique_name', 'UNIQUE(name)', 'El nombre del tipo de propiedad debe ser único.')
    ]
    
    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
    