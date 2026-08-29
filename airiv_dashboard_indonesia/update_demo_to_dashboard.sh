#!/bin/bash
echo ">>> Updating /demo endpoint to render the Airiv Command Center Dashboard directly without login <<<"

MODULE_DIR="$HOME/odoo-stack/extra-addons/airiv_dashboard_indonesia"

cat << 'CONTROLLER' > "$MODULE_DIR/controllers/main.py"
from odoo import http
from odoo.http import request

class AirivDemoController(http.Controller):

    @http.route('/demo', type='http', auth='none', website=True)
    def airiv_demo_dashboard(self, **kwargs):
        html_content = """
        <!DOCTYPE html>
        <html lang="id">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Airiv Command Center - Executive Dashboard</title>
            <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
        </head>
        <body class="bg-slate-50 font-sans text-slate-900 antialiased min-h-screen flex flex-col">
            <!-- Top Navbar -->
            <header class="bg-white border-b border-slate-200 sticky top-0 z-50">
                <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
                    <div class="flex items-center space-x-3">
                        <div class="h-3.5 w-3.5 bg-emerald-500 rounded-full animate-pulse"></div>
                        <span class="font-bold text-slate-800 text-lg tracking-tight">Airiv Command Center</span>
                        <span class="text-xs font-semibold bg-blue-50 text-blue-700 px-2.5 py-1 rounded-md border border-blue-100">Odoo 18 UMKM Edition</span>
                    </div>
                    <div class="flex items-center space-x-4">
                        <a href="/web" class="px-4 py-2 bg-slate-900 hover:bg-slate-800 text-white text-sm font-medium rounded-lg shadow-sm transition-colors">
                            ERP Workspace Login
                        </a>
                    </div>
                </div>
            </header>

            <!-- Main Dashboard Container -->
            <main class="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
                <!-- Welcome Banner -->
                <div class="bg-gradient-to-r from-slate-900 to-slate-800 rounded-2xl p-6 sm:p-8 text-white shadow-lg mb-8">
                    <div class="max-w-3xl">
                        <h1 class="text-2xl sm:text-3xl font-bold tracking-tight mb-2">Executive Governance &amp; Compliance Hub</h1>
                        <p class="text-slate-300 text-sm sm:text-base leading-relaxed">
                            High-performance enterprise command center tailored for Indonesian SMEs and UMKM. Fully integrated with Coretax, statutory tax structures, and multi-gateway rails.
                        </p>
                    </div>
                </div>

                <!-- Metrics Grid -->
                <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
                    <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-xs">
                        <p class="text-xs font-semibold uppercase tracking-wider text-slate-500 mb-1">Effective PPN Rate</p>
                        <h3 class="text-2xl font-bold text-slate-900">11%</h3>
                        <span class="text-xs text-emerald-600 font-medium mt-2 inline-block">● DPP Nilai Lain Compliant</span>
                    </div>
                    <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-xs">
                        <p class="text-xs font-semibold uppercase tracking-wider text-slate-500 mb-1">Payment Gateways</p>
                        <h3 class="text-2xl font-bold text-slate-900">Midtrans / Xendit</h3>
                        <span class="text-xs text-blue-600 font-medium mt-2 inline-block">● IDR &amp; Cross-Border Active</span>
                    </div>
                    <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-xs">
                        <p class="text-xs font-semibold uppercase tracking-wider text-slate-500 mb-1">Tax Integration</p>
                        <h3 class="text-2xl font-bold text-slate-900">Coretax / e-Faktur</h3>
                        <span class="text-xs text-emerald-600 font-medium mt-2 inline-block">● NPWP/NIK Validated</span>
                    </div>
                    <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-xs">
                        <p class="text-xs font-semibold uppercase tracking-wider text-slate-500 mb-1">Communication</p>
                        <h3 class="text-2xl font-bold text-slate-900">WhatsApp API</h3>
                        <span class="text-xs text-purple-600 font-medium mt-2 inline-block">● Fonnte / Waha Ready</span>
                    </div>
                </div>

                <!-- Operational Modules Overview -->
                <div class="bg-white rounded-2xl border border-slate-200 p-6 sm:p-8 shadow-xs">
                    <h2 class="text-lg font-bold text-slate-900 mb-4">Localized Indonesian Module Suite (17 Modules Active)</h2>
                    <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
                        <div class="p-4 bg-slate-50 rounded-xl border border-slate-100">
                            <h4 class="font-semibold text-slate-800 text-sm">Accounting &amp; Tax</h4>
                            <p class="text-xs text-slate-500 mt-1">PPh 21/23/25 computations, PPN returns, chart of accounts.</p>
                        </div>
                        <div class="p-4 bg-slate-50 rounded-xl border border-slate-100">
                            <h4 class="font-semibold text-slate-800 text-sm">Logistics Aggregators</h4>
                            <p class="text-xs text-slate-500 mt-1">Biteship &amp; RajaOngkir bindings for JNE, J&amp;T, SiCepat, GoSend.</p>
                        </div>
                        <div class="p-4 bg-slate-50 rounded-xl border border-slate-100">
                            <h4 class="font-semibold text-slate-800 text-sm">Payroll &amp; HR</h4>
                            <p class="text-xs text-slate-500 mt-1">BPJS Ketenagakerjaan/Kesehatan calculations and overtime workflows.</p>
                        </div>
                    </div>
                </div>
            </main>

            <!-- Footer -->
            <footer class="bg-white border-t border-slate-200 mt-auto py-6">
                <div class="max-w-7xl mx-auto px-4 text-center text-xs text-slate-400">
                    Airiv ERP Platform &mdash; Powered by Riv Cloud Management. Zero external server overhead.
                </div>
            </footer>
        </body>
        </html>
        """
        return request.make_response(html_content, [('Content-Type', 'text/html; charset=utf-8')])
        
    @http.route('/demo/json', type='json', auth='none')
    def airiv_demo_json(self, **kwargs):
        return {
            "status": "success",
            "message": "Airiv Command Center Dashboard API is operational.",
            "effective_ppn": 0.11,
            "gateways": ["midtrans", "xendit", "paypal"]
        }
CONTROLLER

echo ">>> Upgrading airiv_dashboard_indonesia module to apply updated controller <<<"
docker exec -it odoo_app odoo -d OdooAIRIV -u airiv_dashboard_indonesia --stop-after-init --db_host=odoo_db --db_user=odoo --db_password=odoo
docker restart odoo_app
sleep 3
echo ">>> Verification of /demo endpoint response: <<<"
curl -I -H "Host: erp.airiv.id" http://127.0.0.1/demo
