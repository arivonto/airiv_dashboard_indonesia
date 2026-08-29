#!/bin/bash
echo ">>> Restoring airiv_dashboard_indonesia from GitHub <<<"
MODULE_DIR="$HOME/odoo-stack/extra-addons/airiv_dashboard_indonesia"

cd "$MODULE_DIR" || { echo "Module directory not found!"; exit 1; }

# Check if the folder is currently a Git repository
if [ -d .git ]; then
    echo ">>> Git repository detected. Securing current state... <<<"
    
    # Stash our recent OWL asset fixes so we can re-apply them later if needed
    git stash -m "Stashing OWL asset fixes before GitHub restore"
    
    # Identify current branch and pull the latest code
    BRANCH=$(git rev-parse --abbrev-ref HEAD)
    echo ">>> Pulling latest code from origin/$BRANCH... <<<"
    git pull origin "$BRANCH"
    
    echo ">>> Code restored. Upgrading Odoo module to rebuild UI links... <<<"
    docker exec -it odoo_app odoo -d OdooAIRIV -u airiv_dashboard_indonesia --stop-after-init --db_host=odoo_db --db_user=odoo --db_password=odoo
    
    docker restart odoo_app
    echo ">>> Restoration complete. Log into Odoo to verify your plugins are back! <<<"
else
    echo ">>> ERROR: This directory is not currently tracked by Git (.git folder missing)."
    echo ">>> If your repository is cloned elsewhere, clone it directly into $HOME/odoo-stack/extra-addons/"
fi
