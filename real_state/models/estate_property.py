from odoo import models, fields
from dateutil.relativedelta import relativedelta

class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate Property'
    
    name = fields.Char(required=True)
    description = fields.Text()
    active = fields.Boolean(default=True)  
    state = fields.Selection([
        ("new", "New"),
        ("offer_received", "Offer Received"),
        ("offer_accepted", "Offer Accepted"),
        ("sold", "Sold"),
        ("canceled", "Canceled")
    ], default='new')
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=lambda self: fields.Date.today() + relativedelta(months=3))
    selling_price = fields.Float(readonly=True, copy=False)  # readonly para activar o desactivar campos
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean() 
    garden = fields.Boolean()  
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([
        ('north', 'Norte'),
        ('south', 'Sur'),
        ('east', 'Este'),
        ('west', 'Oeste')
    ])
