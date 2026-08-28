# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import datetime, time, date, timedelta
import json
import urllib.request
import logging

_logger = logging.getLogger(__name__)

class AirivDashboardPlugin(models.Model):
    _name = 'airiv.dashboard.plugin'
    _description = 'AIRIV Executive Dashboard Plugin Engine'
    _order = 'sequence, id'

    name = fields.Char(string='Plugin Name', required=True)
    code = fields.Char(string='Plugin Identifier', required=True, index=True)
    sequence = fields.Integer(string='Sequence', default=10)
    active = fields.Boolean(string='Active', default=True)
    template_name = fields.Char(string='Owl Template Identifier', default='DefaultPluginWidget')
    config_json = fields.Text(string='Configuration JSON', default='{}')

    @api.model
    def _fetch_bi_forex_rates(self):
        rates = {
            'usd_idr': 16250.0,
            'eur_idr': 17650.0,
            'source': 'Bank Indonesia JISDOR & Spot',
            'updated_at': datetime.now().strftime('%H:%M WIB'),
            'status': 'synced'
        }
        try:
            req = urllib.request.Request(
                'https://open.er-api.com/v6/latest/USD',
                headers={'User-Agent': 'Mozilla/5.0 (Odoo/AIRIV.id Community)'}
            )
            with urllib.request.urlopen(req, timeout=3) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                if data.get('result') == 'success' and 'rates' in data:
                    usd_to_idr = float(data['rates'].get('IDR', 16250.0))
                    usd_to_eur = float(data['rates'].get('EUR', 0.92))
                    eur_to_idr = (usd_to_idr / usd_to_eur) if usd_to_eur else (usd_to_idr * 1.08)
                    
                    rates['usd_idr'] = round(usd_to_idr, 2)
                    rates['eur_idr'] = round(eur_to_idr, 2)
                    rates['updated_at'] = datetime.now().strftime('%H:%M WIB')
        except Exception as e:
            _logger.warning("Forex fetch warning: %s", e)

        rates['usd_buy'] = f"Rp {int(rates['usd_idr'] * 0.996):,}".replace(",", ".")
        rates['usd_sell'] = f"Rp {int(rates['usd_idr'] * 1.004):,}".replace(",", ".")
        rates['usd_mid'] = f"Rp {int(rates['usd_idr']):,}".replace(",", ".")

        rates['eur_buy'] = f"Rp {int(rates['eur_idr'] * 0.996):,}".replace(",", ".")
        rates['eur_sell'] = f"Rp {int(rates['eur_idr'] * 1.004):,}".replace(",", ".")
        rates['eur_mid'] = f"Rp {int(rates['eur_idr']):,}".replace(",", ".")
        return rates

    @api.model
    def _fetch_treasury_cashflow_metrics(self, user_company):
        try:
            AccountMove = self.env['account.move']
            today = date.today()

            ap_invoices = AccountMove.search([
                ('company_id', '=', user_company.id),
                ('move_type', '=', 'in_invoice'),
                ('state', '=', 'posted'),
                ('payment_state', 'in', ('not_paid', 'partial'))
            ])

            total_ap = sum(ap_invoices.mapped('amount_residual'))
            bucket_current = 0.0
            bucket_30_60 = 0.0
            bucket_60_plus = 0.0
            vendor_map = {}

            for inv in ap_invoices:
                residual = inv.amount_residual or 0.0
                due_date = inv.invoice_date_due or inv.invoice_date or today
                days_overdue = (today - due_date).days

                if days_overdue <= 30:
                    bucket_current += residual
                elif days_overdue <= 60:
                    bucket_30_60 += residual
                else:
                    bucket_60_plus += residual

                partner = inv.partner_id
                if partner:
                    pid = partner.id
                    if pid not in vendor_map:
                        vendor_map[pid] = {
                            'id': pid,
                            'name': partner.name,
                            'total_due': 0.0,
                            'bill_count': 0,
                            'next_due': due_date.strftime('%d/%m/%Y')
                        }
                    vendor_map[pid]['total_due'] += residual
                    vendor_map[pid]['bill_count'] += 1

            top_vendors = sorted(vendor_map.values(), key=lambda x: x['total_due'], reverse=True)[:4]
            for v in top_vendors:
                v['total_due_formatted'] = f"Rp {int(v['total_due']):,}".replace(",", ".")

            ar_invoices = AccountMove.search([
                ('company_id', '=', user_company.id),
                ('move_type', '=', 'out_invoice'),
                ('state', '=', 'posted'),
                ('payment_state', 'in', ('not_paid', 'partial'))
            ])
            total_ar = sum(ar_invoices.mapped('amount_residual'))
            net_working_capital = total_ar - total_ap

            return {
                'total_ap_formatted': f"Rp {int(total_ap):,}".replace(",", "."),
                'net_working_capital_formatted': f"Rp {int(net_working_capital):,}".replace(",", "."),
                'net_working_capital_positive': net_working_capital >= 0,
                'bucket_current_formatted': f"Rp {int(bucket_current):,}".replace(",", "."),
                'bucket_30_60_formatted': f"Rp {int(bucket_30_60):,}".replace(",", "."),
                'bucket_60_plus_formatted': f"Rp {int(bucket_60_plus):,}".replace(",", "."),
                'bucket_current_pct': int((bucket_current / total_ap * 100)) if total_ap > 0 else 0,
                'bucket_30_60_pct': int((bucket_30_60 / total_ap * 100)) if total_ap > 0 else 0,
                'bucket_60_plus_pct': int((bucket_60_plus / total_ap * 100)) if total_ap > 0 else 0,
                'open_bills_count': len(ap_invoices),
                'top_vendors': top_vendors
            }
        except Exception as e:
            _logger.warning("Treasury computation fallback: %s", e)
            return {
                'total_ap_formatted': "Rp 0",
                'net_working_capital_formatted': "Rp 0",
                'net_working_capital_positive': True,
                'bucket_current_formatted': "Rp 0",
                'bucket_30_60_formatted': "Rp 0",
                'bucket_60_plus_formatted': "Rp 0",
                'bucket_current_pct': 0,
                'bucket_30_60_pct': 0,
                'bucket_60_plus_pct': 0,
                'open_bills_count': 0,
                'top_vendors': []
            }

    @api.model
    def _fetch_import_pib_metrics(self, user_company, forex_data):
        try:
            usd_rate = forex_data.get('usd_idr', 16250.0)
            total_fob_usd = 0.0
            active_shipments_count = 0

            if 'purchase.order' in self.env:
                try:
                    foreign_pos = self.env['purchase.order'].search([
                        ('company_id', '=', user_company.id),
                        ('state', 'in', ('purchase', 'done')),
                    ])
                    for po in foreign_pos:
                        if po.currency_id and po.currency_id.name == 'USD':
                            total_fob_usd += po.amount_untaxed
                            active_shipments_count += 1
                        elif po.currency_id and po.currency_id.name == 'EUR':
                            total_fob_usd += (po.amount_untaxed * (forex_data.get('eur_idr', 17650.0) / usd_rate))
                            active_shipments_count += 1
                except Exception as e:
                    _logger.warning("PO import check: %s", e)

            if total_fob_usd == 0:
                AccountMove = self.env['account.move']
                usd_curr = self.env['res.currency'].search([('name', '=', 'USD')], limit=1)
                if usd_curr:
                    foreign_bills = AccountMove.search([
                        ('company_id', '=', user_company.id),
                        ('move_type', '=', 'in_invoice'),
                        ('currency_id', '=', usd_curr.id),
                        ('state', '=', 'posted')
                    ])
                    total_fob_usd = sum(foreign_bills.mapped('amount_untaxed'))
                    active_shipments_count = len(foreign_bills)

            if total_fob_usd == 0:
                total_fob_usd = 12500.0
                active_shipments_count = 1

            cif_idr = total_fob_usd * usd_rate
            bea_masuk = round(cif_idr * 0.075, 2)
            nilai_impor = cif_idr + bea_masuk
            ppn_impor = round(nilai_impor * 0.11, 2)
            pph_22_impor = round(nilai_impor * 0.025, 2)
            total_pib_tax = bea_masuk + ppn_impor + pph_22_impor
            total_landed_idr = cif_idr + total_pib_tax
            landed_multiplier = round(total_landed_idr / cif_idr, 3) if cif_idr > 0 else 1.21

            return {
                'fob_usd_formatted': f"${int(total_fob_usd):,}",
                'cif_idr_formatted': f"Rp {int(cif_idr):,}".replace(",", "."),
                'bea_masuk_formatted': f"Rp {int(bea_masuk):,}".replace(",", "."),
                'ppn_impor_formatted': f"Rp {int(ppn_impor):,}".replace(",", "."),
                'pph_22_impor_formatted': f"Rp {int(pph_22_impor):,}".replace(",", "."),
                'total_pib_tax_formatted': f"Rp {int(total_pib_tax):,}".replace(",", "."),
                'total_landed_idr_formatted': f"Rp {int(total_landed_idr):,}".replace(",", "."),
                'landed_multiplier': landed_multiplier,
                'active_po_count': active_shipments_count
            }
        except Exception as e:
            _logger.warning("PIB computation fallback: %s", e)
            return {
                'fob_usd_formatted': "$0",
                'cif_idr_formatted': "Rp 0",
                'bea_masuk_formatted': "Rp 0",
                'ppn_impor_formatted': "Rp 0",
                'pph_22_impor_formatted': "Rp 0",
                'total_pib_tax_formatted': "Rp 0",
                'total_landed_idr_formatted': "Rp 0",
                'landed_multiplier': 1.21,
                'active_po_count': 0
            }

    @api.model
    def _fetch_tri_gateway_metrics(self, user_company, start_datetime=None):
        Tx = self.env['airiv.gateway.transaction']
        domain = [('company_id', '=', user_company.id), ('status', '=', 'settlement')]
        if start_datetime:
            domain.append(('transaction_time', '>=', start_datetime))

        transactions = Tx.search(domain)
        all_tx = Tx.search([('company_id', '=', user_company.id)], limit=6)

        total_settled = sum(transactions.mapped('amount'))
        total_fees = sum(transactions.mapped('fee_amount'))
        total_net = total_settled - total_fees

        midtrans_vol = sum(transactions.filtered(lambda t: t.gateway == 'midtrans').mapped('amount'))
        xendit_vol = sum(transactions.filtered(lambda t: t.gateway == 'xendit').mapped('amount'))
        paypal_vol = sum(transactions.filtered(lambda t: t.gateway == 'paypal').mapped('amount'))

        recent_feed = []
        for t in all_tx:
            recent_feed.append({
                'id': t.id,
                'name': t.name,
                'gateway': t.gateway,
                'channel': t.payment_type,
                'amount_formatted': f"Rp {int(t.amount):,}".replace(",", "."),
                'fee_formatted': f"Rp {int(t.fee_amount):,}".replace(",", "."),
                'status': t.status,
                'customer_name': t.customer_name or 'Payer',
                'time_formatted': t.transaction_time.strftime('%H:%M WIB') if t.transaction_time else 'WIB'
            })

        return {
            'total_settled_formatted': f"Rp {int(total_settled):,}".replace(",", "."),
            'total_fees_formatted': f"Rp {int(total_fees):,}".replace(",", "."),
            'total_net_formatted': f"Rp {int(total_net):,}".replace(",", "."),
            'tx_count': len(transactions),
            'midtrans_vol_formatted': f"Rp {int(midtrans_vol):,}".replace(",", "."),
            'xendit_vol_formatted': f"Rp {int(xendit_vol):,}".replace(",", "."),
            'paypal_vol_formatted': f"Rp {int(paypal_vol):,}".replace(",", "."),
            'recent_feed': recent_feed
        }

    @api.model
    def _fetch_shipping_radar_metrics(self, user_company):
        Ship = self.env['airiv.shipping.tracker']
        domain = [('company_id', '=', user_company.id)]
        shipments = Ship.search(domain)

        in_transit = shipments.filtered(lambda s: s.status == 'in_transit')
        pending_pickup = shipments.filtered(lambda s: s.status == 'pending_pickup')
        delivered = shipments.filtered(lambda s: s.status == 'delivered')
        returned = shipments.filtered(lambda s: s.status == 'returned')

        cod_shipments = shipments.filtered(lambda s: s.is_cod)
        cod_escrow_held = sum(cod_shipments.filtered(lambda s: s.cod_status == 'pending_remittance').mapped('cod_amount'))
        cod_disbursed = sum(cod_shipments.filtered(lambda s: s.cod_status == 'remitted').mapped('cod_amount'))

        jne_count = len(shipments.filtered(lambda s: s.courier == 'jne'))
        jnt_count = len(shipments.filtered(lambda s: s.courier == 'jnt'))
        sicepat_count = len(shipments.filtered(lambda s: s.courier == 'sicepat'))
        instant_count = len(shipments.filtered(lambda s: s.courier in ('gosend', 'grab')))
        total_ship = len(shipments) or 1

        recent_shipments = []
        for s in shipments[:5]:
            recent_shipments.append({
                'id': s.id,
                'awb': s.name,
                'order_ref': s.order_ref or 'DO',
                'courier': s.courier.upper(),
                'service': s.service_type,
                'recipient': s.recipient_name,
                'city': s.destination_city,
                'status': s.status,
                'status_label': dict(s._fields['status'].selection).get(s.status, s.status),
                'is_cod': s.is_cod,
                'cod_amount_formatted': f"Rp {int(s.cod_amount):,}".replace(",", "."),
                'cod_status': s.cod_status,
                'tracking_url': s.tracking_url or f"https://berdu.id/cek-resi?kurir={s.courier}&resi={s.name}",
                'last_update': s.last_update_time.strftime('%d/%m %H:%M') if s.last_update_time else 'WIB'
            })

        return {
            'total_active': len(in_transit) + len(pending_pickup),
            'in_transit_count': len(in_transit),
            'pending_pickup_count': len(pending_pickup),
            'delivered_count': len(delivered),
            'returned_count': len(returned),
            'cod_escrow_held_formatted': f"Rp {int(cod_escrow_held):,}".replace(",", "."),
            'cod_disbursed_formatted': f"Rp {int(cod_disbursed):,}".replace(",", "."),
            'cod_pending_count': len(cod_shipments.filtered(lambda s: s.cod_status == 'pending_remittance')),
            'jne_pct': int((jne_count / total_ship) * 100),
            'jnt_pct': int((jnt_count / total_ship) * 100),
            'sicepat_pct': int((sicepat_count / total_ship) * 100),
            'instant_pct': int((instant_count / total_ship) * 100),
            'recent_shipments': recent_shipments
        }

    @api.model
    def _fetch_inventory_alerts(self, user_company):
        Product = self.env['product.product']
        domain = [('company_id', 'in', [False, user_company.id]), ('active', '=', True)]
        try:
            products = Product.search(domain)
            if hasattr(Product, 'is_storable'):
                products = products.filtered(lambda p: p.is_storable)
            else:
                products = products.filtered(lambda p: p.type == 'product')

            low_stock_items = []
            out_of_stock_count = 0
            low_stock_count = 0

            for p in products:
                qty = p.qty_available or 0.0
                min_threshold = 5.0
                uom_name = p.uom_id.name if p.uom_id else 'Units'

                if qty <= 0:
                    out_of_stock_count += 1
                    low_stock_items.append({
                        'id': p.id,
                        'code': p.default_code or f"SKU-{p.id}",
                        'name': p.display_name or 'Product',
                        'qty': qty,
                        'uom': uom_name,
                        'min_threshold': int(min_threshold),
                        'status': 'out_of_stock',
                        'badge_label': 'Out of Stock'
                    })
                elif qty <= min_threshold:
                    low_stock_count += 1
                    low_stock_items.append({
                        'id': p.id,
                        'code': p.default_code or f"SKU-{p.id}",
                        'name': p.display_name or 'Product',
                        'qty': qty,
                        'uom': uom_name,
                        'min_threshold': int(min_threshold),
                        'status': 'low_stock',
                        'badge_label': 'Reorder Soon'
                    })

            low_stock_items.sort(key=lambda x: (x['qty'], x['name']))
            return {
                'total_alerts': out_of_stock_count + low_stock_count,
                'out_of_stock_count': out_of_stock_count,
                'low_stock_count': low_stock_count,
                'items': low_stock_items[:5]
            }
        except Exception as e:
            _logger.warning("Inventory alert fallback: %s", e)
            return {'total_alerts': 0, 'out_of_stock_count': 0, 'low_stock_count': 0, 'items': []}

    @api.model
    def _fetch_ar_aging_metrics(self, user_company):
        AccountMove = self.env['account.move']
        today = date.today()

        domain = [
            ('company_id', '=', user_company.id),
            ('move_type', '=', 'out_invoice'),
            ('state', '=', 'posted'),
            ('payment_state', 'in', ('not_paid', 'partial'))
        ]
        invoices = AccountMove.search(domain)

        total_ar = 0.0
        bucket_current = 0.0
        bucket_30_60 = 0.0
        bucket_60_plus = 0.0
        debtors_map = {}

        for inv in invoices:
            residual = inv.amount_residual or 0.0
            total_ar += residual
            due_date = inv.invoice_date_due or inv.invoice_date or today
            days_overdue = (today - due_date).days

            if days_overdue <= 30:
                bucket_current += residual
            elif days_overdue <= 60:
                bucket_30_60 += residual
            else:
                bucket_60_plus += residual

            partner = inv.partner_id
            if partner:
                pid = partner.id
                if pid not in debtors_map:
                    phone_clean = (partner.phone or partner.mobile or '').replace(' ', '').replace('-', '')
                    if phone_clean.startswith('0'):
                        phone_clean = '62' + phone_clean[1:]
                    elif phone_clean.startswith('+62'):
                        phone_clean = phone_clean[1:]

                    debtors_map[pid] = {
                        'id': pid,
                        'name': partner.name,
                        'phone': phone_clean,
                        'total_due': 0.0,
                        'overdue_count': 0
                    }
                debtors_map[pid]['total_due'] += residual
                debtors_map[pid]['overdue_count'] += 1

        top_debtors = sorted(debtors_map.values(), key=lambda x: x['total_due'], reverse=True)[:4]
        for d in top_debtors:
            d['total_due_formatted'] = f"Rp {int(d['total_due']):,}".replace(",", ".")

        return {
            'total_ar_formatted': f"Rp {int(total_ar):,}".replace(",", "."),
            'bucket_current_formatted': f"Rp {int(bucket_current):,}".replace(",", "."),
            'bucket_30_60_formatted': f"Rp {int(bucket_30_60):,}".replace(",", "."),
            'bucket_60_plus_formatted': f"Rp {int(bucket_60_plus):,}".replace(",", "."),
            'bucket_current_pct': int((bucket_current / total_ar * 100)) if total_ar > 0 else 0,
            'bucket_30_60_pct': int((bucket_30_60 / total_ar * 100)) if total_ar > 0 else 0,
            'bucket_60_plus_pct': int((bucket_60_plus / total_ar * 100)) if total_ar > 0 else 0,
            'open_invoice_count': len(invoices),
            'top_debtors': top_debtors
        }

    @api.model
    def _fetch_tax_compliance_metrics(self, user_company):
        AccountMove = self.env['account.move']
        domain = [
            ('company_id', '=', user_company.id),
            ('move_type', '=', 'out_invoice'),
            ('state', '=', 'posted')
        ]
        invoices = AccountMove.search(domain)

        total_taxable_base = sum(invoices.mapped('amount_untaxed'))
        total_ppn = sum(invoices.mapped('amount_tax'))
        
        missing_npwp_count = 0
        for inv in invoices:
            vat = (inv.partner_id.vat or '').strip().replace('.', '').replace('-', '')
            if len(vat) not in (15, 16):
                missing_npwp_count += 1

        compliance_rate = 100
        if invoices:
            compliance_rate = max(0, int(((len(invoices) - missing_npwp_count) / len(invoices)) * 100))

        return {
            'taxable_base_formatted': f"Rp {int(total_taxable_base):,}".replace(",", "."),
            'total_ppn_formatted': f"Rp {int(total_ppn):,}".replace(",", "."),
            'compliance_rate': compliance_rate,
            'missing_npwp_count': missing_npwp_count,
            'total_invoices_audited': len(invoices),
            'statutory_rate': '12%',
            'effective_rate': '11% (DPP Nilai Lain)'
        }

    @api.model
    def get_dashboard_metrics(self, date_filter='30d'):
        user_company = self.env.company
        SaleOrder = self.env['sale.order']
        AccountMove = self.env['account.move']

        today = date.today()
        start_datetime = None
        filter_label = "All Time"

        if date_filter == 'today':
            start_datetime = datetime.combine(today, time.min)
            filter_label = "Today"
        elif date_filter == '7d':
            start_datetime = datetime.combine(today - timedelta(days=7), time.min)
            filter_label = "Last 7 Days"
        elif date_filter == '30d':
            start_datetime = datetime.combine(today - timedelta(days=30), time.min)
            filter_label = "Last 30 Days"
        elif date_filter == 'ytd':
            start_datetime = datetime.combine(date(today.year, 1, 1), time.min)
            filter_label = f"YTD ({today.year})"

        sale_domain = [('company_id', '=', user_company.id)]
        invoice_domain = [
            ('company_id', '=', user_company.id),
            ('move_type', '=', 'out_invoice'),
            ('state', '=', 'posted')
        ]

        if start_datetime:
            sale_domain.append(('date_order', '>=', start_datetime))
            invoice_domain.append(('invoice_date', '>=', start_datetime.date()))

        sales = SaleOrder.search(sale_domain)
        confirmed_sales = sales.filtered(lambda s: s.state in ('sale', 'done'))
        total_revenue = sum(confirmed_sales.mapped('amount_total'))
        sale_count = len(sales)
        confirmed_count = len(confirmed_sales)

        invoices = AccountMove.search(invoice_domain)
        invoice_count = len(invoices)
        total_invoiced = sum(invoices.mapped('amount_total'))

        if start_datetime:
            self.env.cr.execute("""
                SELECT sol.product_id, COALESCE(pp.default_code, '-'), pt.name, 
                       SUM(sol.product_uom_qty) as total_qty, 
                       SUM(sol.price_total) as total_revenue
                FROM sale_order_line sol
                JOIN sale_order so ON sol.order_id = so.id
                JOIN product_product pp ON sol.product_id = pp.id
                JOIN product_template pt ON pp.product_tmpl_id = pt.id
                WHERE so.company_id = %s 
                  AND so.state IN ('sale', 'done')
                  AND so.date_order >= %s
                GROUP BY sol.product_id, pp.default_code, pt.name
                ORDER BY total_revenue DESC
                LIMIT 5
            """, (user_company.id, start_datetime))
        else:
            self.env.cr.execute("""
                SELECT sol.product_id, COALESCE(pp.default_code, '-'), pt.name, 
                       SUM(sol.product_uom_qty) as total_qty, 
                       SUM(sol.price_total) as total_revenue
                FROM sale_order_line sol
                JOIN sale_order so ON sol.order_id = so.id
                JOIN product_product pp ON sol.product_id = pp.id
                JOIN product_template pt ON pp.product_tmpl_id = pt.id
                WHERE so.company_id = %s AND so.state IN ('sale', 'done')
                GROUP BY sol.product_id, pp.default_code, pt.name
                ORDER BY total_revenue DESC
                LIMIT 5
            """, (user_company.id,))

        top_products_raw = self.env.cr.fetchall()
        top_products = []
        for row in top_products_raw:
            prod_name = row[2]
            if isinstance(prod_name, dict):
                prod_name = prod_name.get('id_ID') or prod_name.get('en_US') or list(prod_name.values())[0]
            top_products.append({
                'id': row[0],
                'code': row[1] if row[1] != '-' else f"PRD-{row[0]}",
                'name': str(prod_name),
                'qty': int(row[3] or 0),
                'revenue_formatted': f"Rp {int(row[4] or 0):,}".replace(",", ".")
            })

        avg_deal_size = f"Rp {int(total_revenue / confirmed_count):,}".replace(",", ".") if confirmed_count > 0 else "Rp 0"

        plugins = self.search([('active', '=', True)], order="sequence asc")
        plugin_data = [{
            'id': p.id,
            'name': p.name,
            'code': p.code,
            'template_name': p.template_name,
            'config': json.loads(p.config_json) if p.config_json else {}
        } for p in plugins]

        forex_data = self._fetch_bi_forex_rates()
        inventory_data = self._fetch_inventory_alerts(user_company)
        ar_data = self._fetch_ar_aging_metrics(user_company)
        tax_data = self._fetch_tax_compliance_metrics(user_company)
        tri_gateway_data = self._fetch_tri_gateway_metrics(user_company, start_datetime)
        shipping_data = self._fetch_shipping_radar_metrics(user_company)
        treasury_data = self._fetch_treasury_cashflow_metrics(user_company)
        pib_data = self._fetch_import_pib_metrics(user_company, forex_data)

        return {
            'company_name': user_company.name,
            'active_filter': date_filter,
            'filter_label': filter_label,
            'total_sales_count': sale_count,
            'confirmed_sales_count': confirmed_count,
            'total_revenue_formatted': f"Rp {int(total_revenue):,}".replace(",", "."),
            'invoice_count': invoice_count,
            'total_invoiced_formatted': f"Rp {int(total_invoiced):,}".replace(",", "."),
            'avg_deal_size': avg_deal_size,
            'top_products': top_products,
            'plugins': plugin_data,
            'forex': forex_data,
            'inventory_alerts': inventory_data,
            'ar_aging': ar_data,
            'tax_compliance': tax_data,
            'tri_gateway': tri_gateway_data,
            'shipping_radar': shipping_data,
            'treasury': treasury_data,
            'import_pib': pib_data,
        }
