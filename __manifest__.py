{
    "name": "Logo por punto de venta (diario)",
    "summary": "Cada diario de venta puede llevar su propio logo en el comprobante",
    "description": """
Logo por punto de venta
=======================

Una misma persona jurídica puede operar varias unidades de negocio bajo el mismo
CUIT, separadas por punto de venta. Odoo tiene un solo logo por compañía, así que
todas las unidades comparten la papelería.

Este módulo agrega un logo opcional en el diario. Cuando el diario del comprobante
tiene uno cargado, el reporte lo usa; si no, cae al logo de la compañía y el
comportamiento es exactamente el de siempre.

El campo nace vacío: mientras nadie cargue un logo en ningún diario, ningún
reporte cambia.
""",
    "author": "Yagüven C.G.",
    "website": "https://yaguven.com",
    "category": "Accounting/Accounting",
    "version": "19.0.1.0.0",
    "license": "LGPL-3",
    "depends": ["account", "web"],
    "data": [
        "views/account_journal_views.xml",
        "views/report_layout.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
}
