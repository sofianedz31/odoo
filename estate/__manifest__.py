{
    'name': 'estate',
    'depends': ['base','web'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_menus.xml',
        'views/res_users_views.xml',
        'data/data.xml',
        'report/estate_property_templates.xml', 
        'report/estate_property_reports.xml',

    ],
    'demo': [
        'demo/demo_data.xml',
    ],
    'application': True,
}
