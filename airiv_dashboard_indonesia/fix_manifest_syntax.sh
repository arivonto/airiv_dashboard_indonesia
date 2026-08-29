#!/bin/bash
echo ">>> Checking and fixing trailing commas or syntax errors in __manifest__.py files <<<"

find ~/odoo-stack/extra-addons -name "__manifest__.py" | while read -r manifest; do
    echo "Inspecting: $manifest"
    python3 -c "
import ast
try:
    with open('$manifest', 'r') as f:
        ast.literal_eval(f.read())
    print('   [OK] Syntax valid.')
except Exception as e:
    print(f'   [ERROR] Syntax invalid: {e}')
"
done

echo ">>> Manifest verification script completed <<<"
