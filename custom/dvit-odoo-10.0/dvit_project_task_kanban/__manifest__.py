
{
    'name': 'Project Task - Kanban Improvement',
    'category': 'Project',
    'summary': 'Project task kanban view improvement',
    'website': 'https://dvit.me/',
    'version': '10.0.1.0.0',
    'license': 'AGPL-3',
    'description': '''
        - Customer's name added in the Kanban box.
        - Added planned hours, remaining hours, progress and Progress Guage widget
        ''',

    'author': 'DVIT.ME',
    'depends': [
        'hr_timesheet',
    ],
    'data': [
        'views/project_task_view.xml',
    ],
    'installable': True,
    'auto_install': True,
}
