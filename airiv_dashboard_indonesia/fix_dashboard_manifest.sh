#!/bin/bash
echo ">>> Fixing airiv_dashboard_indonesia manifest syntax <<<"

MANIFEST_PATH="$HOME/odoo-stack/extra-addons/airiv_dashboard_indonesia/__manifest__.py"

cat << 'MANIFEST' > "$MANIFEST_PATH"
{
    'name': 'Airiv Executive Dashboard Indonesia',
    'version': '18.0.1.0.0',
    'category': 'Extra Tools',
    'summary': 'Executive command center built natively with Odoo 18 OWL framework for Indonesian UMKM',
    'description': 'A high-performance executive command center built natively with Odoo 18 OWL framework, tailored specifically for Indonesian SMEs, local enterprises, and UMKM governance.',
    'author': 'Riv Cloud Management',
    'license': 'LGPL-3',
    'depends': ['base', 'web', 'mail'],
    'data': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
MANIFEST

echo ">>> Restarting odoo_app container to apply fix <<<"
docker restart odoo_app
echo ">>> Done <<<"
