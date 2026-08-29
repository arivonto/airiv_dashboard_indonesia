# -*- coding: utf-8 -*-
import json
import logging
from datetime import datetime
from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)

class AirivShippingWebhookController(http.Controller):

    @http.route('/airiv_logistics/webhook/biteship', type='json', auth='public', methods=['POST'], csrf=False)
    def webhook_biteship(self, **kw):
        """Native Biteship Courier Tracking & POD Notification Listener"""
        try:
            payload = request.get_json_data() or {}
            event = payload.get('event', 'order.status_updated')
            waybill_id = payload.get('waybill_id', payload.get('order_id', ''))
            courier_tracking_id = payload.get('courier_tracking_id', waybill_id)
            courier_code = payload.get('courier_code', 'jne').lower()
            biteship_status = payload.get('status', 'in_transit').lower()

            status_map = {
                'allocated': 'pending_pickup',
                'picking_up': 'pending_pickup',
                'picked': 'in_transit',
                'dropping_off': 'in_transit',
                'delivered': 'delivered',
                'returned': 'returned',
                'cancelled': 'cancelled',
            }
            mapped_status = status_map.get(biteship_status, 'in_transit')

            Ship = request.env['airiv.shipping.tracker'].sudo()
            existing = Ship.search(['|', ('name', '=', courier_tracking_id), ('order_ref', '=', waybill_id)], limit=1)

            if existing:
                vals = {
                    'status': mapped_status,
                    'last_update_time': datetime.now(),
                }
                if mapped_status == 'delivered' and existing.is_cod:
                    vals['cod_status'] = 'remitted'
                existing.write(vals)
                _logger.info("[AIRIV Logistics] Updated AWB %s -> %s", courier_tracking_id, mapped_status)
                return {'status': 'success', 'awb': courier_tracking_id}
            else:
                _logger.info("[AIRIV Logistics] Received webhook for unlinked AWB %s", courier_tracking_id)
                return {'status': 'ignored', 'message': 'Tracking ref not found'}
        except Exception as e:
            _logger.error("[AIRIV Logistics] Biteship webhook error: %s", str(e))
            return {'status': 'error', 'message': str(e)}
