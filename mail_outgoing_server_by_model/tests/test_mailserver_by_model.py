# Copyright 2023 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo_test_helper import FakeModelLoader

from odoo.tests.common import Form, TransactionCase


class TestMailserverByModel(TransactionCase):
    at_install = False
    post_install = True

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.setUpClassModels()
        cls.setUpClassMailserver()
        cls.setUpClassMail()

    @classmethod
    def tearDownClass(cls):
        cls.loader.restore_registry()
        return super().tearDownClass()

    @classmethod
    def setUpClassModels(cls):
        cls.loader = FakeModelLoader(cls.env, cls.__module__)
        cls.loader.backup_registry()
        from .models import ModelWithMail

        cls.loader.update_registry((ModelWithMail,))
        dest_partner = cls.env["res.partner"].create(
            {"name": "René Coty", "email": "rene.coty@gouv.fr"}
        )
        cls.record_with_mail = cls.env[ModelWithMail._name].create(
            {"partner_id": dest_partner.id}
        )
        cls.model_with_mail_model = cls.env["ir.model"].search(
            [("model", "=", ModelWithMail._name)]
        )

    @classmethod
    def setUpClassMailserver(cls):
        default_vals = {
            "smtp_host": "localhost",
            "smtp_port": "25",
            "smtp_user": "georges.abitbol@localhost",
            "smtp_pass": "1 4m v3ry 53cur3",
            "smtp_authentication": "login",
            "smtp_encryption": "none",
        }
        mailserver_model = cls.env["ir.mail_server"]
        default_mailserver_vals = dict(
            default_vals,
            **{
                "name": "default",
                "smtp_user": "default@localhost",
                "sequence": 10,
            }
        )
        cls.default_mailserver = mailserver_model.create(default_mailserver_vals)
        secondary_mailserver_vals = dict(
            default_vals,
            **{
                "name": "secondary",
                "smtp_user": "secondary@localhost",
                "sequence": 42,
            }
        )
        cls.secondary_mailserver = mailserver_model.create(secondary_mailserver_vals)

    @classmethod
    def setUpClassMail(cls):
        cls.mail_template = cls.env["mail.template"].create(
            {
                "model_id": cls.model_with_mail_model.id,
                "name": "Model with Mail: Send by Mail",
                "subject": "Model with Mail: {{object.partner_id.name}}",
                "partner_to": "{{object.partner_id.id}}",
                "body_html": "Hello, this is a mail",
            }
        )

    def _write_message_on_record(self, record):
        composer = Form(
            self.env["mail.compose.message"].with_context(
                default_model=record._name,
                default_res_id=record.id,
                default_use_template=True,
                default_template_id=self.mail_template.id,
                default_composition_mode="comment",
            )
        )
        composer.save().action_send_mail()
        return record.message_ids[0]

    def test_mail_server(self):
        # By default, message.mail_server_id is False
        message = self._write_message_on_record(self.record_with_mail)
        self.assertFalse(message.mail_server_id)
        # But if we set outgoing_mailserver_id on the model, secondary_mailserver
        # is forced.
        self.model_with_mail_model.write(
            {"outgoing_mailserver_id": self.secondary_mailserver.id}
        )
        message = self._write_message_on_record(self.record_with_mail)
        self.assertEqual(message.mail_server_id, self.secondary_mailserver)
