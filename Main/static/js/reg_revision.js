function rellenarDatosAdicionales(data){
  
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
      <h4>Serie temporal ${j+1} - ${serie.nombreEstacion}</h4>
    </div>`;

    for (let index = 0; index < muestras.length; index++) {
      const muestra = muestras[index];

      const x = document.createElement('div');
      x.innerHTML = `
        <div class="mb-2">
          <label class="form-label">${muestra.tipoDeDato.denominacion}</label>
          <input type="text" class="form-control" value="${muestra.valor} ${muestra.tipoDeDato.nombreUnidadMedida}">
        </div>
      `;

      y.appendChild(x);
    }

    sismo_container.appendChild(y);
  }
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
        option.textContent = `${evento.fechaHoraOcurrencia} - ${evento.origenGeneracion.nombre} - ${evento.origenGeneracion.descripcion} - M${evento.magnitud}`;
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

  const evento = eventosSismicos.find(e => e.id.toString() === idSeleccionado);
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