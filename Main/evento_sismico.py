class OrigenDeGeneracion:
    def __init__(self, descripcion: str, nombre: str) -> None:
        self.descripcion = descripcion
        self.nombre = nombre

    def getNombre(self) -> str:
        return self.nombre


class MagnitudRichter:
    def __init__(self, descripcionMagnitud: str, numero: float) -> None:
        self.descripcionMagnitud = descripcionMagnitud
        self.numero = numero
        

class AlcanceSismo:
    def __init__(self, descripcion: str, nombre: str) -> None:
        self.descripcion = descripcion
        self.nombre = nombre
    
    def getNombre(self) -> str:
        return self.nombre  


class Estado:
    def __init__(self, ambito: str, nombreEstado: str) -> None:
        self.ambito: str = ambito
        self.nombreEstado: str = nombreEstado


class EventoSismico:
    def __init__(self, id: int, fechaHoraFin, fechaHoraOcurrencia, latitudEpicentro: float, longitudEpicentro: float,
                 latitudHipocentro: float, longitudHipocentro: float, magnitud: MagnitudRichter, origenGeneracion: OrigenDeGeneracion, alcanceSismo: AlcanceSismo, estadoActual: Estado) -> None:
        self.id = id
        self.fechaHoraFin = fechaHoraFin
        self.fechaHoraOcurrencia = fechaHoraOcurrencia
        self.latitudEpicentro = latitudEpicentro
        self.longitudEpicentro = longitudEpicentro
        self.latitudHipocentro = latitudHipocentro
        self.longitudHipocentro = longitudHipocentro
        self.magnitud = magnitud
        self.origenGeneracion = origenGeneracion
        self.alcanceSismo = alcanceSismo
        self.estadoActual = estadoActual

    def as_dict(self):
        return {
            'id': self.id,
            'fechaHoraFin': self.fechaHoraFin.strftime('%Y-%m-%d %H:%M:%S') if hasattr(self.fechaHoraFin, 'strftime') else self.fechaHoraFin,
            'fechaHoraOcurrencia': self.fechaHoraOcurrencia.strftime('%Y-%m-%d %H:%M:%S') if hasattr(self.fechaHoraOcurrencia, 'strftime') else self.fechaHoraOcurrencia,
            'latitudEpicentro': self.latitudEpicentro,
            'longitudEpicentro': self.longitudEpicentro,
            'latitudHipocentro': self.latitudHipocentro,
            'longitudHipocentro': self.longitudHipocentro,
            'magnitud': self.magnitud.numero if hasattr(self.magnitud, 'numero') else self.magnitud,
            'origenGeneracion': self.origenGeneracion.getNombre() if hasattr(self.origenGeneracion, 'getNombre') else self.origenGeneracion,
            'alcanceSismo': self.alcanceSismo.getNombre(),
            'estadoActual': self.estadoActual.nombreEstado
        }

