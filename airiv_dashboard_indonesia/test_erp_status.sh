#!/bin/bash
sleep 3
echo ">>> Testing local routing responses after container recovery <<<"
curl -I -H "Host: erp.airiv.id" http://127.0.0.1/
curl -I -H "Host: erp.airiv.id" http://127.0.0.1/web
echo ">>> Status check complete <<<"
