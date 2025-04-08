from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import timedelta

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Oferta de Propiedad"
    
    price = fields.Float(string="Price")
    status = fields.Selection([
        ("accepted", "Aceptada"),
        ("refused", "Rechazada"),
    ], string="Estado", copy=False)
    partner_id = fields.Many2one("res.partner", string="Cliente", required=True)
    property_id = fields.Many2one("estate.property", string="Propiedad", required=True) 
    validity = fields.Integer(string="Validez", default=7)
    date_deadline = fields.Date(string="Fecha de Caducidad", compute="_compute_date_deadline", inverse="_inverse_date_deadline")

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date + timedelta(days=record.validity)
            else:
                record.date_deadline = fields.Date.today() + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline and record.create_date:
                # Convertir create_date (datetime) a date para poder restar
                create_date_as_date = record.create_date.date()
                delta = record.date_deadline - create_date_as_date
                record.validity = delta.days
            else:
                record.validity = (record.date_deadline - fields.Date.today()).days

    @api.model
    def create(self, vals):
        # Crear la oferta
        offer = super(EstatePropertyOffer, self).create(vals)
        
        # Actualizar el estado de la propiedad a "offer_received" si está en estado "new"
        if offer.property_id.state == 'new':
            offer.property_id.state = 'offer_received'
            
        # Calcular la mejor oferta
        offer.property_id._compute_best_price()
        
        return offer

    def action_accept(self):
        for record in self:
            # Verificar si ya hay ofertas aceptadas para esta propiedad
            if record.property_id.offer_ids.filtered(lambda o: o.status == 'accepted' and o.id != record.id):
                raise UserError("Ya existe una oferta aceptada para esta propiedad.")
            
            # Cambiar el estado de la oferta a aceptada
            record.status = "accepted"
            
            # Actualizar la propiedad con los datos de la oferta aceptada
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price
            
            # Cambiar el estado de la propiedad a "offer_accepted"
            record.property_id.state = "offer_accepted"
            
            return True
        
    def action_refuse(self):
        for record in self:
            record.status = "refused"
            return True
           
