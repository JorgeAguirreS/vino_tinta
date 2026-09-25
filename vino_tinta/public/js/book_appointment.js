(() => {
	const TIMEZONE = "America/Tegucigalpa";

	// Solo aplicar en la página nativa de reservas
	if (!window.location.pathname.startsWith("/book_appointment")) {
		return;
	}

	function fijar_zona_horaria() {
		const selector = document.getElementById("appointment-timezone");

		if (!selector) {
			return;
		}

		// Si ERPNext volvió a cargar todas las zonas, las quitamos.
		if (
			selector.options.length !== 1 ||
			selector.options[0]?.value !== TIMEZONE
		) {
			selector.innerHTML = "";

			const opcion = document.createElement("option");
			opcion.value = TIMEZONE;
			opcion.textContent = "Tegucigalpa (GMT-6)";
			opcion.selected = true;

			selector.appendChild(opcion);
		}

		selector.value = TIMEZONE;

		// El usuario puede verlo, pero no cambiarlo.
		selector.disabled = true;
	}

	function iniciar() {
		const selector = document.getElementById("appointment-timezone");

		if (!selector) {
			setTimeout(iniciar, 100);
			return;
		}

		fijar_zona_horaria();

		// ERPNext llena este select dinámicamente.
		// Si intenta agregar nuevamente todas las zonas,
		// lo dejamos otra vez únicamente en Tegucigalpa.
		const observer = new MutationObserver(() => {
			fijar_zona_horaria();
		});

		observer.observe(selector, {
			childList: true,
		});

		// Un par de verificaciones extra por la inicialización async de ERPNext.
		setTimeout(fijar_zona_horaria, 250);
		setTimeout(fijar_zona_horaria, 1000);
	}

	if (document.readyState === "loading") {
		document.addEventListener("DOMContentLoaded", iniciar);
	} else {
		iniciar();
	}
})();
