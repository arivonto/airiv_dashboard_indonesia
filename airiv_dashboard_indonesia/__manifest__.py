{
    'name': 'Airiv Command Center',
    'version': '18.0.2.0.1',
    'category': 'Extra Tools',
    'summary': 'OWL-based Executive Command Center with Google Gemini AI for Indonesian UMKM',
    'author': 'Riv Cloud Management',
    'license': 'LGPL-3',
    'depends': ['base', 'web', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/dashboard_action.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'airiv_dashboard_indonesia/static/src/xml/command_center.xml',
            'airiv_dashboard_indonesia/static/src/js/command_center.js',
        ],
    },
    'images': ['static/description/banner.png', 'static/description/icon.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
