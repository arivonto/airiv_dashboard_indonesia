#!/bin/bash
echo ">>> Inspecting Odoo Container Error Logs <<<"
docker logs odoo_app --tail 50
