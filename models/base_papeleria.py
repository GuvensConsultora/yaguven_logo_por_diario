from odoo import models

# Orden en que se busca al responsable de un documento. El primero que exista en el
# modelo y tenga valor gana; `create_uid` va último porque lo tienen todos los
# modelos y es la respuesta correcta sólo cuando no hay nada mejor (el recibo, por
# ejemplo, no tiene vendedor ni diario de ventas: tiene quien lo emitió).
_CAMPOS_RESPONSABLE = ("invoice_user_id", "user_id", "create_uid")


class Base(models.AbstractModel):
    _inherit = "base"

    def _yaguven_logo_unidad(self):
        """Devuelve el logo con el que debe imprimirse este documento, o False.

        Se define sobre `base` a propósito: el `t-set` del layout corre para
        cualquier modelo que llegue a un reporte, y así no hace falta preguntar si
        el método existe ni heredar uno por uno los modelos de cada aplicación —
        que además obligaría a este módulo a depender de `sale`, `stock` y del
        módulo de recibos.

        La cadena es: diario del comprobante → unidad del responsable → nada
        (y ahí el layout cae al logo de la compañía, como siempre).

        Ante cualquier duda devuelve False. Este método corre en TODOS los PDF de
        la base: si levantara una excepción, dejaría de imprimirse cualquier
        documento de cualquier compañía.
        """
        if not self or len(self) != 1:
            return False
        registro = self.sudo()

        diario = registro._yaguven_diario_papeleria()
        if diario and diario.logo:
            return diario.logo

        unidad = registro._yaguven_unidad_papeleria()
        if unidad and unidad.logo:
            return unidad.logo

        return False

    def _yaguven_diario_papeleria(self):
        """El diario del que sale la papelería del documento, si hay alguno.

        Directo si el documento tiene `journal_id` (factura, pedido de venta con
        diario de facturación elegido); a través del pedido si es un remito, que no
        tiene diario propio pero sí el pedido que lo originó.
        """
        registro = self.sudo()
        diario = registro._fields.get("journal_id") and registro.journal_id
        if diario and diario._name == "account.journal":
            return diario
        pedido = registro._fields.get("sale_id") and registro.sale_id
        if pedido and "journal_id" in pedido._fields and pedido.journal_id:
            return pedido.journal_id
        return False

    def _yaguven_unidad_papeleria(self):
        """La unidad del responsable del documento, leída en SU compañía.

        El `with_company` no es un detalle: `yaguven_unidad_id` es
        `company_dependent`, así que su valor depende de la compañía activa. Sin
        esto, un documento de Arauco impreso por alguien que tiene Camiletti como
        compañía activa leería la unidad equivocada.
        """
        registro = self.sudo()
        compania = registro._fields.get("company_id") and registro.company_id
        if not compania or compania._name != "res.company":
            compania = self.env.company

        for campo in _CAMPOS_RESPONSABLE:
            if campo not in registro._fields:
                continue
            responsable = registro[campo]
            if not responsable or responsable._name != "res.users":
                continue
            return responsable.with_company(compania).yaguven_unidad_id
        return False
