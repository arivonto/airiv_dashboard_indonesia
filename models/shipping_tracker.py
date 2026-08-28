# -*- coding: utf-8 -*-
from odoo import models, fields, api

class AirivShippingTracker(models.Model):
    _name = 'airiv.shipping.tracker'
    _description = 'AIRIV Domestic Courier & COD Settlement Radar'
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Tracking / Resi Number (AWB)', required=True, index=True)
    order_ref = fields.Char(string='Order Reference / DO', index=True)
    
    courier = fields.Selection([
        ('jne', 'JNE Express'),
        ('jnt', 'J&T Express'),
        ('sicepat', 'SiCepat Ekspres'),
        ('anteraja', 'Anteraja'),
        ('gosend', 'GoSend Instant / SameDay'),
        ('grab', 'GrabExpress'),
        ('ninja', 'Ninja Xpress'),
    ], string='Courier Carrier', required=True, default='jne', index=True)

    service_type = fields.Char(string='Service Type', default='REG') # e.g. REG, YES, EZ, GOKIL, Instant
    aggregator = fields.Selection([
        ('biteship', 'Biteship API'),
        ('rajaongkir', 'RajaOngkir Pro'),
        ('direct', 'Direct Courier API'),
    ], string='Logistics Gateway', default='biteship', index=True)

    status = fields.Selection([
        ('pending_pickup', 'Pending Pickup / Manifest'),
        ('in_transit', 'In Transit (On Delivery)'),
        ('delivered', 'Delivered (POD)'),
        ('returned', 'Returned (RTS / Issue)'),
        ('cancelled', 'Cancelled'),
    ], string='Fulfillment Status', default='in_transit', index=True)

    recipient_name = fields.Char(string='Recipient / Customer Name', required=True)
    recipient_phone = fields.Char(string='Recipient WhatsApp / Phone')
    destination_city = fields.Char(string='Destination Area / Kota', default='Jakarta Selatan')

    is_cod = fields.Boolean(string='COD (Cash on Delivery)', default=False, index=True)
    cod_amount = fields.Monetary(string='COD Amount', default=0.0, currency_field='currency_id')
    cod_status = fields.Selection([
        ('not_cod', 'Non-COD'),
        ('pending_remittance', 'Held in Escrow (Pending Remittance)'),
        ('remitted', 'Remitted to Bank (Disbursed)'),
    ], string='COD Settlement Status', default='not_cod', index=True)

    shipping_cost = fields.Monetary(string='Shipping Tariff', default=0.0, currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id)
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)
    last_update_time = fields.Datetime(string='Last Telemetry Update', default=fields.Datetime.now)
    tracking_url = fields.Char(string='Live Tracking URL')
