{
    "name": "Logo por punto de venta (diario)",
    "summary": "Papelería propia por punto de venta y por unidad de negocio",
    "description": """
Papelería por unidad de negocio
===============================

Una misma persona jurídica puede operar varias unidades bajo el mismo CUIT: una casa
central y una casa de repuestos, por ejemplo. Odoo tiene un solo logo por compañía, así
que todas las unidades comparten la papelería.

Este módulo resuelve el logo de cada documento con una cadena de tres pasos:

1. **El diario del comprobante**, si tiene logo propio. Ata la papelería al punto de
   venta: la factura sale igual la imprima quien la imprima.
2. **La unidad del responsable del documento** — el vendedor del pedido, el del remito,
   quien emitió el recibo. Cubre todo lo que no tiene diario de ventas.
3. **El logo de la compañía**, como siempre.

Todo vacío = ningún reporte cambia.
""",
    "author": "Yagüven C.G.",
    "website": "https://yaguven.com",
    "category": "Accounting/Accounting",
    "version": "19.0.2.0.0",
    "license": "LGPL-3",
    "depends": ["account", "web", "l10n_ar"],
    "data": [
        "security/ir.model.access.csv",
        "views/yaguven_unidad_papeleria_views.xml",
        "views/account_journal_views.xml",
        "views/res_users_views.xml",
        "views/report_layout.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
}
