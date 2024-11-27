# Copyright 2024 Camptocamp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models

MAGIC_FIELDS = models.MAGIC_COLUMNS


class MailActivityType(models.Model):
    _inherit = "mail.activity.type"

    model_id = fields.Many2one("ir.model", compute="_compute_model_id")

    default_user_field_id = fields.Many2one(
        "ir.model.fields",
        domain=f"""
            [
                ("name", "not in", {str(MAGIC_FIELDS)}),
                ("ttype", "in", ["one2many","many2one", "many2many"]),
                ("model_id", "=", model_id),
                ("relation", "=", "res.users")
            ]
        """,
        help="Default assignee is set based on this field",
    )

    @api.depends("res_model")
    def _compute_model_id(self):
        for rec in self:
            if not rec.res_model:
                rec.model_id = False
                continue
            rec.model_id = self.env["ir.model"]._get_id(rec.res_model)

    @api.onchange("res_model")
    def _onchange_res_model(self):
        res = super()._onchange_res_model()
        self.default_user_field_id = self.default_user_field_id.filtered(
            lambda field: field.model_id.model == self.res_model
        )
        return res
