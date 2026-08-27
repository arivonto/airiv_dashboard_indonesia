# AIRIV Dashboard Indonesia for Odoo 18.0

Comprehensive analytics and regional operational intelligence tailored specifically for Indonesian enterprises (UMKM and SMBs), providing real-time financial tracking, tax compliance oversight, and localized logistics monitoring natively within Odoo Community.

## Detailed Feature Capabilities

- **Indonesian Regulatory & Financial Alignment**: Complete oversight designed around Indonesian statutory compliance, supporting local tax standards (PPN 11% effective calculations with DPP Nilai Lain, NPWP/NIK validation) and localized multi-gate payment tracking (Midtrans, Xendit, and PayPal).
- **Logistics Integration Hub**: Unified monitoring for domestic shipping aggregators (Biteship, RajaOngkir, Shipper) covering primary couriers (JNE, J&T, SiCepat, GoSend) directly inside sales and inventory workflows.
- **WhatsApp Notification Metrics**: Operational dashboards tracking automated customer messaging metrics via WhatsApp Business API (Fonnte/Waha) for delivery updates, OTPs, and invoices.
- **Executive Analytics & KPI Cards**: Real-time sales velocity, revenue breakdowns in IDR (Rp), and stock turnover metrics built on pure Odoo ORM models without external middleware overhead.

## Installation & Odoo Configuration Guide

1. Clone or copy the airiv_dashboard_indonesia module directory into your Odoo custom addons path.
2. Restart your Odoo container to refresh module lists:
   docker restart odoo_app
3. Navigate to your Odoo instance, activate **Developer Mode**, go to **Apps**, update the app list, and click **Activate** on **AIRIV Dashboard Indonesia**.

## Module Specifications Table

| Specification | Value |
| :--- | :--- |
| **Module Name** | airiv_dashboard_indonesia |
| **Compatibility** | 18.0 Community |
| **License** | LGPL-3 |
| **Dependencies** | base, account, sale, stock |
