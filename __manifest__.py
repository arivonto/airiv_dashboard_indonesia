# -*- coding: utf-8 -*-
{
    'name': 'AIRIV Executive Command Center (Indonesia Edition)',
    'version': '18.0.1.0.0',
    'category': 'Sales/Management',
    'summary': 'Native Owl 2 Executive Dashboard with Bank Indonesia JISDOR Forex, Real-time Sales Velocity, Inventory Reorder Alerts & Tri-Gateway Telemetry',
    'description': """
AIRIV Executive Command Center (Indonesia Edition)
===================================================
A high-performance, native Owl 2 analytical cockpit engineered for Odoo 18 Community.
Built for Indonesian enterprises, SMBs, and UMKMs with zero external proxy overhead.
    """,
    'author': 'Riv Cloud Management',
    'website': 'https://airiv.id',
    'license': 'LGPL-3',
    'price': 0.0,
    'currency': 'EUR',
    'depends': [
        'base',
        'sale_management',
        'account',
        'stock',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/dashboard_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'airiv_dashboard_indonesia/static/src/scss/dashboard.scss',
            'airiv_dashboard_indonesia/static/src/js/dashboard_plugin.js',
            'airiv_dashboard_indonesia/static/src/xml/dashboard_template.xml',
        ],
    },
    'images': [
        'static/description/banner.png',
        'static/description/icon.png',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
