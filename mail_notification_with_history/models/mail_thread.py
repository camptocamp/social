# Copyright 2022 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import api, models


class MailThread(models.AbstractModel):
    _inherit = "mail.thread"

    _mail_notification_include_history = False

    @api.model
    def with_mail_notification_history(self):
        return self._mail_notification_include_history
