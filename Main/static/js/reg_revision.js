let evento = null;
let accionSeleccionada = null;

const selectAccion = document.getElementById('accion');

accionSeleccionada = selectAccion.value;

selectAccion.addEventListener('change', function () {
  accionSeleccionada = this.value;
  console.log('Acción seleccionada:', accionSeleccionada);
});


const modalElement = document.getElementById('confirmacionModal');
const bootstrapModal = new bootstrap.Modal(modalElement);


function abrirModal() {
  bootstrapModal.show();
}


function cerrarModal() {
  bootstrapModal.hide();
}


document.getElementById('btnSi').addEventListener('click', function () {
  cerrarModal();
  console.log('Se presionó SÍ');
});


document.getElementById('btnNo').addEventListener('click', function () {
  cerrarModal();
  console.log('Se presionó NO');
});


function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}


function tomarModificacionDatos(id_evento, enviarDatos = false, magnitud = null, origen = null, alcance = null) {
  const url = new URL(window.location.href);
  /*
  EL MENSAJE tomarModificacionDatos y tomarOpcionAccion se envian juntos en este fetch
  */
  if (enviarDatos) {
    body_to_send = {
      action: 'save',
      actionToDo: selectAccion.value,
      id_evento: id_evento,
      alcance: alcance,
      origen: origen,
      magnitud: magnitud
    }
  }

  else {
    body_to_send = {
      id_evento: id_evento,
      actionToDo: selectAccion.value,
      action: 'dontSave'
    }
  }

  fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken')
    },
    body: JSON.stringify(body_to_send)
  })
    .then(response => {
      if (!response.ok) throw new Error('Error en la solicitud');
      return response.json();
    })
    .then(data => {
      console.log(data);
    })
    .catch(error => {
      console.error(error);
    });
}


const boton_enviar_datos = document.getElementById('tomarModificacionDatos');


boton_enviar_datos.addEventListener('click', async function (e) {
  e.preventDefault();

  const confirmar = await abrirModalConfirmacion();

  if (!confirmar) {
    console.log("El usuario canceló la modificación.");
    tomarModificacionDatos(evento.id);
    return;
  }

  tomarModificacionDatos(
    evento.id,
    enviarDatos = true,
    document.getElementById('magnitudVista').value,
    document.getElementById('origenVista').value,
    document.getElementById('alcanceVista').value
  );
});


function abrirModalConfirmacion() {
  return new Promise((resolve) => {
    const modalElement = document.getElementById('confirmacionModal');
    const modal = new bootstrap.Modal(modalElement);

    const btnSi = document.getElementById('btnSi');
    const btnNo = document.getElementById('btnNo');

    const limpiarListeners = () => {
      btnSi.removeEventListener('click', onYes);
      btnNo.removeEventListener('click', onNo);
    };

    const onYes = () => {
      limpiarListeners();
      modal.hide();
      resolve(true);
    };

    const onNo = () => {
      limpiarListeners();
      modal.hide();
      resolve(false);
    };

    btnSi.addEventListener('click', onYes);
    btnNo.addEventListener('click', onNo);

    modal.show();
  });
}


function rellenarDatosAdicionales(data) {
  document.getElementById('clasificacion').value = data.datosEvenSis.clasificacionEventoSis.nombre;
  document.getElementById('kmProfundidadDesde').value = data.datosEvenSis.clasificacionEventoSis.kmProfundidadDesde;
  document.getElementById('kmProfundidadHasta').value = data.datosEvenSis.clasificacionEventoSis.kmProfundidadHasta;

  document.getElementById('origenVista').value = `${data.datosEvenSis.origenGeneracionEventoSis.nombre} - ${data.datosEvenSis.origenGeneracionEventoSis.descripcion}`;
  document.getElementById('alcanceVista').value = `${data.datosEvenSis.alcanceEventoSis.nombre} - ${data.datosEvenSis.alcanceEventoSis.descripcion}`;

  let serieTemporal = data.serieTemp;

  document.getElementById('nombreEstacion').value = serieTemporal[0].nombreEstacion;

  const sismo_container = document.getElementById('containerSeries');
  sismo_container.innerHTML = '';

  for (let j = 0; j < serieTemporal.length; j++) {
    const serie = serieTemporal[j];
    let muestras = serie.muestra;

    let y = document.createElement('div');
    y.innerHTML = `<div class="mb-2">
      <h4>Serie temporal ${j + 1} - ${serie.nombreEstacion}</h4>
    </div>`;

    for (let index = 0; index < muestras.length; index++) {
      const muestra = muestras[index];

      const x = document.createElement('div');
      x.innerHTML = `
        <div class="mb-2">
          <label class="form-label">${muestra.tipoDeDato.denominacion}</label>
          <input type="text" disabled class="form-control" value="${muestra.valor} ${muestra.tipoDeDato.nombreUnidadMedida}">
        </div>
      `;

      y.appendChild(x);
    }

    sismo_container.appendChild(y);
  }
}


