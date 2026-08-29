# -*- coding: utf-8 -*-
import io
import csv
from datetime import datetime
from odoo import http
from odoo.http import request, content_disposition

class AirivDashboardExportController(http.Controller):

    @http.route('/airiv_dashboard/export_excel', type='http', auth='user', methods=['GET'])
    def export_excel(self, date_filter='30d', **kw):
        Plugin = request.env['airiv.dashboard.plugin']
        data = Plugin.get_dashboard_metrics(date_filter=date_filter)

        output = io.BytesIO()
        try:
            from odoo.tools.misc import xlsxwriter
            workbook = xlsxwriter.Workbook(output, {'in_memory': True})
            worksheet = workbook.add_worksheet('Executive Report')

            title_fmt = workbook.add_format({'bold': True, 'font_size': 14, 'font_color': '#0f172a'})
            header_fmt = workbook.add_format({'bold': True, 'bg_color': '#f1f5f9', 'border': 1, 'font_size': 10})
            cell_fmt = workbook.add_format({'border': 1, 'font_size': 10})
            money_fmt = workbook.add_format({'border': 1, 'font_size': 10, 'align': 'right', 'bold': True})

            worksheet.set_column('A:A', 22)
            worksheet.set_column('B:B', 38)
            worksheet.set_column('C:C', 18)
            worksheet.set_column('D:D', 24)

            worksheet.write(0, 0, f"AIRIV Command Center - Executive Telemetry ({data.get('filter_label')})", title_fmt)
            worksheet.write(1, 0, f"Tenant: {data.get('company_name')} | Generated: {datetime.now().strftime('%d/%m/%Y %H:%M')} WIB")

            worksheet.write(3, 0, "Core Metric KPI", header_fmt)
            worksheet.write(3, 1, "Realized Value", header_fmt)
            worksheet.write(4, 0, "Sales Revenue", cell_fmt)
            worksheet.write(4, 1, data.get('total_revenue_formatted'), money_fmt)
            worksheet.write(5, 0, "Confirmed Orders", cell_fmt)
            worksheet.write(5, 1, data.get('confirmed_sales_count'), cell_fmt)
            worksheet.write(6, 0, "Average Deal Velocity", cell_fmt)
            worksheet.write(6, 1, data.get('avg_deal_size'), money_fmt)
            worksheet.write(7, 0, "Billed Invoices", cell_fmt)
            worksheet.write(7, 1, data.get('total_invoiced_formatted'), money_fmt)

            forex = data.get('forex', {})
            worksheet.write(8, 0, "USD / IDR (JISDOR)", cell_fmt)
            worksheet.write(8, 1, forex.get('usd_mid', '-'), money_fmt)
            worksheet.write(9, 0, "EUR / IDR (JISDOR)", cell_fmt)
            worksheet.write(9, 1, forex.get('eur_mid', '-'), money_fmt)

            worksheet.write(11, 0, "SKU / Code", header_fmt)
            worksheet.write(11, 1, "Product / Service Name", header_fmt)
            worksheet.write(11, 2, "Units Sold", header_fmt)
            worksheet.write(11, 3, "Total Revenue", header_fmt)

            row = 12
            for item in data.get('top_products', []):
                worksheet.write(row, 0, item.get('code'), cell_fmt)
                worksheet.write(row, 1, item.get('name'), cell_fmt)
                worksheet.write(row, 2, f"{item.get('qty')} units", cell_fmt)
                worksheet.write(row, 3, item.get('revenue_formatted'), money_fmt)
                row += 1

            workbook.close()
            output.seek(0)
            filename = f"AIRIV_Executive_Report_{date_filter}_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx"
            return request.make_response(
                output.getvalue(),
                headers=[
                    ('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
                    ('Content-Disposition', content_disposition(filename))
                ]
            )
        except Exception:
            output_csv = io.StringIO()
            writer = csv.writer(output_csv)
            writer.writerow(["AIRIV.id Executive Metrics", data.get('filter_label')])
            writer.writerow(["Tenant", data.get('company_name')])
            writer.writerow(["Total Revenue", data.get('total_revenue_formatted')])
            writer.writerow([])
            writer.writerow(["SKU", "Product Name", "Units", "Revenue"])
            for item in data.get('top_products', []):
                writer.writerow([item.get('code'), item.get('name'), item.get('qty'), item.get('revenue_formatted')])
            filename = f"AIRIV_Executive_Report_{date_filter}.csv"
            return request.make_response(
                output_csv.getvalue().encode('utf-8'),
                headers=[
                    ('Content-Type', 'text/csv; charset=utf-8'),
                    ('Content-Disposition', content_disposition(filename))
                ]
            )

    @http.route('/airiv_dashboard/export_pdf', type='http', auth='user', methods=['GET'])
    def export_pdf(self, date_filter='30d', **kw):
        Plugin = request.env['airiv.dashboard.plugin']
        data = Plugin.get_dashboard_metrics(date_filter=date_filter)

        products_html = ""
        for p in data.get('top_products', []):
            products_html += f"""
            <tr>
                <td><code>{p['code']}</code></td>
                <td><strong>{p['name']}</strong></td>
                <td style="text-align:center;">{p['qty']} units</td>
                <td style="text-align:right; font-weight:bold; color:#16a34a;">{p['revenue_formatted']}</td>
            </tr>
            """

        if not products_html:
            products_html = "<tr><td colspan='4' style='text-align:center; padding:20px; color:#64748b;'>No confirmed sales recorded for this period.</td></tr>"

        forex = data.get('forex', {})
        html_doc = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8"/>
    <title>AIRIV Executive Report</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; padding: 30px; color: #0f172a; margin: 0; }}
        .header {{ border-bottom: 3px solid #2563eb; padding-bottom: 12px; margin-bottom: 24px; }}
        .title {{ font-size: 22px; font-weight: bold; color: #0f172a; margin: 0; }}
        .meta {{ font-size: 12px; color: #64748b; margin-top: 6px; }}
        .grid {{ display: flex; gap: 12px; margin-bottom: 24px; }}
        .card {{ flex: 1; border: 1px solid #e2e8f0; border-radius: 6px; padding: 12px; background: #f8fafc; }}
        .label {{ font-size: 10px; text-transform: uppercase; color: #64748b; font-weight: bold; }}
        .val {{ font-size: 17px; font-weight: bold; margin-top: 4px; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 12px; }}
        th {{ background: #f1f5f9; text-align: left; padding: 10px 8px; border-bottom: 2px solid #cbd5e1; font-weight: bold; }}
        td {{ padding: 10px 8px; border-bottom: 1px solid #e2e8f0; }}
        .badge {{ display: inline-block; padding: 2px 6px; background: #2563eb; color: #fff; border-radius: 4px; font-size: 10px; }}
        @media print {{
            body {{ padding: 0; }}
            .no-print {{ display: none; }}
        }}
    </style>
</head>
<body onload="window.print()">
    <div class="header">
        <div class="title">AIRIV Command Center &bull; Executive Telemetry Report</div>
        <div class="meta">
            Tenant: <strong>{data.get('company_name')}</strong> | 
            Timeframe: <strong>{data.get('filter_label')}</strong> | 
            Generated: <strong>{datetime.now().strftime('%d %B %Y %H:%M')} WIB</strong>
        </div>
    </div>

    <div class="grid">
        <div class="card">
            <div class="label">Sales Revenue</div>
            <div class="val" style="color: #16a34a;">{data.get('total_revenue_formatted')}</div>
        </div>
        <div class="card">
            <div class="label">Avg Deal Velocity</div>
            <div class="val" style="color: #2563eb;">{data.get('avg_deal_size')}</div>
        </div>
        <div class="card">
            <div class="label">Billed Invoices</div>
            <div class="val" style="color: #0891b2;">{data.get('total_invoiced_formatted')}</div>
        </div>
        <div class="card">
            <div class="label">USD/IDR (JISDOR)</div>
            <div class="val">{forex.get('usd_mid', '-')}</div>
        </div>
    </div>

    <h4 style="margin-bottom: 8px; color: #0f172a;">Top Performing Products & Services ({data.get('filter_label')})</h4>
    <table>
        <thead>
            <tr>
                <th>SKU / Code</th>
                <th>Product Name</th>
                <th style="text-align:center;">Units Sold</th>
                <th style="text-align:right;">Realized Revenue</th>
            </tr>
        </thead>
        <tbody>
            {products_html}
        </tbody>
    </table>
</body>
</html>
"""
        return request.make_response(
            html_doc,
            headers=[('Content-Type', 'text/html; charset=utf-8')]
        )
