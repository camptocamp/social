# Copyright 2022 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import models


class MicrosoftOutlookMixin(models.AbstractModel):
    _inherit = "microsoft.outlook.mixin"

    @property
    def _OUTLOOK_ENDPOINT(self):
        tenant_id = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("microsoft_outlook_tenant_id")
        )
        outlook_endpoint = "https://login.microsoftonline.com/common/oauth2/v2.0/"
        if tenant_id:
            outlook_endpoint = outlook_endpoint.replace("common", tenant_id)
        return outlook_endpoint
