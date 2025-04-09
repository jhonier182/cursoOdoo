from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import timedelta
from odoo.tools import float_compare

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Oferta de Propiedad Inmobiliaria"
    _order = "price desc"
    
    # Restricciones SQL para garantizar integridad de datos
    _sql_constraints = [
        ('check_price', 'CHECK(price > 0)', 'El precio de la oferta debe ser estrictamente positivo.')
    ]
    
    # Campos básicos
    price = fields.Float(string="Precio", required=True)
    status = fields.Selection(
        [('accepted', 'Aceptada'), ('refused', 'Rechazada')],
        string="Estado",
        copy=False
    )
    
    # Relaciones
    partner_id = fields.Many2one('res.partner', string="Comprador", required=True)
    property_id = fields.Many2one('estate.property', string="Propiedad", required=True)
    
    # Campos para la validez de la oferta
    validity = fields.Integer(string="Validez (días)", default=7)
    date_deadline = fields.Date(string="Fecha Límite", compute="_compute_date_deadline", inverse="_inverse_date_deadline", store=True)
    
    # Campo relacionado para mostrar el estado de la propiedad
    property_type_id = fields.Many2one(
        'estate.property.type',
        related='property_id.property_type_id',
        string="Tipo de Propiedad",
        store=True
    )
    
    # Campo para mostrar el estado de la propiedad
    property_state = fields.Selection(
        related='property_id.state',
        string="Estado de la Propiedad"
    )
    
    @api.depends('validity', 'create_date')
    def _compute_date_deadline(self):
        for offer in self:
            if offer.create_date:
                create_date = offer.create_date.date()
            else:
                create_date = fields.Date.today()
            offer.date_deadline = create_date + timedelta(days=offer.validity)
    
    def _inverse_date_deadline(self):
        for offer in self:
            if offer.create_date and offer.date_deadline:
                create_date = offer.create_date.date()
                delta = offer.date_deadline - create_date
                offer.validity = delta.days
    
    @api.model
    def create(self, vals):
        # Crear la oferta
        offer = super(EstatePropertyOffer, self).create(vals)
        
        # Obtener la propiedad para trabajar con ella
        property_obj = self.env['estate.property'].browse(offer.property_id.id)
        
        # Actualizar el estado de la propiedad a "offer_received" si está en estado "new"
        if property_obj.state == 'new':
            # Forzar la actualización usando el método write
            property_obj.sudo().write({
                'state': 'offer_received'
            })
            # Forzar la actualización en la base de datos inmediatamente
            self.env.cr.commit()
        
        # Recalcular la mejor oferta
        property_obj._compute_best_price()
        
        return offer

    def action_accept(self):
        for offer in self:
            # Verificar si ya hay una oferta aceptada
            if any(o.status == 'accepted' and o.id != offer.id for o in offer.property_id.offer_ids):
                raise UserError("No se puede aceptar otra oferta, ya hay una aceptada.")
            
            # Actualizar estado de la oferta
            offer.status = 'accepted'
            
            # Actualizar estado y valores de la propiedad
            offer.property_id.write({
                'state': 'offer_accepted',
                'selling_price': offer.price,
                'buyer_id': offer.partner_id.id
            })
            
            # Rechazar el resto de ofertas
            other_offers = offer.property_id.offer_ids.filtered(lambda o: o.id != offer.id)
            other_offers.action_refuse()
        return True
    
    def action_refuse(self):
        for offer in self:
            offer.status = 'refused'
        return True
           
