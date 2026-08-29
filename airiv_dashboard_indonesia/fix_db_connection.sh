#!/bin/bash
echo ">>> Fixing Odoo Database Connection parameters for odoo_app container <<<"

CONTAINER_CONF="/etc/odoo/odoo.conf"

docker exec -it odoo_app bash -c "cat << 'CONF' > $CONTAINER_CONF
[options]
addons_path = /mnt/extra-addons,/usr/lib/python3/dist-packages/odoo/addons
data_dir = /var/lib/odoo
admin_passwd = admin
db_host = odoo_db
db_port = 5432
db_user = odoo
db_password = odoo
CONF
"

echo ">>> Upgrading airiv_dashboard_indonesia module with correct db_host <<<"
docker exec -it odoo_app odoo -d OdooAIRIV -u airiv_dashboard_indonesia --stop-after-init --db_host=odoo_db --db_user=odoo --db_password=odoo
docker restart odoo_app
echo ">>> Database connection and module upgrade completed <<<"
