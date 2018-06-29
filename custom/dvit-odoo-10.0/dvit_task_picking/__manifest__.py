# -*- coding: utf-8 -*-

{
    "name": "Task stock transfers",
    "version": "10.0.1.0.0",
    "category": "Project Management",
    "license": "AGPL-3",
    'summary': 'Allow creating transfers to a task.',
    'description': """
    Create and link transfers to a task.
    """,
    "author": "DVIT.ME",
    "website": "http://dvit.me",
    "depends": ['project',
                'project_stage_closed',
                'project_task_default_stage',
                'dvit_stock_picking_invoice',
                'dvit_stock_analytic'],
    "data": [
             "wizard/wizard.xml",
             "views/templates.xml",
             ],
	 "images": [
        'static/description/banner.png'
    ],
    "installable": True,
}
