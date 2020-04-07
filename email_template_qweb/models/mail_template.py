# Copyright 2016 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, tools, models
from odoo.addons.mail.models.mail_template import (
    format_amount, format_date, format_tz
)


class MailTemplate(models.Model):
    _inherit = 'mail.template'

    body_type = fields.Selection(
        [('jinja2', 'Jinja2'), ('qweb', 'QWeb')], 'Body templating engine',
        default='jinja2', required=True)
    body_view_id = fields.Many2one(
        'ir.ui.view', 'Body view', domain=[('type', '=', 'qweb')])
    body_view_arch = fields.Text(related='body_view_id.arch')

    @api.multi
    def generate_email(self, res_ids, fields=None):
        multi_mode = True
        if isinstance(res_ids, int):
            res_ids = [res_ids]
            multi_mode = False
        result = super(MailTemplate, self).generate_email(
            res_ids, fields=fields
        )
        for res_id, template in self.get_email_template(res_ids).items():
            if template.body_type == 'qweb' and\
                    (not fields or 'body_html' in fields):
                for record in self.env[template.model].browse(res_id):
                    body_html = template.body_view_id.render(
                        template._qweb_render_context(record)
                    )
                    # Some wizards, like when sending a sales order, need this
                    # fix to display accents correctly
                    body_html = tools.ustr(body_html)
                    result[res_id]['body_html'] = self.render_post_process(
                        body_html
                    )
                    result[res_id]['body'] = tools.html_sanitize(
                        result[res_id]['body_html']
                    )
        return multi_mode and result or result[res_ids[0]]

    def _qweb_render_context(self, record):
        res = {}
        if record._name == 'mail.message':
            partner_model = self.env['res.partner']
            # these variables are usually loaded when the notification is sent
            # but there are some key values that that are nice to have
            # if you want to pre-render your template in preview mode.
            # This is particularly useful if you use the template
            # from the mail composer, whereas the rendering is done on load.
            # Also, you don't need to access them from `ctx`.
            res = partner_model._notify_prepare_template_context(record)
        res.update({
            'object': record,
            'email_template': self,
            # Same as for Jinja rendering,
            # taken from `mail_template.render_template`.
            # These ease porting of old Jinja templates to qweb ones.
            'format_date':
                lambda date, format=False,
                context=self._context: format_date(self.env, date, format),
            'format_tz':
                lambda dt, tz=False, format=False,
                context=self._context: format_tz(self.env, dt, tz, format),
            'format_amount':
                lambda amount, currency,
                context=self._context: format_amount(
                    self.env, amount, currency),
            'user': self.env.user,
            # keep it for Jinja template compatibility
            'ctx': self.env.context,
        })
        return res
