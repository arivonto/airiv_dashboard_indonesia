#!/bin/bash
echo ">>> Packaging and Publishing Airiv Command Center to GitHub (8-Core Framework) <<<"

DEV_DIR="$HOME/odoo-stack/extra-addons/airiv_dashboard_indonesia"
STAGING_DIR="$HOME/odoo-app-store/airiv_dashboard_indonesia_repo"
MODULE_FOLDER="airiv_dashboard_indonesia"

# 1. Setup Staging Repository
mkdir -p "$HOME/odoo-app-store"
if [ ! -d "$STAGING_DIR/.git" ]; then
    echo ">>> Cloning repository to isolated staging area... <<<"
    git clone https://github.com/arivonto/airiv_dashboard_indonesia.git "$STAGING_DIR"
fi

cd "$STAGING_DIR" || exit
git fetch --all
git reset --hard origin/main

# 2. Wipe root tracked files to enforce App Store structure (repo_name/module_name/)
echo ">>> Restructuring repository to meet Odoo App Store guidelines... <<<"
git ls-files | xargs git rm -f 2>/dev/null || true

mkdir -p "$MODULE_FOLDER"

# 3. Copy files (Rule 4: Do not move active workspace files)
echo ">>> Copying source files from active workspace... <<<"
rsync -a --exclude='.git' "$DEV_DIR/" "$STAGING_DIR/$MODULE_FOLDER/"

# 4. Dynamic Documentation Sync (Rule 7 & 8)
echo ">>> Auto-syncing README.md from pure light-mode index.html... <<<"
cp "$STAGING_DIR/$MODULE_FOLDER/static/description/index.html" "$STAGING_DIR/README.md"
sed -i '1s/^/<!-- Markdown generated dynamically from pure light-mode HTML specifications -->\n\n/' "$STAGING_DIR/README.md"

# 5. Commit and Push
echo ">>> Committing App Store compliant package... <<<"
git add .
git commit -m "build: App Store compliant structural refactor and automated docs sync"
git push origin main

echo ">>> Publishing complete! Code is live on GitHub and formatted for Odoo App Store submission. <<<"
echo ">>> Active development workspace at $DEV_DIR remains untouched. <<<"
