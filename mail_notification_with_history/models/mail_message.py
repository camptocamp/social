# Copyright 2022 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import models


class Message(models.Model):
    _inherit = "mail.message"

    def get_notification_message_history(self):
        """Get the list of messages to include into an email notification history."""
        if not self.env[self.model].with_mail_notification_history():
            return []
        if not self._with_notification_message_history():
            return []
        domain = self._get_notification_message_history_domain()
        messages = self.env["mail.message"].search(domain, order="date desc")
        return messages - self

    def _get_notification_message_history_domain(self):
        return [
            ("model", "=", self.model),
            ("res_id", "=", self.res_id),
            ("message_type", "in", ("user_notification", "comment", "email")),
        ]

    def _with_notification_message_history(self):
        """Allow overriding to not include message history."""
        return True
