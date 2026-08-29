#!/bin/bash
echo ">>> Verifying complete domain routing for erp.airiv.id/web and /demo <<<"
curl -I -H "Host: erp.airiv.id" http://127.0.0.1/web
curl -I -H "Host: erp.airiv.id" http://127.0.0.1/demo
echo ">>> Verification complete <<<"
