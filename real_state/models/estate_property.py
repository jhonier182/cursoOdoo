from odoo import models, fields, api  # Importación de los módulos básicos de Odoo para definir modelos y campos
from dateutil.relativedelta import relativedelta  # Importación para manejar operaciones con fechas

class EstateProperty(models.Model):
    _name = 'estate.property'  # Identificador técnico del modelo en la base de datos
    _description = 'Estate Property'  # Descripción legible del modelo
    
    # Campo para el nombre de la propiedad, obligatorio
    name = fields.Char(string="Nombre", required=True)
    # Campo para una descripción detallada de la propiedad
    description = fields.Text(string="Descripción")
    # Campo booleano para indicar si el registro está activo, por defecto es True
    active = fields.Boolean(string="Estado Activo", default=True, help="Indica si la propiedad está activa o archivada")
    # Campo de selección para el estado de la propiedad con diferentes opciones
    state = fields.Selection([
        ("new", "New"),  # Nuevo
        ("offer_received", "Offer Received"),  # Oferta recibida
        ("offer_accepted", "Offer Accepted"),  # Oferta aceptada
        ("sold", "Sold"),  # Vendido
        ("canceled", "Canceled")  # Cancelado
    ], string="Estado", copy=False, requiered=True, default='new')  # No se copia al duplicar, es obligatorio y por defecto es 'new'
    # Campo para el código postal de la propiedad
    postcode = fields.Char(string="Código Postal")
    # Campo para la fecha de disponibilidad, no se copia al duplicar y por defecto es 3 meses después de hoy
    date_availability = fields.Date(string="Fecha de Disponibilidad", copy=False, default=lambda self: fields.Date.today() + relativedelta(months=3))
    # Campo para el precio de venta, solo lectura y no se copia al duplicar
    selling_price = fields.Float(string="Precio de Venta", readonly=True, copy=False)
    # Campo para el número de habitaciones, por defecto 2
    bedrooms = fields.Integer(string="Habitaciones", default=2)
    # Campo para el área habitable en metros cuadrados
    living_area = fields.Integer(string="Área Habitable")
    # Campo para el número de fachadas del inmueble
    facades = fields.Integer(string="Fachadas")
    # Campo booleano para indicar si la propiedad tiene garaje
    garage = fields.Boolean(string="Garaje") 
    # Campo booleano para indicar si la propiedad tiene jardín
    garden = fields.Boolean(string="Jardín")  
    # Campo para el área del jardín en metros cuadrados
    garden_area = fields.Integer(string="Área del Jardín")
    # Campo de selección para la orientación del jardín
    garden_orientation = fields.Selection([
        ('north', 'Norte'),  # Orientación norte
        ('south', 'Sur'),    # Orientación sur
        ('east', 'Este'),    # Orientación este
        ('west', 'Oeste')    # Orientación oeste
    ], string="Orientación del Jardín")

