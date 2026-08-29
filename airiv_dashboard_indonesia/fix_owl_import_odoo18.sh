#!/bin/bash
echo ">>> Fixing OWL module import syntax for Odoo 18 in dashboard.js <<<"

MODULE_DIR="$HOME/odoo-stack/extra-addons/airiv_dashboard_indonesia"

# 1. Update JS to use `@odoo/owl` instead of `@owl` (Crucial for Odoo 17/18)
cat << 'JS' > "$MODULE_DIR/static/src/js/dashboard.js"
/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component } from "@odoo/owl";

export class ExecutiveDashboard extends Component {
    static template = "airiv_dashboard_indonesia.ExecutiveDashboard";
}

registry.category("actions").add("airiv_dashboard_indonesia.ExecutiveDashboard", ExecutiveDashboard);
JS

# 2. Make sure Manifest specifically orders XML before JS in assets array
cat << 'MANIFEST' > "$MODULE_DIR/__manifest__.py"
{
    'name': 'Airiv Executive Dashboard Indonesia',
    'version': '18.0.1.0.0',
    'category': 'Extra Tools',
    'summary': 'Executive command center built natively with Odoo 18 OWL framework for Indonesian UMKM',
    'author': 'Riv Cloud Management',
    'license': 'LGPL-3',
    'depends': ['base', 'web', 'mail'],
    'data': [
        'views/dashboard_action.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'airiv_dashboard_indonesia/static/src/xml/dashboard.xml',
            'airiv_dashboard_indonesia/static/src/js/dashboard.js',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
}
MANIFEST

echo ">>> Purging asset attachment cache directly in DB to force fresh bundle generation <<<"
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
"

echo ">>> Upgrading module to register new asset sequence <<<"
docker exec -it odoo_app odoo -d OdooAIRIV -u airiv_dashboard_indonesia --stop-after-init --db_host=odoo_db --db_user=odoo --db_password=odoo

echo ">>> Restarting Odoo to clear runtime memory <<<"
docker restart odoo_app
echo ">>> @odoo/owl fix applied and container restarted <<<"
