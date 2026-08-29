#!/bin/bash
echo ">>> Adding /demo controller or route mapping inside airiv_dashboard_indonesia <<<"

MODULE_DIR="$HOME/odoo-stack/extra-addons/airiv_dashboard_indonesia"
mkdir -p "$MODULE_DIR/controllers"

# 1. Create a Python controller handling the /demo route
cat << 'CONTROLLER' > "$MODULE_DIR/controllers/main.py"
from odoo import http
from odoo.http import request

class AirivDemoController(http.Controller):

    @http.route('/demo', type='http', auth='none', website=True)
    def airiv_demo_landing(self, **kwargs):
        html_content = """
        <!DOCTYPE html>
        <html lang="id">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Airiv ERP Indonesia - Demo Portal</title>
            <script src="https://cdn.tailwindcss.com"></script>
        </head>
        <body class="bg-slate-50 font-sans text-slate-900 antialiased">
            <div class="min-h-screen flex flex-col justify-center items-center p-6">
                <div class="max-w-2xl w-full bg-white shadow-xl rounded-2xl p-8 border border-slate-100">
                    <div class="flex items-center space-x-3 mb-6">
                        <div class="h-3 w-3 bg-emerald-500 rounded-full animate-pulse"></div>
                        <span class="text-xs font-semibold uppercase tracking-wider text-emerald-600 bg-emerald-50 px-3 py-1 rounded-full">Odoo 18 Indonesian UMKM Edition</span>
                    </div>
                    <h1 class="text-3xl font-bold tracking-tight text-slate-900 mb-3">Airiv Executive Demo Portal</h1>
                    <p class="text-slate-600 mb-6 leading-relaxed">
                        Welcome to the live demonstration environment for Indonesian localization standards, featuring Coretax readiness, statutory 11% effective PPN calculations, and integrated WhatsApp business messaging rails.
                    </p>
                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-8">
                        <div class="p-4 bg-slate-50 rounded-xl border border-slate-200">
                            <h3 class="text-sm font-semibold text-slate-700">Tax Standard</h3>
                            <p class="text-lg font-bold text-slate-900 mt-1">PPN 11% Effective</p>
                        </div>
                        <div class="p-4 bg-slate-50 rounded-xl border border-slate-200">
                            <h3 class="text-sm font-semibold text-slate-700">Payment Gateways</h3>
                            <p class="text-lg font-bold text-slate-900 mt-1">Midtrans & Xendit</p>
                        </div>
                    </div>
                    <div class="flex flex-col sm:flex-row items-center justify-between gap-4 pt-4 border-t border-slate-100">
                        <a href="/web" class="w-full sm:w-auto text-center px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-xl shadow-sm transition-colors duration-200">
                            Access ERP Workspace
                        </a>
                        <span class="text-xs text-slate-400">Powered by Riv Cloud Management</span>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        return request.make_response(html_content, [('Content-Type', 'text/html; charset=utf-8')])
        
    @http.route('/demo/json', type='json', auth='none')
    def airiv_demo_json(self, **kwargs):
        return {
            "status": "success",
            "message": "Airiv Odoo 18 Indonesian Localization Demo API is operational.",
            "effective_ppn": 0.11,
            "gateways": ["midtrans", "xendit", "paypal"]
        }
    
    @http.route('/demo/redirect', type='http', auth='none')
    def airiv_demo_redirect(self, **kwargs):
        return request.redirect('/web')
CONTROLLER

# 2. Expose controller in __init__.py
cat << 'INIT' > "$MODULE_DIR/controllers/__init__.py"
from . import main
INIT

cat << 'MAININIT' > "$MODULE_DIR/__init__.py"
from . import controllers
MAININIT

# 3. Update manifest to include controllers
cat << 'MANIFEST' > "$MODULE_DIR/__manifest__.py"
{
    'name': 'Airiv Executive Dashboard Indonesia',
    'version': '18.0.1.0.0',
    'category': 'Extra Tools',
    'summary': 'Executive command center built natively with Odoo 18 OWL framework for Indonesian UMKM',
    'description': 'A high-performance executive command center built natively with Odoo 18 OWL framework, tailored specifically for Indonesian SMEs, local enterprises, and UMKM governance.',
    'author': 'Riv Cloud Management',
    'license': 'LGPL-3',
    'depends': ['base', 'web', 'mail'],
    'data': [
        'views/dashboard_action.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'airiv_dashboard_indonesia/static/src/js/dashboard.js',
            'airiv_dashboard_indonesia/static/src/xml/dashboard.xml',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
}
MANIFEST

echo ">>> Upgrading module in Odoo container to register demo controller <<<"
docker exec -it odoo_app odoo -d OdooAIRIV -u airiv_dashboard_indonesia --stop-after-init --db_host=odoo_db --db_user=odoo --db_password=odoo
docker restart odoo_app
sleep 3
echo ">>> Testing /demo endpoint response... <<<"
curl -I -H "Host: erp.airiv.id" http://127.0.0.1/demo
