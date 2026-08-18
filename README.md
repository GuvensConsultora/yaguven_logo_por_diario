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

El logo se resuelve una sola vez en el despachador `web.external_layout`, antes del
`t-call` al layout concreto. Como en QWeb las variables de `t-set` del llamador son
visibles en el llamado, la variable llega a los siete layouts sin repetir la expresión.

Cada layout se modifica con `position="attributes"` sobre su `<img>`, tocando sólo
`t-if` y `t-att-src`. La clase CSS queda intacta, así el logo conserva el tamaño y la
posición que cada formato le da.

La guarda (`o and 'journal_id' in o`) copia el idioma que usa el propio Odoo en
`web.external_layout`: `o` puede no estar definido —al previsualizar el formato del
documento desde Ajustes, por ejemplo— y QWeb lo evalúa como falso.

### El encabezado argentino

La factura argentina **no pasa por ese bloque de logo**. `l10n_latam_invoice_document`
apaga el encabezado nativo (`t-if="not custom_header"`) y llama en su lugar a
`l10n_ar.custom_header`, que arma la cabecera con la letra del comprobante y escribe el
logo directo contra `o.company_id.logo`. Por eso el módulo hereda también ese template:
sin eso, la factura AR sale siempre con el logo de la compañía aunque el diario tenga
uno cargado.

El remito (`l10n_ar_stock.custom_header`) hereda del mismo encabezado, pero ahí `o` es un
`stock.picking` sin `journal_id`: la variable queda en falso y el logo sigue siendo el de
la compañía.

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
