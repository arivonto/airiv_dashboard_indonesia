import os
from PIL import Image, ImageDraw

module_dir = os.path.expanduser("~/odoo-stack/extra-addons/airiv_dashboard_indonesia")
desc_dir = os.path.join(module_dir, "static", "description")
os.makedirs(desc_dir, exist_ok=True)

icon_size = (128, 128)
icon_img = Image.new("RGBA", icon_size, (15, 23, 42, 255))
draw_icon = ImageDraw.Draw(icon_img)
draw_icon.rounded_rectangle([16, 16, 112, 112], radius=24, fill=(30, 41, 59, 255), outline=(56, 189, 248, 255), width=3)
draw_icon.text((36, 48), "AIRIV", fill=(255, 255, 255, 255))
icon_path = os.path.join(desc_dir, "icon.png")
icon_img.save(icon_path, "PNG")

banner_size = (1200, 630)
banner_img = Image.new("RGB", banner_size, color=(15, 23, 42))
draw_banner = ImageDraw.Draw(banner_img)
draw_banner.rectangle([80, 80, 1120, 550], fill=(30, 41, 59), outline=(56, 189, 248), width=2)
draw_banner.text((120, 120), "AIRIV EXECUTIVE DASHBOARD INDONESIA", fill=(255, 255, 255))
draw_banner.text((120, 170), "Odoo 18 Native OWL Command Center for Indonesian UMKM", fill=(148, 163, 184))
banner_path = os.path.join(desc_dir, "banner.png")
banner_img.save(banner_path, "PNG")

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Airiv Executive Dashboard Indonesia</title>
    <style>
        body { background-color: #f8fafc; color: #0f172a; font-family: system-ui, -apple-system, sans-serif; line-height: 1.6; padding: 40px; }
        .container { max-width: 900px; margin: auto; background: #ffffff; padding: 40px; border-radius: 12px; border: 1px solid #cbd5e1; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); }
        h1 { color: #0f172a; font-size: 2.25rem; border-bottom: 2px solid #e2e8f0; padding-bottom: 15px; margin-top: 0; }
        h2 { color: #334155; margin-top: 30px; font-size: 1.5rem; }
        p, li { color: #334155; font-size: 1rem; }
        .badge { display: inline-block; background: #e2e8f0; color: #0f172a; padding: 4px 12px; border-radius: 6px; font-weight: 600; font-size: 0.875rem; margin-bottom: 20px; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th, td { border: 1px solid #cbd5e1; padding: 12px; text-align: left; background: #ffffff; color: #334155; }
        th { background: #f1f5f9; font-weight: 600; }
    </style>
</head>
<body>
    <div class="container">
        <span class="badge">Odoo 18 Community Compatible | LGPL-3</span>
        <h1>Executive Dashboard Indonesia</h1>
        <p>A high-performance executive command center built natively with Odoo 18 OWL framework, tailored specifically for Indonesian SMEs, local enterprises, and UMKM governance.</p>
        
        <h2>Key Capabilities</h2>
        <ul>
            <li><strong>Real-time KPI Tracking:</strong> Instant visibility into sales metrics, cash flow, inventory thresholds, and tax compliance data.</li>
            <li><strong>100% Native OWL Architecture:</strong> Zero external middleware, server overhead, or third-party webhooks. Operates entirely inside standard Odoo boundaries.</li>
            <li><strong>Localized Formatting:</strong> Built-in IDR currency formatting (Rp), WIB timezone indicators, and streamlined Indonesian business layouts.</li>
        </ul>

        <h2>Module Specifications</h2>
        <table>
            <tr><th>Technical Name</th><td>airiv_dashboard_indonesia</td></tr>
            <tr><th>Odoo Version</th><td>18.0</td></tr>
            <tr><th>License</th><td>LGPL-3 (Free and Open Source)</td></tr>
            <tr><th>Framework</th><td>OWL and Python ORM</td></tr>
        </table>
    </div>
</body>
</html>
"""

index_path = os.path.join(desc_dir, "index.html")
with open(index_path, "w") as f:
    f.write(html_content)

readme_content = """# Airiv Executive Dashboard Indonesia (airiv_dashboard_indonesia)

An executive command center designed natively for Odoo 18, tailored for Indonesian SMEs and UMKM operations.

## Detailed Feature Capabilities
* Interactive KPI Workspace: Real-time visualizations powered by the Odoo OWL framework.
* Zero External Dependencies: Operates 100% natively within standard Odoo boundaries ($0.00 infrastructure overhead).
* Indonesian Regional Standards: Localized currency formatting (IDR) and operational metrics.

## Installation and Odoo Configuration Guide
1. Place airiv_dashboard_indonesia in your Odoo extra-addons directory.
2. Update your Odoo instance modules list or run the upgrade command via terminal.
3. Navigate to your Odoo dashboard workspace to access the executive command view.

## Module Specifications Table
| Parameter | Specification |
| :--- | :--- |
| Version | 18.0.1.0.0 |
| License | LGPL-3 |
| Dependencies | base, web, mail |
| Framework Compatibility | Odoo 18 Community |
"""

readme_path = os.path.join(module_dir, "README.md")
with open(readme_path, "w") as f:
    f.write(readme_content)

print("All store assets and documentation generated successfully.")
