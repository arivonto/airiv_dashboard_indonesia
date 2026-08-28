# -*- coding: utf-8 -*-
from odoo import models, fields, api

class AirivGatewayTransaction(models.Model):
    _name = 'airiv.gateway.transaction'
    _description = 'AIRIV Tri-Gateway Live Transaction Feed'
    _order = 'transaction_time desc, id desc'

    name = fields.Char(string='Transaction Reference', required=True, index=True)
    gateway = fields.Selection([
        ('midtrans', 'Midtrans (Domestic IDR)'),
        ('xendit', 'Xendit (Domestic IDR)'),
        ('paypal', 'PayPal REST v2 (Cross-Border USD/EUR)'),
    ], string='Gateway Rail', required=True, default='midtrans', index=True)

    payment_type = fields.Char(string='Channel / Method', default='QRIS')
    channel_category = fields.Selection([
        ('qris', 'QRIS (GoPay/ShopeePay/Dana)'),
        ('va', 'Bank Virtual Account'),
        ('ewallet', 'E-Wallet'),
        ('card', 'Credit / Debit Card'),
        ('cross_border', 'PayPal International FX'),
    ], string='Channel Category', default='qris', index=True)

    amount = fields.Monetary(string='Gross Amount', required=True, currency_field='currency_id')
    fee_amount = fields.Monetary(string='Gateway Fee (MDR)', default=0.0, currency_field='currency_id')
    net_amount = fields.Monetary(string='Net Settlement', compute='_compute_net_amount', store=True, currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', string='Currency', required=True, default=lambda self: self.env.company.currency_id)

    status = fields.Selection([
        ('pending', 'Pending / In Escrow'),
        ('settlement', 'Settled (Success)'),
        ('expire', 'Expired'),
        ('failed', 'Failed / Cancelled'),
    ], string='Status', default='settlement', index=True)

    transaction_time = fields.Datetime(string='Timestamp (WIB)', default=fields.Datetime.now, index=True)
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)
    customer_name = fields.Char(string='Payer / Customer Name')
    customer_phone = fields.Char(string='Payer WhatsApp / Phone')
    external_id = fields.Char(string='Gateway TxID / External Ref')
    raw_payload = fields.Text(string='Raw Webhook Payload')

    @api.depends('amount', 'fee_amount')
    def _compute_net_amount(self):
        for rec in self:
            rec.net_amount = (rec.amount or 0.0) - (rec.fee_amount or 0.0)
