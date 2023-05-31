# Copyright 2023 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)


def migrate(cr, version):
    cr.execute(
        """ALTER TABLE ONLY mailing_contact_list_rel ALTER COLUMN active SET DEFAULT TRUE;"""
    )
