# -*- coding: utf-8 -*-

{
    'name': 'Open academy',
    'version': '1.0.0',
    'category': 'Academy',
    'sequence': -100,
    'summary': 'Open academy system',
    'description': """Open academy system""",
    'depends': ['board'],
    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/templates.xml',
        'views/course.xml',
        'views/session.xml',
        'reports/sessions_report_templates.xml',
        'reports/sessions_report.xml',
        'wizard/reg_participants_to_sessions_wizard.xml',
        'views/partner.xml',
        'views/session_board.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
    'author': 'Sheremet Oleg',
}
