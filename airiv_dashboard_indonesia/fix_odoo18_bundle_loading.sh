#!/bin/bash
echo ">>> Fixing Odoo 18 asset bundle manifest loading for airiv_dashboard_indonesia <<<"

MODULE_DIR="$HOME/odoo-stack/extra-addons/airiv_dashboard_indonesia"

# 1. Update manifest to load assets into 'web.assets_backend' correctly
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

# 2. Ensure dashboard.js uses the exact Odoo 18 module definition and registry syntax
cat << 'JS' > "$MODULE_DIR/static/src/js/dashboard.js"
/** @odoo-module */

import { registry } from "@web/core/registry";
import { Component } from "@owl";

export class ExecutiveDashboard extends Component {
    static template = "airiv_dashboard_indonesia.ExecutiveDashboard";
}

registry.category("actions").add("airiv_dashboard_indonesia.ExecutiveDashboard", ExecutiveDashboard);
JS

# 3. Re-run upgrade and clear ir.attachment assets cache
docker exec -it odoo_app python3 -c "
import odoo
from odoo import api, SUPERUSER_ID
from odoo.modules.registry import Registry
db_name = 'OdooAIRIV'
registry = Registry(db_name)
with registry.cursor() as cr:
    env = api.Environment(cr, SUPERUSER_ID, {})
    env['ir.attachment'].search([('url', 'ilike', '/web/assets/')]).unlink()
    cr.commit()
    print('>>> Cleared asset bundles from ir.attachment cache. <<<')
"

docker exec -it odoo_app odoo -d OdooAIRIV -u airiv_dashboard_indonesia --stop-after-init --db_host=odoo_db --db_user=odoo --db_password=odoo
docker restart odoo_app
echo ">>> Asset bundle registration fixed and Odoo container restarted. <<<"
