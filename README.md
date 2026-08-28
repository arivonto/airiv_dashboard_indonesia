# AIRIV Dashboard Indonesia

![License](https://img.shields.io/badge/License-LGPL--3-blue)
![Odoo](https://img.shields.io/badge/Odoo-18.0%20Community-purple)
![Price](https://img.shields.io/badge/Price-%240.00%20(Free)-brightgreen)
![Bundle](https://img.shields.io/badge/Bundle-7--in--1%20Indonesian%20Suite-red)

## Detailed Feature Capabilities
- **Regulatory Articles**: Statutory PPN 11% effective rate calculations and DPP Nilai Lain compliance.
- **Technical Scope**: 100% Native Odoo Community Architecture ensuring Zero External Server Overhead.
- **API Rails**: Native hooks for WhatsApp Business API (Fonnte/Waha) and logistics aggregators (Biteship, RajaOngkir, Shipper).

## Installation & Odoo Configuration Guide
1. Clone or extract the `airiv_dashboard_indonesia` directory into your Odoo custom addons path.
2. Restart your Odoo container to refresh the system (`docker restart odoo_app`).
3. Activate **Developer Mode**, update the Apps List, and install **AIRIV Dashboard Indonesia**.
4. Configure default IDR currency and domestic payment rails (Midtrans, Xendit) via standard settings.

## Validated Commercial Test Use Case
- **Benchmark Scenario**: Automated ORM integration suite executing inside the active container (`odoo shell`) to verify complete multi-branch revenue aggregation and effective PPN separation.

## Module Specifications Table
| Specification | Value |
| :--- | :--- |
| **Version** | 18.0.1.0.0 |
| **License** | LGPL-3 |
| **Dependencies** | `base`, `account`, `sale`, `stock`, `hr` |
| **Framework Compatibility**| Odoo 18.0 Community |
| **Pricing** | $0.00 (Free) |
