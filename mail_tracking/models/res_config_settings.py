from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    mail_tracking_show_aliases = fields.Boolean(
        related="company_id.mail_tracking_show_aliases",
        readonly=False,
    )
    enable_mail_tracking_email_deletion_job = fields.Boolean(
        "Enable deletion of old mail tracking records",
        config_parameter="mail_tracking.enable_mail_tracking_email_deletion_job",
        help="Enables the job to delete old mail tracking records to reduce "
        "the database size. This sets an ir.config.parameter "
        "mail_tracking.enable_mail_tracking_email_deletion_job",
    )
