# -*- coding: utf-8 -*-

{
    'name': 'Open academy',
    'version': '1.0.0',
    'category': 'Academy',
    'sequence': -100,
    'summary': 'Open academy system',
    'description': """Open academy system""",
    'depends': [],
    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/templates.xml',
        'views/course.xml',
        'views/session.xml',
        'views/partner.xml'
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
