# Copyright 2024 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    image_embedding_method = fields.Selection(
        selection=[
            ("none", "No attachment"),
            ("cid", "CIDs attachment"),
            ("data", "Data SRC"),
        ],
        default="cid",  # previous module version only supported CID
        required=True,
    )
