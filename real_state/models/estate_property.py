from odoo import models, fields, api  # Importación de los módulos básicos de Odoo para definir modelos y campos
from dateutil.relativedelta import relativedelta  # Importación para manejar operaciones con fechas

class EstateProperty(models.Model):
    _name = 'estate.property'  # Identificador técnico del modelo en la base de datos
    _description = 'Estate Property'  # Descripción legible del modelo
    
    # Campo para el nombre de la propiedad, obligatorio
    name = fields.Char(string="Nombre", required=True)  # Nombre de la propiedad, requerido para su identificación
    # Campo para una descripción detallada de la propiedad
    description = fields.Text(string="Descripción")  # Descripción que proporciona información adicional sobre la propiedad
    # Campo booleano para indicar si el registro está activo, por defecto es True
    active = fields.Boolean(string="Estado Activo", default=True, help="Indica si la propiedad está activa o archivada")  # Indica si la propiedad está activa o no
    # Campo de selección para el estado de la propiedad con diferentes opciones
    state = fields.Selection([
        ("new", "New"),  # Nuevo
        ("offer_received", "Offer Received"),  # Oferta recibida
        ("offer_accepted", "Offer Accepted"),  # Oferta aceptada
        ("sold", "Sold"),  # Vendido
        ("canceled", "Canceled")  # Cancelado
    ], string="Estado", copy=False, required=True, default='new')  # Estado de la propiedad, obligatorio y no se copia al duplicar
    # Campo para el código postal de la propiedad
    postcode = fields.Char(string="Código Postal")  # Código postal asociado a la propiedad
    # Campo para la fecha de disponibilidad, no se copia al duplicar y por defecto es 3 meses después de hoy
    date_availability = fields.Date(string="Fecha de Disponibilidad", copy=False, default=lambda self: fields.Date.today() + relativedelta(months=3))  # Fecha en que la propiedad estará disponible
    # Campo para el precio de venta, solo lectura y no se copia al duplicar
    selling_price = fields.Float(string="Precio de Venta", readonly=False, copy=False)  # Precio al que se vende la propiedad
    # Campo para el número de habitaciones, por defecto 2
    bedrooms = fields.Integer(string="Habitaciones", default=2)  # Número de habitaciones en la propiedad
    # Campo para el área habitable en metros cuadrados
    living_area = fields.Integer(string="Área Habitable")  # Área habitable de la propiedad en metros cuadrados
    # Campo para el número de fachadas del inmueble
    facades = fields.Integer(string="Fachadas")  # Número de fachadas que tiene la propiedad
    # Campo booleano para indicar si la propiedad tiene garaje
    garage = fields.Boolean(string="Garaje")  # Indica si la propiedad cuenta con garaje
    # Campo booleano para indicar si la propiedad tiene jardín
    garden = fields.Boolean(string="Jardín")  # Indica si la propiedad cuenta con jardín
    # Campo para el área del jardín en metros cuadrados
    garden_area = fields.Integer(string="Área del Jardín")  # Área del jardín en metros cuadrados
    # Campo de selección para la orientación del jardín
    garden_orientation = fields.Selection([
        ('north', 'Norte'),  # Orientación norte
        ('south', 'Sur'),    # Orientación sur
        ('east', 'Este'),    # Orientación este
        ('west', 'Oeste')    # Orientación oeste
    ], string="Orientación del Jardín")  # Orientación del jardín
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")  # Tipo de propiedad
    salesperson_id = fields.Many2one("res.users", string="Salesman", index=True, default=lambda self: self.env.user)  # Vendedor asignado a la propiedad
    buyer_id = fields.Many2one("res.partner", string="Buyer", index=True, copy=False)  # Comprador de la propiedad
    tags_ids = fields.Many2many("estate.property.tag", string="Property Tags")  # Etiquetas asociadas a la propiedad
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")  # Ofertas recibidas para la propiedad
    total_area = fields.Float(string="Área Total", compute="_compute_total_area")  # Área total calculada de la propiedad
    best_price = fields.Float(string="Mejor Oferta", compute="_compute_best_price")  # Mejor oferta recibida
    onchange_state = fields.Char(string="Onchange State")  # Estado de cambio para el campo

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area  # Cálculo del área total

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            prices = record.offer_ids.mapped("price")
            record.best_price = max(prices) if prices else 0.0  # Si no hay ofertas, devuelve 0

    # Este método se activa cuando cambia el estado del campo 'garden'. 
    # Si el jardín está habilitado, se establece el área del jardín en 10 y la orientación en "norte". 
    # Se muestra una advertencia al usuario indicando que estas configuraciones son predeterminadas.
    # Si el jardín no está habilitado, se restablecen el área y la orientación del jardín a None.
    @api.onchange("garden")
    def _onchange_garden_area(self):
        if self.garden:
            self.garden_area = 10  # Establece el área del jardín a 10 si está habilitado
            self.garden_orientation = "north"  # Establece la orientación del jardín a norte
            return {
                "warning": {
                    "title": "Atención",
                    "message": "Esta opción habilitará el área del jardín (por defecto 10) y la orientación del jardín (por defecto norte)"  # Mensaje de advertencia al usuario
                }
            }
        else:
            self.garden_area = None  # Restablece el área del jardín a None si no está habilitado
            self.garden_orientation = None  # Restablece la orientación del jardín a None
            
    def action_sold(self):
        """Método que cambia el estado de la propiedad a 'sold' (vendida)"""
        for record in self:
            if record.state == 'canceled':
                raise models.ValidationError("Las propiedades canceladas no pueden marcarse como vendidas.")
            record.state = 'sold'
        return True
        
    def action_cancel(self):
        """Método que cambia el estado de la propiedad a 'canceled' (cancelada)"""
        for record in self:
            if record.state == 'sold':
                raise models.ValidationError("Las propiedades vendidas no pueden cancelarse.")
            record.state = 'canceled'
        return True