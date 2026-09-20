import frappe


@frappe.whitelist(allow_guest=True)
def rastrear_pieza(codigo=None):
    codigo = (codigo or "").strip()

    if not codigo:
        return {
            "encontrada": False,
            "mensaje": "Ingresa un código de pieza."
        }

    # Primero intenta buscar por el ID del documento: PZ-00008
    pieza = frappe.db.get_value(
        "Pieza Vino Tinta",
        codigo,
        [
            "name",
            "tipopieza",
            "tipo_de_proceso",
            "estado",
            "date"
        ],
        as_dict=True
    )

    # Si no lo encuentra, intenta con el campo Código de pieza
    if not pieza:
        pieza = frappe.db.get_value(
            "Pieza Vino Tinta",
            {"codigopieza": codigo},
            [
                "name",
                "tipopieza",
                "tipo_de_proceso",
                "estado",
                "date"
            ],
            as_dict=True
        )

    if not pieza:
        return {
            "encontrada": False,
            "mensaje": "No encontramos una pieza con ese código."
        }

    return {
        "encontrada": True,
        "codigo": pieza.name,
        "tipo_pieza": pieza.tipopieza,
        "tipo_proceso": pieza.tipo_de_proceso,
        "estado": pieza.estado,
        "fecha_estimada": str(pieza.date) if pieza.date else None
    }
