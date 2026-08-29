#!/bin/bash
echo ">>> Forcing clean pull from GitHub for airiv_dashboard_indonesia <<<"
MODULE_DIR="$HOME/odoo-stack/extra-addons/airiv_dashboard_indonesia"

cd "$MODULE_DIR" || { echo "Module directory not found!"; exit 1; }

# Get the current active branch (usually main or master)
BRANCH=$(git rev-parse --abbrev-ref HEAD)
echo ">>> Current branch detected: $BRANCH <<<"

# Fetch the absolute latest history from GitHub
git fetch --all

# Force the local directory to perfectly match the GitHub repository
echo ">>> Wiping local broken files and resetting to origin/$BRANCH... <<<"
git reset --hard "origin/$BRANCH"

# Pull to ensure everything is synced
git pull origin "$BRANCH"

echo ">>> Code restored! Upgrading module in Odoo to rebuild the database links... <<<"
docker exec -it odoo_app odoo -d OdooAIRIV -u airiv_dashboard_indonesia --stop-after-init --db_host=odoo_db --db_user=odoo --db_password=odoo

echo ">>> Restarting Odoo container... <<<"
docker restart odoo_app

echo ">>> Pull and upgrade complete. Your plugins should now be restored! <<<"
