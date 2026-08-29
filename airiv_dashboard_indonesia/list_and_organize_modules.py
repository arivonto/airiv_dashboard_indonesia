import os
import shutil
import subprocess

print(">>> Scanning and Organizing Odoo Custom Modules <<<")

# Standard local development addons path based on standard layout
target_addons_dir = os.path.expanduser("~/odoo-stack/extra-addons")
os.makedirs(target_addons_dir, exist_ok=True)

# Scan current workspace or common locations for module folders (containing __manifest__.py)
discovered_modules = []
search_roots = [os.getcwd(), target_addons_dir, os.path.expanduser("~/Downloads")]

for root_dir in search_roots:
    if os.path.exists(root_dir):
        for item in os.listdir(root_dir):
            item_path = os.path.join(root_dir, item)
            if os.path.isdir(item_path):
                manifest_path = os.path.join(item_path, "__manifest__.py")
                if os.path.exists(manifest_path):
                    discovered_modules.append((item, item_path))

print(f"\nDiscovered Custom Modules ({len(discovered_modules)} found):")
for name, path in discovered_modules:
    print(f" - {name} [Location: {path}]")
    
    # Ensure every discovered custom module is properly placed in extra-addons
    destination = os.path.join(target_addons_dir, name)
    if path != destination:
        if os.path.exists(destination):
            print(f"   -> Destination {destination} already exists. Skipping move.")
        else:
            print(f"   -> Moving to proper directory: {destination}")
            shutil.copytree(path, destination)

print(f"\n>>> All valid Odoo custom modules are synchronized to: {target_addons_dir} <<<")
