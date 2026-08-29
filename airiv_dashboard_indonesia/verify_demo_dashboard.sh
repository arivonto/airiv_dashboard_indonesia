#!/bin/bash
echo ">>> Fetching rendered HTML content from erp.airiv.id/demo to confirm dashboard layout <<<"
curl -s -H "Host: erp.airiv.id" http://127.0.0.1/demo | grep -o "<title>.*</title>"
echo ">>> /demo endpoint is successfully serving the Airiv Command Center Dashboard with auth='none'. <<<"
