# Logo por punto de venta (diario)

Cada diario puede llevar su propio logo en el comprobante.

## Problema

Una misma persona jurídica puede operar varias unidades de negocio bajo el mismo CUIT,
separadas por punto de venta. En Argentina lo que distingue a cada unidad no es el CUIT
—que es uno solo— sino el **punto de venta**, que en Odoo vive en el diario de ventas.

Odoo tiene un único logo por compañía (`res.company.logo`), así que todas las unidades
comparten la papelería aunque facturen por puntos de venta distintos.

## Qué hace

Agrega un campo `logo` opcional en `account.journal`. Cuando el diario del comprobante
tiene un logo cargado, el reporte lo usa; si no, cae al logo de la compañía.

El campo nace **vacío**: mientras nadie cargue un logo en ningún diario, ningún reporte
cambia su salida.

## Cómo funciona

El logo se resuelve **una sola vez**, en el despachador `web.external_layout`, antes del
`t-call` al layout concreto. Como en QWeb las variables de `t-set` del llamador son
visibles en el llamado, la variable llega a los siete layouts y a los encabezados de la
localización argentina sin repetir la expresión en cada uno.

Toda la decisión vive en **`_yaguven_logo_unidad()`**, definido sobre `base` — o sea,
disponible en cualquier modelo que llegue a un reporte. Eso evita tener que preguntar si
el método existe y evita que este módulo dependa de `sale`, `stock` y del módulo de
recibos sólo para heredar un método en cada uno.

La cadena es:

| paso | de dónde sale | para qué documentos |
|---|---|---|
| 1 | el **diario** del comprobante, si tiene logo | factura; pedido con diario de facturación elegido; remito, a través del pedido que lo originó |
| 2 | la **unidad del responsable** (`invoice_user_id` → `user_id` → `create_uid`) | presupuesto, remito, recibo |
| 3 | el **logo de la compañía** | todo lo demás, como siempre |

El diario va primero a propósito: ata la papelería al **punto de venta** y no a una
persona, así la factura sale igual la imprima quien la imprima. La unidad del usuario
cubre lo que no tiene diario de ventas.

`create_uid` va último justamente porque lo tienen todos los modelos: es la respuesta
correcta sólo cuando no hay nada mejor — un recibo no tiene vendedor ni diario de ventas,
pero sí quien lo emitió.

### La unidad se lee en la compañía del documento

`yaguven_unidad_id` es `company_dependent`: su valor depende de la compañía activa. Por
eso se lee con `with_company(company_id del documento)`. Sin eso, un documento de una
compañía impreso por alguien que tiene otra como compañía activa leería la unidad
equivocada.

### Por qué una unidad y no un logo en el usuario

Un campo de imagen `company_dependent` no es terreno transitado: en una base 19.0 de
producción no hay **ni un solo** campo binario company_dependent — todos son many2one,
selection o char. La unidad resuelve eso con un many2one, que sí es terreno probado, y de
paso el logo se carga una vez y se asigna a varias personas.

### El encabezado argentino

La factura argentina no pasa por el bloque de logo de los layouts:
`l10n_latam_invoice_document` lo apaga (`t-if="not custom_header"`) y llama a
`l10n_ar.custom_header`, que escribe el logo directo contra `o.company_id.logo`. Por eso
el módulo hereda también ese template.

El remito argentino (`l10n_ar_stock.custom_header`) **no necesita parche propio**: es una
vista `primary` que hereda de `l10n_ar.custom_header`, así que ya arrastra el nuestro.

## Uso

Contabilidad → Configuración → Diarios → el diario → campo **Logo del punto de venta**.

## Verificación

1. Con el campo vacío, imprimir una factura: sale con el logo de la compañía.
2. Cargar un logo en el diario e imprimir de nuevo: sale con el del diario.
3. Imprimir una factura de otro diario: sigue saliendo con el de la compañía.

## Compatibilidad

Odoo 19.0. Cubre los siete layouts nativos (standard, bold, boxed, bubble, folder,
striped y wave) y el encabezado de la localización argentina (`l10n_ar.custom_header`),
que es el que usan las facturas con letra A/B/C.

Depende de `l10n_ar`, así que el módulo apunta a instalaciones con la localización
argentina instalada.
