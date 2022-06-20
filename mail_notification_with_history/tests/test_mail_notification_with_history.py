# Copyright 2022 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from unittest.mock import Mock, patch

from odoo.tests import common


class TestMailNotificationWithHistory(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.base_template = cls.env.ref("mail.message_notification_email")
        cls.mail_message = cls.env.ref("mail.mail_message_channel_1_2_1")
        cls.message_subtype = cls.env.ref("mail.mt_comment")
        cls.render_values = {
            "button_access": {"title": "View Record", "url": "http://127.0.0.1"},
            "actions": [],
            "company": cls.env.company,
            "has_button_access": True,
            "is_discussion": True,
            "lang": "en_US",
            "message": cls.mail_message,
            "subtype": cls.message_subtype,
        }

    def test_thread_history_is_included(self):
        with patch(
            (
                "odoo.addons.mail_notification_with_history.models.mail_thread."
                "MailThread._mail_notification_include_history"
            ),
            new=Mock(return_value=True),
        ):
            body = self.base_template._render(
                self.render_values, engine="ir.qweb", minimal_qcontext=True
            )
        self.assertTrue(body.find(b"Discussion") >= 0)

    def test_thread_history_is_not_included(self):
        body = self.base_template._render(
            self.render_values, engine="ir.qweb", minimal_qcontext=True
        )
        self.assertTrue(body.find(b"Discussion") == -1)
