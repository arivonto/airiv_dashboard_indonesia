#!/bin/bash
echo ">>> Applying Odoo 18 compliant JS module format for client action registry <<<"

MODULE_DIR="$HOME/odoo-stack/extra-addons/airiv_dashboard_indonesia"

# 1. Update dashboard.js to use exact Odoo 18 module syntax matching web.assets_backend bundling
cat << 'JS' > "$MODULE_DIR/static/src/js/dashboard.js"
/** @odoo-module */

import { registry } from "@web/core/registry";
import { Component } from "@owl";

export class ExecutiveDashboard extends Component {
    static template = "airiv_dashboard_indonesia.ExecutiveDashboard";
}

registry.category("actions").add("airiv_dashboard_indonesia.ExecutiveDashboard", ExecutiveDashboard);
JS

# 2. Ensure manifest explicitly references the asset files correctly
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

echo ">>> Upgrading module and clearing asset bundle cache in Odoo <<<"
docker exec -it odoo_app odoo -d OdooAIRIV -u airiv_dashboard_indonesia --stop-after-init --db_host=odoo_db --db_user=odoo --db_password=odoo
docker restart odoo_app
echo ">>> Action registry fix deployed successfully. <<<"
