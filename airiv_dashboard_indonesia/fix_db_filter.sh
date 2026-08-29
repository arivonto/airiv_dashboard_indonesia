#!/bin/bash
echo ">>> Configuring db_filter in Odoo configuration to bypass database selector <<<"

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
db_name = OdooAIRIV
dbfilter = ^OdooAIRIV$
CONF
"

docker restart odoo_app
sleep 3
echo ">>> Database filter applied. Testing response... <<<"
curl -I -H "Host: erp.airiv.id" http://127.0.0.1/web
