#!/bin/bash
echo ">>> Testing local routing responses for erp.airiv.id paths <<<"
echo "Testing root (/):"
curl -I -H "Host: erp.airiv.id" http://127.0.0.1/
echo -e "\nTesting /web path:"
curl -I -H "Host: erp.airiv.id" http://127.0.0.1/web
echo -e "\nTesting /demo path:"
curl -I -H "Host: erp.airiv.id" http://127.0.0.1/demo
echo -e "\n>>> Routing tests completed <<<"
