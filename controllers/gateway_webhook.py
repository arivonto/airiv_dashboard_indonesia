# -*- coding: utf-8 -*-
import json
import logging
from datetime import datetime
from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)

class AirivGatewayWebhookController(http.Controller):

    @http.route('/airiv_gateway/webhook/midtrans', type='json', auth='public', methods=['POST'], csrf=False)
    def webhook_midtrans(self, **kw):
        """Native Midtrans SNAP & Core API Notification Listener"""
        try:
            payload = request.get_json_data() or {}
            order_id = payload.get('order_id', f"MDT-{int(datetime.now().timestamp())}")
            gross_amount = float(payload.get('gross_amount', 0.0))
            payment_type = payload.get('payment_type', 'qris')
            transaction_status = payload.get('transaction_status', 'settlement')
            fraud_status = payload.get('fraud_status', 'accept')

            status = 'pending'
            if transaction_status in ('capture', 'settlement') and fraud_status == 'accept':
                status = 'settlement'
            elif transaction_status in ('deny', 'cancel', 'expire'):
                status = 'expire' if transaction_status == 'expire' else 'failed'

            channel_cat = 'qris'
            fee = 0.0
            if payment_type in ('qris', 'gopay', 'shopeepay'):
                channel_cat = 'qris'
                fee = round(gross_amount * 0.007, 2)
            elif 'va' in payment_type or payment_type in ('bank_transfer', 'echannel'):
                channel_cat = 'va'
                fee = 4000.0
            elif payment_type in ('credit_card', 'card'):
                channel_cat = 'card'
                fee = round((gross_amount * 0.029) + 2000.0, 2)
            else:
                channel_cat = 'ewallet'
                fee = round(gross_amount * 0.015, 2)

            company = request.env['res.company'].sudo().search([], limit=1)
            idr_currency = request.env['res.currency'].sudo().search([('name', '=', 'IDR')], limit=1) or company.currency_id

            Tx = request.env['airiv.gateway.transaction'].sudo()
            existing = Tx.search([('name', '=', order_id)], limit=1)
            vals = {
                'name': order_id,
                'gateway': 'midtrans',
                'payment_type': payment_type.upper(),
                'channel_category': channel_cat,
                'amount': gross_amount,
                'fee_amount': fee,
                'currency_id': idr_currency.id,
                'status': status,
                'transaction_time': datetime.now(),
                'company_id': company.id,
                'customer_name': payload.get('customer_details', {}).get('first_name', 'Customer Midtrans'),
                'customer_phone': payload.get('customer_details', {}).get('phone', ''),
                'external_id': payload.get('transaction_id', ''),
                'raw_payload': json.dumps(payload),
            }

            if existing:
                existing.write(vals)
                tx_record = existing
            else:
                tx_record = Tx.create(vals)

            _logger.info("[AIRIV Gateway] Midtrans webhook processed: %s (%s)", order_id, status)
            return {'status': 'success', 'order_id': order_id, 'tx_id': tx_record.id}
        except Exception as e:
            _logger.error("[AIRIV Gateway] Midtrans webhook error: %s", str(e))
            return {'status': 'error', 'message': str(e)}

    @http.route('/airiv_gateway/webhook/xendit', type='json', auth='public', methods=['POST'], csrf=False)
    def webhook_xendit(self, **kw):
        """Native Xendit Invoice & Virtual Account Webhook Listener"""
        try:
            payload = request.get_json_data() or {}
            external_id = payload.get('external_id', f"XND-{int(datetime.now().timestamp())}")
            amount = float(payload.get('amount', payload.get('paid_amount', 0.0)))
            xendit_status = str(payload.get('status', 'PAID')).upper()
            payment_method = payload.get('payment_method', 'VIRTUAL_ACCOUNT')
            payment_channel = payload.get('payment_channel', 'BCA')

            status = 'settlement' if xendit_status in ('PAID', 'SETTLED', 'COMPLETED') else 'pending'
            if xendit_status in ('EXPIRED', 'FAILED'):
                status = 'expire' if xendit_status == 'EXPIRED' else 'failed'

            channel_cat = 'va'
            fee = 4000.0
            if 'QR' in str(payment_method) or 'QRIS' in str(payment_channel):
                channel_cat = 'qris'
                fee = round(amount * 0.007, 2)
            elif 'EWALLET' in str(payment_method) or payment_channel in ('OVO', 'DANA', 'LINKAJA', 'SHOPEEPAY'):
                channel_cat = 'ewallet'
                fee = round(amount * 0.015, 2)
            elif 'CARD' in str(payment_method):
                channel_cat = 'card'
                fee = round((amount * 0.029) + 2000.0, 2)

            company = request.env['res.company'].sudo().search([], limit=1)
            idr_currency = request.env['res.currency'].sudo().search([('name', '=', 'IDR')], limit=1) or company.currency_id

            Tx = request.env['airiv.gateway.transaction'].sudo()
            existing = Tx.search([('name', '=', external_id)], limit=1)
            vals = {
                'name': external_id,
                'gateway': 'xendit',
                'payment_type': f"{payment_method} ({payment_channel})",
                'channel_category': channel_cat,
                'amount': amount,
                'fee_amount': fee,
                'currency_id': idr_currency.id,
                'status': status,
                'transaction_time': datetime.now(),
                'company_id': company.id,
                'customer_name': payload.get('payer_email', payload.get('customer_name', 'Customer Xendit')),
                'customer_phone': payload.get('customer_phone', ''),
                'external_id': payload.get('id', ''),
                'raw_payload': json.dumps(payload),
            }

            if existing:
                existing.write(vals)
                tx_record = existing
            else:
                tx_record = Tx.create(vals)

            _logger.info("[AIRIV Gateway] Xendit webhook processed: %s (%s)", external_id, status)
            return {'status': 'success', 'external_id': external_id, 'tx_id': tx_record.id}
        except Exception as e:
            _logger.error("[AIRIV Gateway] Xendit webhook error: %s", str(e))
            return {'status': 'error', 'message': str(e)}

    @http.route('/airiv_gateway/webhook/paypal', type='json', auth='public', methods=['POST'], csrf=False)
    def webhook_paypal(self, **kw):
        """Native PayPal REST API v2 Cross-Border Settlement Listener"""
        try:
            payload = request.get_json_data() or {}
            event_type = payload.get('event_type', 'PAYMENT.CAPTURE.COMPLETED')
            resource = payload.get('resource', {})
            order_id = resource.get('id', f"PAYPAL-{int(datetime.now().timestamp())}")
            
            amount_obj = resource.get('amount', {})
            gross_usd = float(amount_obj.get('value', 0.0))
            currency_code = amount_obj.get('currency_code', 'USD')

            Plugin = request.env['airiv.dashboard.plugin'].sudo()
            forex = Plugin._fetch_bi_forex_rates()
            rate = forex.get('usd_idr', 16250.0) if currency_code == 'USD' else forex.get('eur_idr', 17650.0)
            gross_idr = gross_usd * rate
            fee_idr = round(gross_idr * 0.044 + 4500, 2)

            status = 'settlement' if event_type in ('PAYMENT.CAPTURE.COMPLETED', 'CHECKOUT.ORDER.APPROVED') else 'pending'

            company = request.env['res.company'].sudo().search([], limit=1)
            idr_currency = request.env['res.currency'].sudo().search([('name', '=', 'IDR')], limit=1) or company.currency_id

            Tx = request.env['airiv.gateway.transaction'].sudo()
            vals = {
                'name': order_id,
                'gateway': 'paypal',
                'payment_type': f"PayPal REST v2 ({currency_code})",
                'channel_category': 'cross_border',
                'amount': gross_idr,
                'fee_amount': fee_idr,
                'currency_id': idr_currency.id,
                'status': status,
                'transaction_time': datetime.now(),
                'company_id': company.id,
                'customer_name': resource.get('payer', {}).get('name', {}).get('given_name', 'Global Buyer'),
                'customer_phone': '',
                'external_id': payload.get('id', ''),
                'raw_payload': json.dumps(payload),
            }
            tx_record = Tx.create(vals)
            _logger.info("[AIRIV Gateway] PayPal webhook processed: %s", order_id)
            return {'status': 'success', 'order_id': order_id, 'tx_id': tx_record.id}
        except Exception as e:
            _logger.error("[AIRIV Gateway] PayPal webhook error: %s", str(e))
            return {'status': 'error', 'message': str(e)}
