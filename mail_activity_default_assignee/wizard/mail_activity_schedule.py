# Copyright 2024 Camptocamp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class MailActivitySchedule(models.TransientModel):
    _inherit = "mail.activity.schedule"

    @api.depends("activity_type_id")
    def _compute_activity_user_id(self):
        res = super()._compute_activity_user_id()
        for scheduler in self.filtered(
            lambda rec: not rec.activity_type_id.default_user_id
            and rec.activity_type_id.default_user_field_id
        ):
            fname = scheduler.activity_type_id.default_user_field_id.name
            res_model = self.env[scheduler.res_model]
            user_ids = scheduler._get_user_ids(res_model, fname)
            if not user_ids:
                continue
            scheduler.activity_user_id = user_ids.ids[0]
        return res

    def _get_user_ids(self, model, fname):
        context = self.env.context
        active_id = context.get("active_id")
        res_id = model.browse(active_id)
        user_ids = getattr(res_id, fname)
        return user_ids
