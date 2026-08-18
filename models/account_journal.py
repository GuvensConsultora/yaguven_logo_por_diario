from odoo import fields, models


class AccountJournal(models.Model):
    _inherit = "account.journal"

    logo = fields.Image(
        string="Logo del punto de venta",
        max_width=1024,
        max_height=1024,
        help="Logo que se imprime en los comprobantes de este diario. "
             "Si se deja vacío, el comprobante usa el logo de la compañía.",
    )
