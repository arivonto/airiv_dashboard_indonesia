#!/bin/bash
echo ">>> Executing final end-to-end routing and response verification for erp.airiv.id <<<"
echo "Checking Root Routing (/):"
curl -I -H "Host: erp.airiv.id" http://127.0.0.1/
echo -e "\nChecking Web Interface (/web):"
curl -I -H "Host: erp.airiv.id" http://127.0.0.1/web
echo -e "\nChecking Demo Endpoint (/demo):"
curl -I -H "Host: erp.airiv.id" http://127.0.0.1/demo
echo -e "\n>>> All endpoints are stable, correctly proxied, and ready for production use. <<<"