function ofrecerModificarEvento() {
  document.getElementById('alcanceVista').disabled = false
  document.getElementById('origenVista').disabled = false
  document.getElementById('magnitudVista').disabled = false
}


function tomarConfirmacionVisualizacion() {
  const url = new URL(window.location.href);
  url.searchParams.set('action', 'tomar_confirmacion_visualizacion');

  fetch(url, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json'
    }
  })
    .then(response => {
      if (!response.ok) throw new Error('Error en la solicitud');
      return response.json();
    })
    .then(data => {
      if (data.success) {
        if (data.action === 'ofrecerModificarEvento') {
          ofrecerModificarEvento()
        }
      }
    })
    .catch(error => {
      console.error(error);
    });
}


function tomarSelEventoSis(idSeleccionado) {
  const url = new URL(window.location.href);
  url.searchParams.set('action', 'tomar_sel_evento_sismico');
  url.searchParams.set('id_evento', idSeleccionado)

  fetch(url, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json'
    }
  })
    .then(response => {
      if (!response.ok) throw new Error('Error en la solicitud');
      return response.json();
    })
    .then(data => {
      console.log(data);
      rellenarDatosAdicionales(data)
      boton_ver_mapa = document.getElementById('visualizarMapa')
      boton_ver_mapa.disabled = false
      boton_ver_mapa.addEventListener('click', tomarConfirmacionVisualizacion())

    })
    .catch(error => {
      console.error(error);
    });
}


function getEventosSismicos() {
  const url = new URL(window.location.href);
  url.searchParams.set('action', 'get_eventos_sismicos');

  fetch(url, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json'
    }
  })
    .then(response => {
      if (!response.ok) throw new Error('Error en la solicitud');
      return response.json();
    })
    .then(data => {
      eventosSismicos = data;

      const select = document.getElementById('eventoSelect');
      select.innerHTML = '<option selected disabled>Seleccione un evento detectado</option>';

      data.forEach(evento => {
        const option = document.createElement('option');
        option.value = evento.id;
        option.textContent = `${evento.fechaHoraOcurrencia} - M${evento.magnitud}`;
        select.appendChild(option);
      });
    })
    .catch(error => {
      console.error('Error al obtener eventos sísmicos:', error);
    });
}


function vaciarFormulario() {
  document.getElementById('fecha').value = "";
  document.getElementById('hora').value = "";
  document.getElementById('magnitudVista').value = "";
  document.getElementById('alcanceVista').value = "";
  document.getElementById('origenVista').value = "";
  document.getElementById('coordenadas').value = "";
  document.getElementById('magnitud').value = "";
  document.getElementById('alcance').value = "";
  document.getElementById('origen').value = "";
}


function eventoSeleccionadoChange() {
  const select = document.getElementById('eventoSelect');
  const idSeleccionado = select.value;
  tomarSelEventoSis(idSeleccionado)

  vaciarFormulario();

  if (!idSeleccionado) {
    console.log('No se seleccionó ningún evento.');
    return;
  }

  evento = eventosSismicos.find(e => e.id.toString() === idSeleccionado);
  if (evento) {

    const fechaHoraOcurrencia = evento.fechaHoraOcurrencia || "";
    if (fechaHoraOcurrencia.includes(" ")) {
      const [fecha, hora] = fechaHoraOcurrencia.split(" ");
      document.getElementById('fecha').value = fecha;
      document.getElementById('hora').value = hora.substring(0, 5);
    } else {
      document.getElementById('fecha').value = fechaHoraOcurrencia;
      document.getElementById('hora').value = "";
    }

    document.getElementById('magnitudVista').value = evento.magnitud || "";


    if (evento.latitudEpicentro != null && evento.longitudEpicentro != null) {
      document.getElementById('coordenadas').value = `${evento.latitudEpicentro}, ${evento.longitudEpicentro}`;
    } else {
      document.getElementById('coordenadas').value = "";
    }

  } else {
    console.warn('Evento no encontrado para el id:', idSeleccionado);
  }
}


document.addEventListener('DOMContentLoaded', () => {
  getEventosSismicos();

  const select = document.getElementById('eventoSelect');
  if (select) {
    select.addEventListener('change', eventoSeleccionadoChange);
  }
});