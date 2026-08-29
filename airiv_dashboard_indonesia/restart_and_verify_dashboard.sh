#!/bin/bash
echo ">>> Restarting Odoo container to apply updated assets and client actions <<<"
docker restart odoo_app
sleep 3
echo ">>> Verifying accessibility of erp.airiv.id/web <<<"
curl -I -H "Host: erp.airiv.id" http://127.0.0.1/web
echo ">>> Done <<<"
