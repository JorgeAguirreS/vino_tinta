def asignar_codigo_pieza(doc, method=None):
    if doc.name and doc.codigopieza != doc.name:
        doc.db_set(
            "codigopieza",
            doc.name,
            update_modified=False
        )
