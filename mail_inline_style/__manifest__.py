# Copyright 2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Mail Inline Style",
    "version": "11.0.1.0.0",
    "category": "Social Network",
    "website": "https://github.com/OCA/social",
    "author": "Camptocamp, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "external_dependencies": {
        "python": [
            'premailer'
        ],
    },
    "depends": [
        "email_template_qweb",
    ],
    "data": [
    ],
    "demo": [
        "demo/demo_template.xml",
        "demo/demo_mail_template.xml",
    ],
}
