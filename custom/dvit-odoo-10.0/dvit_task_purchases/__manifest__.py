# -*- coding: utf-8 -*-
{
    'name': "Purchase orders from tasks",
    'summary': "Purchase orders from project tasks",
    'description': """
        Allows user to create purchase orders from tasks and link the PO to the Sale order that generated the task.
    """,
    'author': "DVIT.ME",
    'website': "http://dvit.me",
    'category': 'Project',
    'version': '10.0.1.0',
    'license':'AGPL-3',
    'depends': ['purchase','project'],
    'data': [
        'views/views.xml',
    ],
    'installable': True,

}
