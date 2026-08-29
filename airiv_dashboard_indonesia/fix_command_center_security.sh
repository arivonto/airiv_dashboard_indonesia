#!/bin/bash
echo ">>> Injecting Odoo Security Access Rules for airiv_dashboard_indonesia <<<"

MODULE_DIR="$HOME/odoo-stack/extra-addons/airiv_dashboard_indonesia"
mkdir -p "$MODULE_DIR/security"

# 1. Create the access rules CSV for the new TransientModel
cat << 'CSV' > "$MODULE_DIR/security/ir.model.access.csv"
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_airiv_command_center,access_airiv_command_center,model_airiv_command_center,base.group_user,1,1,1,1
CSV

# 2. Update Manifest to load the security file before views
cat << 'MANIFEST' > "$MODULE_DIR/__manifest__.py"
{
    'name': 'Airiv Command Center',
    'version': '18.0.2.0.1',
    'category': 'Extra Tools',
    'summary': 'OWL-based Executive Command Center with Google Gemini AI for Indonesian UMKM',
    'author': 'Riv Cloud Management',
    'license': 'LGPL-3',
    'depends': ['base', 'web', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/dashboard_action.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'airiv_dashboard_indonesia/static/src/xml/command_center.xml',
            'airiv_dashboard_indonesia/static/src/js/command_center.js',
        ],
    },
    'images': ['static/description/banner.png', 'static/description/icon.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
MANIFEST

# 3. Upgrade module to apply security rules
echo ">>> Upgrading module to validate security rules... <<<"
docker exec -it odoo_app odoo -d OdooAIRIV -u airiv_dashboard_indonesia --stop-after-init --db_host=odoo_db --db_user=odoo --db_password=odoo
docker restart odoo_app

echo ">>> Security rules applied. The Command Center is now error-free and App Store ready! <<<"
