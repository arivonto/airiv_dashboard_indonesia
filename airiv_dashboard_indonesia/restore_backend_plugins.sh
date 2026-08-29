#!/bin/bash
echo ">>> Restoring lost backend models and views for airiv_dashboard_indonesia <<<"
MODULE_DIR="$HOME/odoo-stack/extra-addons/airiv_dashboard_indonesia"

# 1. Restore root __init__.py
echo "from . import controllers" > "$MODULE_DIR/__init__.py"
if [ -d "$MODULE_DIR/models" ]; then
    echo "from . import models" >> "$MODULE_DIR/__init__.py"
    
    # 2. Dynamically rebuild models/__init__.py based on existing files
    ls -1 "$MODULE_DIR/models"/*.py 2>/dev/null | grep -v '__init__.py' | awk -F/ '{print $NF}' | sed 's/.py$//' | awk '{print "from . import " $1}' > "$MODULE_DIR/models/__init__.py"
    echo ">>> Rebuilt models/__init__.py"
fi

# 3. Dynamically rebuild __manifest__.py using Python
python3 -c "
import os
import ast
import pprint

module_dir = '$MODULE_DIR'
manifest_path = os.path.join(module_dir, '__manifest__.py')

# Read current manifest (which contains our OWL asset fixes)
with open(manifest_path, 'r') as f:
    manifest = ast.literal_eval(f.read())

data_files = []

# Order matters: Load Security first, then Views, then Data
if os.path.exists(os.path.join(module_dir, 'security')):
    for f in sorted(os.listdir(os.path.join(module_dir, 'security'))):
        if f.endswith('.xml') or f.endswith('.csv'):
            data_files.append(f'security/{f}')
            
for folder in ['views', 'data']:
    if os.path.exists(os.path.join(module_dir, folder)):
        for f in sorted(os.listdir(os.path.join(module_dir, folder))):
            if f.endswith('.xml'):
                data_files.append(f'{folder}/{f}')

manifest['data'] = data_files

# Write back to manifest with clean formatting
with open(manifest_path, 'w') as f:
    f.write(pprint.pformat(manifest, sort_dicts=False))
"
echo ">>> Rebuilt __manifest__.py with all views and security rules"

# 4. Upgrade the module to apply the restored files
echo ">>> Upgrading module in Odoo container... <<<"
docker exec -it odoo_app odoo -d OdooAIRIV -u airiv_dashboard_indonesia --stop-after-init --db_host=odoo_db --db_user=odoo --db_password=odoo

docker restart odoo_app
echo ">>> Restoration complete. All backend plugins should now be visible in Odoo! <<<"
