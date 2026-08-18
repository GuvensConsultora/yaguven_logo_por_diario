from odoo import fields, models


class ResUsers(models.Model):
    _inherit = "res.users"

    yaguven_unidad_id = fields.Many2one(
        comodel_name="yaguven.unidad.papeleria",
        string="Unidad de papelería",
        company_dependent=True,
        help="Unidad a la que pertenece este usuario. Los documentos de los que sea "
             "responsable se imprimen con el logo de esta unidad, salvo que el "
             "comprobante tenga un diario con logo propio. Es por compañía: el mismo "
             "usuario puede pertenecer a una unidad distinta en cada una.",
    )
