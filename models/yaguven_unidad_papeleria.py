from odoo import fields, models


class YaguvenUnidadPapeleria(models.Model):
    _name = "yaguven.unidad.papeleria"
    _description = "Unidad de papelería"
    _order = "name"

    name = fields.Char(
        string="Nombre",
        required=True,
        help="Cómo se llama la unidad puertas adentro: Casa Central, Casa de "
             "Repuestos, Sucursal Italia. No se imprime: sirve para elegirla.",
    )
    logo = fields.Image(
        string="Logo",
        max_width=1024,
        max_height=1024,
        help="Logo que se imprime en los comprobantes de esta unidad.",
    )
    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Compañía",
        required=True,
        default=lambda self: self.env.company,
    )
    active = fields.Boolean(string="Activo", default=True)
