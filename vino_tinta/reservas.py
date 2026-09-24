import frappe
from frappe.utils import cint


def validar_cupo_evento(doc, method=None):
    if not doc.evento:
        return

    personas = cint(doc.numero_personas)

    if personas <= 0:
        frappe.throw("El número de personas debe ser mayor a 0.")

    # Bloqueamos temporalmente el evento durante la validación.
    # Esto evita que dos reservas simultáneas se pasen del cupo.
    evento = frappe.db.sql(
        """
        SELECT cupo_maximo
        FROM `tabEvento Vino Tinta`
        WHERE name = %s
        FOR UPDATE
        """,
        (doc.evento,),
        as_dict=True,
    )

    if not evento:
        frappe.throw("El evento seleccionado no existe.")

    cupo_maximo = cint(evento[0].cupo_maximo)

    # Cuenta todas las reservas confirmadas excepto la reserva
    # que se está editando actualmente.
    ocupados = frappe.db.sql(
        """
        SELECT COALESCE(SUM(numero_personas), 0)
        FROM `tabReserva de Evento`
        WHERE evento = %s
          AND estado = 'Confirmada'
          AND name != %s
        """,
        (doc.evento, doc.name or ""),
    )[0][0]

    ocupados = cint(ocupados)

    # Solo las reservas confirmadas consumen cupo.
    if doc.estado == "Confirmada":
        total_nuevo = ocupados + personas
    else:
        total_nuevo = ocupados

    disponibles = max(cupo_maximo - ocupados, 0)

    if total_nuevo > cupo_maximo:
        frappe.throw(
            f"No hay suficientes cupos disponibles para este evento.<br><br>"
            f"<b>Cupo máximo:</b> {cupo_maximo}<br>"
            f"<b>Cupos ocupados:</b> {ocupados}<br>"
            f"<b>Cupos disponibles:</b> {disponibles}<br>"
            f"<b>Personas solicitadas:</b> {personas}"
        )


def recalcular_cupos_evento(evento):
    if not evento:
        return

    ocupados = frappe.db.sql(
        """
        SELECT COALESCE(SUM(numero_personas), 0)
        FROM `tabReserva de Evento`
        WHERE evento = %s
          AND estado = 'Confirmada'
        """,
        (evento,),
    )[0][0]

    frappe.db.set_value(
        "Evento Vino Tinta",
        evento,
        "cupos_ocupados",
        cint(ocupados),
        update_modified=False,
    )


def actualizar_cupos_evento(doc, method=None):
    eventos = set()

    if doc.evento:
        eventos.add(doc.evento)

    # Si editaron una reserva y la movieron a otro evento,
    # también actualizamos el evento anterior.
    anterior = doc.get_doc_before_save()

    if anterior and anterior.evento:
        eventos.add(anterior.evento)

    for evento in eventos:
        recalcular_cupos_evento(evento)


def actualizar_cupos_al_eliminar(doc, method=None):
    if doc.evento:
        recalcular_cupos_evento(doc.evento)
