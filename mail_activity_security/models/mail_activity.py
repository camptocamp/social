# Copyright 2022 Camptocamp SA (https://www.camptocamp.com).
# @author Iván Todorovich <ivan.todorovich@camptocamp.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, models
from odoo.exceptions import AccessError


class MailActivity(models.Model):
    _inherit = "mail.activity"

    def check_activity_security(self, operation: str) -> bool:
        if self.env.context.get("bypass_activity_security"):
            return True
        if any(not rec._check_activity_security(operation) for rec in self):
            if operation == "edit":
                raise AccessError(_("You are not allowed to edit this activity."))
            if operation == "done":
                raise AccessError(
                    _("You are not allowed to mark this activity as done.")
                )
            if operation == "cancel":
                raise AccessError(_("You are not allowed to cancel this activity."))
            raise AccessError(_("You're not allowed to perform this operation."))
        return True

    def _check_activity_security(self, operation: str) -> bool:
        self.ensure_one()
        if not self.activity_type_id:
            return True
        level = getattr(self.activity_type_id, f"security_{operation}")
        return self._check_activity_security_level(level)

    def _check_activity_security_level(self, level: str) -> bool:
        self.ensure_one()
        user = self.env.user
        if self.env.is_superuser() or self.env.is_admin():
            return True
        if level == "all":
            return True
        if level == "user" and self.user_id == user:
            return True
        if self.create_uid == user:
            return True
        if any(g in user.groups_id for g in self.activity_type_id.security_group_ids):
            return True
        return False

    def activity_format(self):
        res = super().activity_format()
        for item in res:
            rec = self.browse(item["id"])
            item.update(
                {
                    "user_can_mark_as_done": rec._check_activity_security("done"),
                    "user_can_edit": rec._check_activity_security("edit"),
                    "user_can_cancel": rec._check_activity_security("cancel"),
                }
            )
        return res

    def _action_done(self, feedback=False, attachment_ids=None):
        self.check_activity_security("done")
        self = self.with_context(bypass_activity_security=True)
        return super()._action_done(feedback=feedback, attachment_ids=attachment_ids)

    def write(self, vals):
        self.check_activity_security("edit")
        return super().write(vals)

    def unlink(self):
        self.check_activity_security("cancel")
        return super().unlink()
