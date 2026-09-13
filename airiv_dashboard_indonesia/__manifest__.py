{
    'name': 'Airiv Command Center',
    'version': '18.0.2.1.0',
    'category': 'Extra Tools',
    'summary': 'OWL-based Executive Command Center for Indonesian business telemetry and portfolio operations',
    'description': """
AIRIV Command Center provides an executive-grade Odoo cockpit for Indonesian business operations.
It brings operational signals, portfolio readiness, business telemetry, and guided navigation into
a focused OWL-based command surface designed for Odoo 18.
""",
    'author': 'AIRIV',
    'website': 'https://airiv.id',
    'license': 'LGPL-3',
    'price': 0.0,
    'currency': 'EUR',
    'depends': ['base', 'web', 'mail', 'airiv_os_core'],
    'data': [
        'security/ir.model.access.csv',
        'views/dashboard_action.xml',
    ],
    'assets': {
        'web.assets_backend': [
            '/web/static/lib/Chart/Chart.js',
            'airiv_dashboard_indonesia/static/src/xml/command_center.xml',
            'airiv_dashboard_indonesia/static/src/js/command_center.js',
            'airiv_dashboard_indonesia/static/src/scss/command_center.scss',
        ],
    },
    'images': ['static/description/banner.png', 'static/description/icon.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
