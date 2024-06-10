from odoo import models


class RePartner(models.Model):
    _inherit = "res.partner"

    def _get_excluded_partners_domain(self):
        return [
            ("active", "in", (True, False)),
            ("show_in_cc", "=", False),
            ("groups_id", "not in", self.env.ref("base.group_portal").ids),
        ]

    def _get_excluded_partners(self):
        domain = self._get_excluded_partners_domain()
        return self.env["res.users"].search(domain).mapped("partner_id")

    def _has_email_notification(self):
        return not self.user_ids or "email" in self.user_ids.mapped("notification_type")

    def _show_in_cc(self, show_internal_users):
        self.ensure_one()
        if not self.user_ids:
            return True
        excluded_partners = self._get_excluded_partners()
        if show_internal_users:
            return self not in excluded_partners and self.user_ids.mapped("show_in_cc")
        else:
            return self not in excluded_partners and self.user_ids.mapped(
                "groups_id"
            ) not in self.env.ref("base.group_portal")
