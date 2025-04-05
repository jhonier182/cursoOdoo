from odoo import models, fields
from dateutil.relativedelta import relativedelta

class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate Property'
    
    name = fields.Char(string="Nombre", required=True)
    description = fields.Text(string="Descripción")
    active = fields.Boolean(string="Activo", default=True)  
    state = fields.Selection([
        ("new", "New"),
        ("offer_received", "Offer Received"),
        ("offer_accepted", "Offer Accepted"),
        ("sold", "Sold"),
        ("canceled", "Canceled")
    ], string="Estado", copy=False, requiered=True, default='new') 
    postcode = fields.Char(string="Código Postal")
    date_availability = fields.Date(string="Fecha de Disponibilidad", copy=False, default=lambda self: fields.Date.today() + relativedelta(months=3))
    selling_price = fields.Float(string="Precio de Venta", readonly=True, copy=False)  # readonly para activar o desactivar campos
    bedrooms = fields.Integer(string="Habitaciones", default=2)
    living_area = fields.Integer(string="Área Habitable")
    facades = fields.Integer(string="Fachadas")
    garage = fields.Boolean(string="Garaje") 
    garden = fields.Boolean(string="Jardín")  
    garden_area = fields.Integer(string="Área del Jardín")
    garden_orientation = fields.Selection([
        ('north', 'Norte'),
        ('south', 'Sur'),
        ('east', 'Este'),
        ('west', 'Oeste')
    ], string="Orientación del Jardín")
