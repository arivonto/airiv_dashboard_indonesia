#!/bin/bash
echo ">>> Fixing Odoo 18 OWL Client Action registration and bundle loading <<<"

MODULE_DIR="$HOME/odoo-stack/extra-addons/airiv_dashboard_indonesia"

# 1. Update manifest to ensure assets are correctly loaded into web.assets_backend
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

# 2. Re-create the JavaScript file with explicit Odoo module syntax and robust registry mapping
cat << 'JS' > "$MODULE_DIR/static/src/js/dashboard.js"
/** @odoo-module */

import { registry } from "@web/core/registry";
import { Component } from "@owl";

export class ExecutiveDashboard extends Component {
    static template = "airiv_dashboard_indonesia.ExecutiveDashboard";
}

registry.category("actions").add("airiv_dashboard_indonesia.ExecutiveDashboard", ExecutiveDashboard);
JS

# 3. Re-create the XML template
cat << 'TEMPLATE' > "$MODULE_DIR/static/src/xml/dashboard.xml"
<templates xml:space="preserve">
    <t t-name="airiv_dashboard_indonesia.ExecutiveDashboard">
        <div class="o_dashboard_container p-4 bg-slate-50 min-h-screen">
            <div class="card shadow-sm p-4 border-0 rounded-3 bg-white">
                <h1 class="text-xl font-bold text-slate-800 mb-2">Airiv Executive Dashboard Indonesia</h1>
                <p class="text-slate-600">Odoo 18 Native OWL Command Center for Indonesian UMKM and SMB Governance.</p>
                <div class="row mt-4">
                    <div class="col-md-4 mb-3">
                        <div class="p-3 bg-light rounded border">
                            <h3 class="text-sm font-semibold text-slate-500">Active PPN Rate</h3>
                            <p class="text-2xl font-bold text-slate-900 mt-1">11% Effective</p>
                        </div>
                    </div>
                    <div class="col-md-4 mb-3">
                        <div class="p-3 bg-light rounded border">
                            <h3 class="text-sm font-semibold text-slate-500">Gateway Status</h3>
                            <p class="text-2xl font-bold text-green-600 mt-1">Connected (IDR / USD)</p>
                        </div>
                    </div>
                    <div class="col-md-4 mb-3">
                        <div class="p-3 bg-light rounded border">
                            <h3 class="text-sm font-semibold text-slate-500">Compliance</h3>
                            <p class="text-2xl font-bold text-blue-600 mt-1">Coretax Ready</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </t>
</templates>
TEMPLATE

echo ">>> Upgrading airiv_dashboard_indonesia module and clearing assets cache <<<"
docker exec -it odoo_app odoo -d OdooAIRIV -u airiv_dashboard_indonesia --stop-after-init --db_host=odoo_db --db_user=odoo --db_password=odoo
docker restart odoo_app
echo ">>> Action registry fix applied and container restarted successfully <<<"
