"""
Universidad Nacional Abierta y a Distancia - UNAD
Escuela de Ciencias Básicas, Tecnología e Ingeniería - ECBTI
Curso: Programación
Código: 213023

Fase 4 - Prácticas simuladas

Proyecto:
Sistema Integral de Gestión de Clientes, Servicios y Reservas - Software FJ

Descripción general:
Aplicación desarrollada en Python bajo el paradigma de programación orientada a objetos.
El sistema permite gestionar clientes, servicios y reservas para la empresa Software FJ,
sin utilizar bases de datos. Toda la información se administra mediante objetos y listas
internas, mientras que los eventos relevantes y errores se registran en un archivo de logs.

El proyecto implementa:
- Clases abstractas.
- Herencia.
- Polimorfismo.
- Encapsulación.
- Métodos sobrescritos.
- Simulación de sobrecarga mediante parámetros opcionales.
- Validaciones estrictas.
- Excepciones personalizadas.
- Bloques try/except.
- Bloques try/except/else.
- Bloques try/except/finally.
- Encadenamiento de excepciones.
- Archivo de logs.
- Simulación de operaciones válidas e inválidas.
"""

from abc import ABC, abstractmethod
from datetime import datetime
import logging
import re
import uuid


# ============================================================
# CONFIGURACIÓN GENERAL DEL SISTEMA DE LOGS
# ============================================================

logging.basicConfig(
    filename="eventos_sistema.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    encoding="utf-8"
)


# ============================================================
# EXCEPCIONES PERSONALIZADAS
# ============================================================

class SistemaFJError(Exception):
    """Excepción base del sistema Software FJ."""
    pass


class DatoInvalidoError(SistemaFJError):
    """Se lanza cuando un dato ingresado no cumple las reglas de validación."""
    pass


class ServicioNoDisponibleError(SistemaFJError):
    """Se lanza cuando se intenta usar un servicio que no está disponible."""
    pass


class ReservaInvalidaError(SistemaFJError):
    """Se lanza cuando una reserva no puede crearse, confirmarse, cancelarse o procesarse."""
    pass


class CostoInvalidoError(SistemaFJError):
    """Se lanza cuando existe un problema relacionado con el cálculo de costos."""
    pass


class OperacionNoPermitidaError(SistemaFJError):
    """Se lanza cuando una operación no se puede ejecutar por el estado actual del objeto."""
    pass


class ClienteDuplicadoError(SistemaFJError):
    """Se lanza cuando se intenta registrar un cliente con un documento ya existente."""
    pass


# ============================================================
# CLASE ABSTRACTA GENERAL DEL SISTEMA
# ============================================================

class EntidadSistema(ABC):
    """
    Clase abstracta general para representar cualquier entidad del sistema.

    Cada entidad posee:
    - Identificador único.
    - Fecha de creación.
    - Método abstracto descripcion().
    """

    def __init__(self):
        self._id = str(uuid.uuid4())[:8]
        self._fecha_creacion = datetime.now()

    @property
    def id(self):
        return self._id

    @property
    def fecha_creacion(self):
        return self._fecha_creacion

    @abstractmethod
    def descripcion(self):
        """Método abstracto que debe ser implementado por las clases hijas."""
        pass


# ============================================================
# CLASE CLIENTE
# ============================================================

class Cliente(EntidadSistema):
    """
    Representa un cliente de la empresa Software FJ.

    Aplica encapsulación porque los atributos principales son privados
    y solo se modifican mediante propiedades con validaciones.
    """

    def __init__(self, nombre, documento, correo, telefono):
        super().__init__()

        self._nombre = None
        self._documento = None
        self._correo = None
        self._telefono = None

        self.nombre = nombre
        self.documento = documento
        self.correo = correo
        self.telefono = telefono

        logging.info(
            f"Cliente creado correctamente | ID: {self.id} | "
            f"Nombre: {self.nombre} | Documento: {self.documento}"
        )

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        if not isinstance(valor, str):
            raise DatoInvalidoError("El nombre del cliente debe ser una cadena de texto.")

        valor = valor.strip()

        if len(valor) < 3:
            raise DatoInvalidoError("El nombre del cliente debe tener mínimo 3 caracteres.")

        if any(caracter.isdigit() for caracter in valor):
            raise DatoInvalidoError("El nombre del cliente no debe contener números.")

        self._nombre = valor.title()

    @property
    def documento(self):
        return self._documento

    @documento.setter
    def documento(self, valor):
        valor = str(valor).strip()

        if not valor.isdigit():
            raise DatoInvalidoError("El documento debe contener únicamente números.")

        if len(valor) < 6:
            raise DatoInvalidoError("El documento debe tener mínimo 6 dígitos.")

        self._documento = valor

    @property
    def correo(self):
        return self._correo

    @correo.setter
    def correo(self, valor):
        if not isinstance(valor, str):
            raise DatoInvalidoError("El correo debe ser una cadena de texto.")

        valor = valor.strip().lower()
        patron_correo = r"^[\w\.-]+@[\w\.-]+\.\w+$"

        if not re.match(patron_correo, valor):
            raise DatoInvalidoError("El correo electrónico no tiene un formato válido.")

        self._correo = valor

    @property
    def telefono(self):
        return self._telefono

    @telefono.setter
    def telefono(self, valor):
        valor = str(valor).strip()

        if not valor.isdigit():
            raise DatoInvalidoError("El teléfono debe contener únicamente números.")

        if len(valor) < 7:
            raise DatoInvalidoError("El teléfono debe tener mínimo 7 dígitos.")

        self._telefono = valor

    def descripcion(self):
        return (
            f"Cliente ID: {self.id} | "
            f"Nombre: {self.nombre} | "
            f"Documento: {self.documento} | "
            f"Correo: {self.correo} | "
            f"Teléfono: {self.telefono}"
        )

    def __str__(self):
        return self.descripcion()


# ============================================================
# CLASE ABSTRACTA SERVICIO
# ============================================================

class Servicio(EntidadSistema):
    """
    Clase abstracta para representar los servicios ofrecidos por Software FJ.

    Las clases hijas deben implementar:
    - validar_parametros()
    - calcular_costo()
    - descripcion()
    """

    def __init__(self, nombre, costo_base, disponible=True):
        super().__init__()

        self._nombre = None
        self._costo_base = None
        self._disponible = None

        self.nombre = nombre
        self.costo_base = costo_base
        self.disponible = disponible

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        if not isinstance(valor, str):
            raise DatoInvalidoError("El nombre del servicio debe ser texto.")

        valor = valor.strip()

        if len(valor) < 4:
            raise DatoInvalidoError("El nombre del servicio debe tener mínimo 4 caracteres.")

        self._nombre = valor.title()

    @property
    def costo_base(self):
        return self._costo_base

    @costo_base.setter
    def costo_base(self, valor):
        try:
            valor = float(valor)

            if valor <= 0:
                raise ValueError("El costo base debe ser mayor que cero.")

            self._costo_base = valor

        except ValueError as error_original:
            raise CostoInvalidoError(
                "No fue posible asignar el costo base del servicio."
            ) from error_original

    @property
    def disponible(self):
        return self._disponible

    @disponible.setter
    def disponible(self, valor):
        if not isinstance(valor, bool):
            raise DatoInvalidoError("La disponibilidad del servicio debe ser True o False.")

        self._disponible = valor

    def cambiar_disponibilidad(self, estado):
        """Permite habilitar o deshabilitar un servicio."""

        if not isinstance(estado, bool):
            raise DatoInvalidoError("El estado de disponibilidad debe ser True o False.")

        self._disponible = estado

        if estado:
            logging.info(f"Servicio habilitado | ID: {self.id} | Nombre: {self.nombre}")
        else:
            logging.warning(f"Servicio deshabilitado | ID: {self.id} | Nombre: {self.nombre}")

    def verificar_disponibilidad(self):
        """Verifica si el servicio está disponible antes de realizar una reserva."""

        if not self.disponible:
            raise ServicioNoDisponibleError(
                f"El servicio '{self.nombre}' no está disponible actualmente."
            )

    @abstractmethod
    def validar_parametros(self, duracion_horas):
        pass

    @abstractmethod
    def calcular_costo(self, duracion_horas):
        pass

    @abstractmethod
    def descripcion(self):
        pass

    def calcular_costo_con_opciones(self, duracion_horas, impuesto=0.19, descuento=0.0):
        """
        Simulación de sobrecarga de métodos mediante parámetros opcionales.

        Casos posibles:
        - calcular_costo_con_opciones(duracion)
        - calcular_costo_con_opciones(duracion, impuesto=0.19)
        - calcular_costo_con_opciones(duracion, impuesto=0.19, descuento=0.10)
        """

        try:
            duracion_horas = float(duracion_horas)
            impuesto = float(impuesto)
            descuento = float(descuento)

            if duracion_horas <= 0:
                raise ValueError("La duración debe ser mayor que cero.")

            if impuesto < 0:
                raise ValueError("El impuesto no puede ser negativo.")

            if descuento < 0 or descuento > 1:
                raise ValueError("El descuento debe estar entre 0 y 1.")

            subtotal = self.calcular_costo(duracion_horas)
            valor_descuento = subtotal * descuento
            base_con_descuento = subtotal - valor_descuento
            valor_impuesto = base_con_descuento * impuesto
            total = base_con_descuento + valor_impuesto

            if total <= 0:
                raise ValueError("El costo total calculado no puede ser menor o igual a cero.")

            return round(total, 2)

        except SistemaFJError:
            raise

        except Exception as error_original:
            raise CostoInvalidoError(
                "Error al calcular el costo total del servicio."
            ) from error_original


# ============================================================
# SERVICIO ESPECIALIZADO 1: RESERVA DE SALA
# ============================================================

class ReservaSala(Servicio):
    """Servicio especializado para reserva de salas."""

    def __init__(self, nombre, costo_base, capacidad, incluye_video_beam=True, disponible=True):
        super().__init__(nombre, costo_base, disponible)

        self.capacidad = capacidad
        self.incluye_video_beam = incluye_video_beam

        self._validar_configuracion()

        logging.info(
            f"Servicio creado | Tipo: ReservaSala | ID: {self.id} | Nombre: {self.nombre}"
        )

    def _validar_configuracion(self):
        if not isinstance(self.capacidad, int):
            raise DatoInvalidoError("La capacidad de la sala debe ser un número entero.")

        if self.capacidad <= 0:
            raise DatoInvalidoError("La capacidad de la sala debe ser mayor que cero.")

        if not isinstance(self.incluye_video_beam, bool):
            raise DatoInvalidoError("El valor de video beam debe ser True o False.")

    def validar_parametros(self, duracion_horas):
        try:
            duracion_horas = float(duracion_horas)

            if duracion_horas <= 0:
                raise ValueError("La duración debe ser mayor que cero.")

            if duracion_horas > 8:
                raise ValueError("Una sala no puede reservarse por más de 8 horas continuas.")

        except ValueError as error_original:
            raise ReservaInvalidaError(
                "Parámetros inválidos para reservar una sala."
            ) from error_original

    def calcular_costo(self, duracion_horas):
        self.verificar_disponibilidad()
        self.validar_parametros(duracion_horas)

        duracion_horas = float(duracion_horas)
        adicional_video = 25000 if self.incluye_video_beam else 0

        return (self.costo_base * duracion_horas) + adicional_video

    def descripcion(self):
        video = "Sí" if self.incluye_video_beam else "No"

        return (
            f"Servicio ID: {self.id} | "
            f"Tipo: Reserva de sala | "
            f"Nombre: {self.nombre} | "
            f"Capacidad: {self.capacidad} personas | "
            f"Video beam: {video} | "
            f"Costo base por hora: ${self.costo_base:,.2f}"
        )


# ============================================================
# SERVICIO ESPECIALIZADO 2: ALQUILER DE EQUIPO
# ============================================================

class AlquilerEquipo(Servicio):
    """Servicio especializado para alquiler de equipos tecnológicos."""

    def __init__(self, nombre, costo_base, tipo_equipo, requiere_seguro=True, disponible=True):
        super().__init__(nombre, costo_base, disponible)

        self.tipo_equipo = tipo_equipo
        self.requiere_seguro = requiere_seguro

        self._validar_configuracion()

        logging.info(
            f"Servicio creado | Tipo: AlquilerEquipo | ID: {self.id} | Nombre: {self.nombre}"
        )

    def _validar_configuracion(self):
        tipos_validos = ["computador", "proyector", "tablet", "camara", "sonido"]

        if not isinstance(self.tipo_equipo, str):
            raise DatoInvalidoError("El tipo de equipo debe ser texto.")

        self.tipo_equipo = self.tipo_equipo.strip().lower()

        if self.tipo_equipo not in tipos_validos:
            raise DatoInvalidoError(
                f"Tipo de equipo inválido. Opciones válidas: {', '.join(tipos_validos)}."
            )

        if not isinstance(self.requiere_seguro, bool):
            raise DatoInvalidoError("El valor de seguro debe ser True o False.")

    def validar_parametros(self, duracion_horas):
        try:
            duracion_horas = float(duracion_horas)

            if duracion_horas <= 0:
                raise ValueError("La duración debe ser mayor que cero.")

            if duracion_horas > 72:
                raise ValueError("Un equipo no puede alquilarse por más de 72 horas.")

        except ValueError as error_original:
            raise ReservaInvalidaError(
                "Parámetros inválidos para alquilar un equipo."
            ) from error_original

    def calcular_costo(self, duracion_horas):
        self.verificar_disponibilidad()
        self.validar_parametros(duracion_horas)

        duracion_horas = float(duracion_horas)
        valor_seguro = 35000 if self.requiere_seguro else 0

        return (self.costo_base * duracion_horas) + valor_seguro

    def descripcion(self):
        seguro = "Sí" if self.requiere_seguro else "No"

        return (
            f"Servicio ID: {self.id} | "
            f"Tipo: Alquiler de equipo | "
            f"Nombre: {self.nombre} | "
            f"Equipo: {self.tipo_equipo.title()} | "
            f"Seguro: {seguro} | "
            f"Costo base por hora: ${self.costo_base:,.2f}"
        )


# ============================================================
# SERVICIO ESPECIALIZADO 3: ASESORÍA ESPECIALIZADA
# ============================================================

class AsesoriaEspecializada(Servicio):
    """Servicio especializado para asesorías profesionales."""

    def __init__(self, nombre, costo_base, area, nivel_experto="intermedio", disponible=True):
        super().__init__(nombre, costo_base, disponible)

        self.area = area
        self.nivel_experto = nivel_experto

        self._validar_configuracion()

        logging.info(
            f"Servicio creado | Tipo: AsesoriaEspecializada | ID: {self.id} | Nombre: {self.nombre}"
        )

    def _validar_configuracion(self):
        if not isinstance(self.area, str):
            raise DatoInvalidoError("El área de asesoría debe ser texto.")

        self.area = self.area.strip()

        if len(self.area) < 4:
            raise DatoInvalidoError("El área de asesoría debe tener mínimo 4 caracteres.")

        niveles_validos = ["basico", "intermedio", "avanzado"]

        if not isinstance(self.nivel_experto, str):
            raise DatoInvalidoError("El nivel experto debe ser texto.")

        self.nivel_experto = self.nivel_experto.strip().lower()

        if self.nivel_experto not in niveles_validos:
            raise DatoInvalidoError(
                "El nivel experto debe ser: basico, intermedio o avanzado."
            )

    def validar_parametros(self, duracion_horas):
        try:
            duracion_horas = float(duracion_horas)

            if duracion_horas <= 0:
                raise ValueError("La duración debe ser mayor que cero.")

            if duracion_horas > 6:
                raise ValueError("Una asesoría no puede superar 6 horas por sesión.")

        except ValueError as error_original:
            raise ReservaInvalidaError(
                "Parámetros inválidos para agendar una asesoría especializada."
            ) from error_original

    def calcular_costo(self, duracion_horas):
        self.verificar_disponibilidad()
        self.validar_parametros(duracion_horas)

        duracion_horas = float(duracion_horas)

        multiplicadores = {
            "basico": 1.0,
            "intermedio": 1.25,
            "avanzado": 1.6
        }

        multiplicador = multiplicadores[self.nivel_experto]

        return self.costo_base * duracion_horas * multiplicador

    def descripcion(self):
        return (
            f"Servicio ID: {self.id} | "
            f"Tipo: Asesoría especializada | "
            f"Nombre: {self.nombre} | "
            f"Área: {self.area.title()} | "
            f"Nivel experto: {self.nivel_experto.title()} | "
            f"Costo base por hora: ${self.costo_base:,.2f}"
        )


# ============================================================
# CLASE RESERVA
# ============================================================

class Reserva(EntidadSistema):
    """Representa una reserva realizada por un cliente sobre un servicio."""

    ESTADO_CREADA = "Creada"
    ESTADO_CONFIRMADA = "Confirmada"
    ESTADO_CANCELADA = "Cancelada"
    ESTADO_PROCESADA = "Procesada"

    def __init__(self, cliente, servicio, duracion_horas):
        super().__init__()

        if not isinstance(cliente, Cliente):
            raise ReservaInvalidaError("La reserva debe tener un cliente válido.")

        if not isinstance(servicio, Servicio):
            raise ReservaInvalidaError("La reserva debe tener un servicio válido.")

        try:
            duracion_horas = float(duracion_horas)

            if duracion_horas <= 0:
                raise ValueError("La duración debe ser mayor que cero.")

        except ValueError as error_original:
            raise ReservaInvalidaError(
                "La duración de la reserva no es válida."
            ) from error_original

        servicio.validar_parametros(duracion_horas)

        self.cliente = cliente
        self.servicio = servicio
        self.duracion_horas = duracion_horas
        self.estado = self.ESTADO_CREADA
        self.costo_total = 0.0

        logging.info(
            f"Reserva creada | ID: {self.id} | Cliente: {cliente.nombre} | "
            f"Servicio: {servicio.nombre} | Duración: {duracion_horas} horas"
        )

    def confirmar(self):
        """Confirma una reserva si cumple las condiciones."""

        if self.estado == self.ESTADO_CANCELADA:
            raise OperacionNoPermitidaError("No se puede confirmar una reserva cancelada.")

        if self.estado == self.ESTADO_CONFIRMADA:
            raise OperacionNoPermitidaError("La reserva ya se encuentra confirmada.")

        if self.estado == self.ESTADO_PROCESADA:
            raise OperacionNoPermitidaError("La reserva ya fue procesada.")

        self.servicio.verificar_disponibilidad()
        self.servicio.validar_parametros(self.duracion_horas)

        self.estado = self.ESTADO_CONFIRMADA

        logging.info(f"Reserva confirmada | ID: {self.id}")

    def cancelar(self):
        """Cancela una reserva si el estado actual lo permite."""

        if self.estado == self.ESTADO_CANCELADA:
            raise OperacionNoPermitidaError("La reserva ya se encuentra cancelada.")

        if self.estado == self.ESTADO_PROCESADA:
            raise OperacionNoPermitidaError("No se puede cancelar una reserva ya procesada.")

        self.estado = self.ESTADO_CANCELADA

        logging.warning(f"Reserva cancelada | ID: {self.id}")

    def procesar(self, impuesto=0.19, descuento=0.0):
        """Procesa una reserva calculando el costo final."""

        if self.estado == self.ESTADO_CANCELADA:
            raise OperacionNoPermitidaError("No se puede procesar una reserva cancelada.")

        if self.estado == self.ESTADO_PROCESADA:
            raise OperacionNoPermitidaError("La reserva ya fue procesada anteriormente.")

        try:
            self.confirmar()

            self.costo_total = self.servicio.calcular_costo_con_opciones(
                self.duracion_horas,
                impuesto=impuesto,
                descuento=descuento
            )

            self.estado = self.ESTADO_PROCESADA

        except SistemaFJError:
            raise

        except Exception as error_original:
            raise ReservaInvalidaError(
                "No fue posible procesar la reserva."
            ) from error_original

        else:
            logging.info(
                f"Reserva procesada exitosamente | ID: {self.id} | "
                f"Total: ${self.costo_total:,.2f}"
            )

            return self.costo_total

        finally:
            logging.info(f"Finalizó intento de procesamiento de reserva | ID: {self.id}")

    def descripcion(self):
        return (
            f"Reserva ID: {self.id} | "
            f"Cliente: {self.cliente.nombre} | "
            f"Servicio: {self.servicio.nombre} | "
            f"Duración: {self.duracion_horas} horas | "
            f"Estado: {self.estado} | "
            f"Total: ${self.costo_total:,.2f}"
        )

    def __str__(self):
        return self.descripcion()


# ============================================================
# CLASE PRINCIPAL DEL SISTEMA SOFTWARE FJ
# ============================================================

class SistemaSoftwareFJ:
    """
    Clase principal que administra clientes, servicios y reservas.
    No utiliza bases de datos. Toda la gestión se realiza mediante listas internas.
    """

    def __init__(self):
        self.clientes = []
        self.servicios = []
        self.reservas = []

        logging.info("Sistema Software FJ inicializado correctamente.")

    def registrar_cliente(self, nombre, documento, correo, telefono):
        """Registra un cliente después de validar duplicidad por documento."""

        documento_normalizado = str(documento).strip()

        if self.buscar_cliente_por_documento(documento_normalizado):
            raise ClienteDuplicadoError(
                f"Ya existe un cliente registrado con el documento {documento_normalizado}."
            )

        cliente = Cliente(nombre, documento, correo, telefono)
        self.clientes.append(cliente)

        logging.info(f"Cliente agregado a la lista interna | ID: {cliente.id}")

        return cliente

    def buscar_cliente_por_documento(self, documento):
        """Busca un cliente por documento."""

        documento = str(documento).strip()

        for cliente in self.clientes:
            if cliente.documento == documento:
                return cliente

        return None

    def agregar_servicio(self, servicio):
        """Agrega un servicio a la lista interna del sistema."""

        if not isinstance(servicio, Servicio):
            raise DatoInvalidoError("Solo se pueden agregar objetos derivados de Servicio.")

        self.servicios.append(servicio)

        logging.info(f"Servicio agregado a la lista interna | ID: {servicio.id}")

        return servicio

    def buscar_servicio_por_id(self, id_servicio):
        """Busca un servicio por ID."""

        for servicio in self.servicios:
            if servicio.id == id_servicio:
                return servicio

        return None

    def crear_reserva(self, cliente, servicio, duracion_horas):
        """Crea una reserva y la agrega a la lista interna."""

        reserva = Reserva(cliente, servicio, duracion_horas)
        self.reservas.append(reserva)

        logging.info(f"Reserva agregada a la lista interna | ID: {reserva.id}")

        return reserva

    def listar_clientes(self):
        """Devuelve un texto con todos los clientes registrados."""

        if not self.clientes:
            return "No hay clientes registrados."

        resultado = "\nCLIENTES REGISTRADOS:\n"

        for cliente in self.clientes:
            resultado += f"- {cliente.descripcion()}\n"

        return resultado

    def listar_servicios(self):
        """Devuelve un texto con todos los servicios registrados."""

        if not self.servicios:
            return "No hay servicios registrados."

        resultado = "\nSERVICIOS REGISTRADOS:\n"

        for servicio in self.servicios:
            estado = "Disponible" if servicio.disponible else "No disponible"
            resultado += f"- {servicio.descripcion()} | Estado: {estado}\n"

        return resultado

    def listar_reservas(self):
        """Devuelve un texto con todas las reservas registradas."""

        if not self.reservas:
            return "No hay reservas registradas."

        resultado = "\nRESERVAS REGISTRADAS:\n"

        for reserva in self.reservas:
            resultado += f"- {reserva.descripcion()}\n"

        return resultado

    def generar_resumen_general(self):
        """Genera un resumen administrativo del sistema."""

        total_clientes = len(self.clientes)
        total_servicios = len(self.servicios)
        total_reservas = len(self.reservas)

        reservas_procesadas = 0
        reservas_canceladas = 0
        ingresos_totales = 0.0

        for reserva in self.reservas:
            if reserva.estado == Reserva.ESTADO_PROCESADA:
                reservas_procesadas += 1
                ingresos_totales += reserva.costo_total

            if reserva.estado == Reserva.ESTADO_CANCELADA:
                reservas_canceladas += 1

        resumen = "\nRESUMEN GENERAL DEL SISTEMA:\n"
        resumen += f"- Total de clientes registrados: {total_clientes}\n"
        resumen += f"- Total de servicios registrados: {total_servicios}\n"
        resumen += f"- Total de reservas registradas: {total_reservas}\n"
        resumen += f"- Reservas procesadas: {reservas_procesadas}\n"
        resumen += f"- Reservas canceladas: {reservas_canceladas}\n"
        resumen += f"- Ingresos totales simulados: ${ingresos_totales:,.2f}\n"

        return resumen


# ============================================================
# FUNCIÓN CONTROLADORA DE OPERACIONES
# ============================================================

def ejecutar_operacion(nombre_operacion, funcion, *args, **kwargs):
    """
    Ejecuta una operación de forma segura.

    Esta función permite demostrar:
    - try
    - except
    - else
    - finally

    Además, evita que el programa se cierre cuando ocurre un error.
    """

    print("\n" + "=" * 90)
    print(f"OPERACIÓN: {nombre_operacion}")
    print("=" * 90)

    try:
        resultado = funcion(*args, **kwargs)

    except SistemaFJError as error:
        print(f"ERROR CONTROLADO: {error}")
        logging.error(
            f"{nombre_operacion} | Error controlado: {error}",
            exc_info=True
        )
        return None

    except Exception as error:
        print(f"ERROR INESPERADO: {error}")
        logging.critical(
            f"{nombre_operacion} | Error inesperado: {error}",
            exc_info=True
        )
        return None

    else:
        print("Operación ejecutada correctamente.")

        if resultado is not None:
            print(resultado)

        logging.info(f"{nombre_operacion} | Operación ejecutada correctamente.")

        return resultado

    finally:
        print("Finalizó la ejecución de la operación.")
        logging.info(f"{nombre_operacion} | Bloque finally ejecutado.")


# ============================================================
# FUNCIONES AUXILIARES PARA CREAR SERVICIOS
# ============================================================

def crear_servicio_reserva_sala(sistema, nombre, costo_base, capacidad, incluye_video_beam=True, disponible=True):
    """Crea y agrega un servicio de reserva de sala."""

    servicio = ReservaSala(
        nombre=nombre,
        costo_base=costo_base,
        capacidad=capacidad,
        incluye_video_beam=incluye_video_beam,
        disponible=disponible
    )

    return sistema.agregar_servicio(servicio)


def crear_servicio_alquiler_equipo(sistema, nombre, costo_base, tipo_equipo, requiere_seguro=True, disponible=True):
    """Crea y agrega un servicio de alquiler de equipo."""

    servicio = AlquilerEquipo(
        nombre=nombre,
        costo_base=costo_base,
        tipo_equipo=tipo_equipo,
        requiere_seguro=requiere_seguro,
        disponible=disponible
    )

    return sistema.agregar_servicio(servicio)


def crear_servicio_asesoria(sistema, nombre, costo_base, area, nivel_experto="intermedio", disponible=True):
    """Crea y agrega un servicio de asesoría especializada."""

    servicio = AsesoriaEspecializada(
        nombre=nombre,
        costo_base=costo_base,
        area=area,
        nivel_experto=nivel_experto,
        disponible=disponible
    )

    return sistema.agregar_servicio(servicio)


# ============================================================
# PRUEBAS SIMULADAS DEL SISTEMA
# ============================================================

def ejecutar_pruebas_simuladas():
    """
    Ejecuta más de 10 operaciones completas, válidas e inválidas.

    Estas pruebas demuestran que el sistema:
    - Valida datos.
    - Controla errores.
    - No se detiene ante excepciones.
    - Registra eventos en archivo de logs.
    - Usa programación orientada a objetos.
    """

    sistema = SistemaSoftwareFJ()

    print("\n")
    print("#" * 90)
    print("SISTEMA INTEGRAL DE GESTIÓN DE CLIENTES, SERVICIOS Y RESERVAS")
    print("EMPRESA SOFTWARE FJ")
    print("FASE 4 - PRÁCTICAS SIMULADAS")
    print("#" * 90)

    # ========================================================
    # CLIENTES VÁLIDOS E INVÁLIDOS
    # ========================================================

    cliente_1 = ejecutar_operacion(
        "1. Registro válido de cliente principal",
        sistema.registrar_cliente,
        "Carlos Andrés Ramírez",
        "1020304050",
        "carlos.ramirez@email.com",
        "3001234567"
    )

    cliente_2 = ejecutar_operacion(
        "2. Registro válido de segundo cliente",
        sistema.registrar_cliente,
        "Laura Marcela Torres",
        "1098765432",
        "laura.torres@email.com",
        "3109876543"
    )

    cliente_3 = ejecutar_operacion(
        "3. Registro válido de tercer cliente",
        sistema.registrar_cliente,
        "Miguel Ángel Pardo",
        "1002003004",
        "miguel.pardo@email.com",
        "3205557788"
    )

    ejecutar_operacion(
        "4. Registro inválido de cliente sin nombre",
        sistema.registrar_cliente,
        "",
        "111222333",
        "usuario@email.com",
        "3001112233"
    )

    ejecutar_operacion(
        "5. Registro inválido de cliente con correo incorrecto",
        sistema.registrar_cliente,
        "Pedro López",
        "1234567891",
        "correo_invalido",
        "3001112233"
    )

    ejecutar_operacion(
        "6. Registro inválido de cliente con documento no numérico",
        sistema.registrar_cliente,
        "Ana María Gómez",
        "ABC123",
        "ana.gomez@email.com",
        "3002223344"
    )

    ejecutar_operacion(
        "7. Registro inválido de cliente duplicado",
        sistema.registrar_cliente,
        "Carlos Andrés Ramírez",
        "1020304050",
        "otro.correo@email.com",
        "3009998888"
    )

    # ========================================================
    # SERVICIOS VÁLIDOS E INVÁLIDOS
    # ========================================================

    sala_juntas = ejecutar_operacion(
        "8. Creación correcta de servicio: Reserva de sala",
        crear_servicio_reserva_sala,
        sistema,
        "Sala de juntas ejecutiva",
        85000,
        20,
        True,
        True
    )

    sala_capacitacion = ejecutar_operacion(
        "9. Creación correcta de servicio: Sala de capacitación",
        crear_servicio_reserva_sala,
        sistema,
        "Sala de capacitación empresarial",
        65000,
        35,
        True,
        True
    )

    equipo_computo = ejecutar_operacion(
        "10. Creación correcta de servicio: Alquiler de computador",
        crear_servicio_alquiler_equipo,
        sistema,
        "Alquiler computador portátil",
        45000,
        "computador",
        True,
        True
    )

    proyector = ejecutar_operacion(
        "11. Creación correcta de servicio: Alquiler de proyector",
        crear_servicio_alquiler_equipo,
        sistema,
        "Alquiler proyector corporativo",
        30000,
        "proyector",
        False,
        True
    )

    asesoria_software = ejecutar_operacion(
        "12. Creación correcta de servicio: Asesoría especializada",
        crear_servicio_asesoria,
        sistema,
        "Asesoría en arquitectura de software",
        120000,
        "Ingeniería de software",
        "avanzado",
        True
    )

    asesoria_datos = ejecutar_operacion(
        "13. Creación correcta de servicio: Asesoría en análisis de datos",
        crear_servicio_asesoria,
        sistema,
        "Asesoría en análisis de datos",
        95000,
        "Analítica de datos",
        "intermedio",
        True
    )

    ejecutar_operacion(
        "14. Creación inválida de servicio con costo negativo",
        crear_servicio_reserva_sala,
        sistema,
        "Sala defectuosa",
        -50000,
        10,
        False,
        True
    )

    ejecutar_operacion(
        "15. Creación inválida de servicio con tipo de equipo no permitido",
        crear_servicio_alquiler_equipo,
        sistema,
        "Equipo inexistente",
        30000,
        "helicoptero",
        True,
        True
    )

    ejecutar_operacion(
        "16. Creación inválida de asesoría con nivel experto incorrecto",
        crear_servicio_asesoria,
        sistema,
        "Asesoría mal configurada",
        90000,
        "Software",
        "maestro",
        True
    )

    # ========================================================
    # RESERVAS VÁLIDAS E INVÁLIDAS
    # ========================================================

    reserva_1 = None
    reserva_2 = None
    reserva_3 = None
    reserva_4 = None

    if cliente_1 and sala_juntas:
        reserva_1 = ejecutar_operacion(
            "17. Creación válida de reserva de sala",
            sistema.crear_reserva,
            cliente_1,
            sala_juntas,
            3
        )

    if reserva_1:
        ejecutar_operacion(
            "18. Procesamiento exitoso de reserva de sala con impuesto y descuento",
            reserva_1.procesar,
            impuesto=0.19,
            descuento=0.10
        )

    if cliente_2 and equipo_computo:
        reserva_2 = ejecutar_operacion(
            "19. Creación válida de reserva de equipo",
            sistema.crear_reserva,
            cliente_2,
            equipo_computo,
            5
        )

    if reserva_2:
        ejecutar_operacion(
            "20. Cancelación correcta de reserva de equipo",
            reserva_2.cancelar
        )

    if reserva_2:
        ejecutar_operacion(
            "21. Intento inválido de procesar una reserva cancelada",
            reserva_2.procesar,
            impuesto=0.19,
            descuento=0
        )

    if cliente_3 and asesoria_software:
        reserva_3 = ejecutar_operacion(
            "22. Creación válida de reserva de asesoría especializada",
            sistema.crear_reserva,
            cliente_3,
            asesoria_software,
            2
        )

    if reserva_3:
        ejecutar_operacion(
            "23. Procesamiento exitoso de asesoría especializada",
            reserva_3.procesar,
            impuesto=0.19,
            descuento=0.05
        )

    if cliente_1 and asesoria_datos:
        ejecutar_operacion(
            "24. Intento inválido de reserva con duración cero",
            sistema.crear_reserva,
            cliente_1,
            asesoria_datos,
            0
        )

    if cliente_1 and sala_capacitacion:
        ejecutar_operacion(
            "25. Intento inválido de reserva de sala por más de 8 horas",
            sistema.crear_reserva,
            cliente_1,
            sala_capacitacion,
            10
        )

    if cliente_2 and asesoria_datos:
        reserva_4 = ejecutar_operacion(
            "26. Creación válida de reserva antes de deshabilitar servicio",
            sistema.crear_reserva,
            cliente_2,
            asesoria_datos,
            2
        )

    if asesoria_datos:
        ejecutar_operacion(
            "27. Deshabilitar servicio de asesoría en datos",
            asesoria_datos.cambiar_disponibilidad,
            False
        )

    if reserva_4:
        ejecutar_operacion(
            "28. Intento inválido de procesar reserva con servicio no disponible",
            reserva_4.procesar,
            impuesto=0.19,
            descuento=0
        )

    if reserva_3:
        ejecutar_operacion(
            "29. Intento inválido de cancelar reserva ya procesada",
            reserva_3.cancelar
        )

    if reserva_1:
        ejecutar_operacion(
            "30. Intento inválido de procesar reserva ya procesada",
            reserva_1.procesar
        )

    if cliente_3 and proyector:
        reserva_5 = ejecutar_operacion(
            "31. Creación válida de reserva de proyector",
            sistema.crear_reserva,
            cliente_3,
            proyector,
            4
        )

        if reserva_5:
            ejecutar_operacion(
                "32. Procesamiento exitoso de reserva de proyector sin descuento",
                reserva_5.procesar,
                impuesto=0.19,
                descuento=0
            )

    # ========================================================
    # LISTADOS Y RESUMEN FINAL
    # ========================================================

    ejecutar_operacion(
        "33. Listado general de clientes",
        sistema.listar_clientes
    )

    ejecutar_operacion(
        "34. Listado general de servicios",
        sistema.listar_servicios
    )

    ejecutar_operacion(
        "35. Listado general de reservas",
        sistema.listar_reservas
    )

    ejecutar_operacion(
        "36. Resumen general del sistema",
        sistema.generar_resumen_general
    )

    print("\n")
    print("#" * 90)
    print("PRUEBAS SIMULADAS FINALIZADAS")
    print("Se generó el archivo 'eventos_sistema.log' en la misma carpeta del proyecto.")
    print("#" * 90)

    logging.info("Todas las pruebas simuladas finalizaron correctamente.")

    return sistema


# ============================================================
# MENÚ INTERACTIVO OPCIONAL
# ============================================================

def menu_interactivo(sistema):
    """Menú básico para consultar la información después de las pruebas simuladas."""

    while True:
        print("\n" + "=" * 90)
        print("MENÚ PRINCIPAL - SOFTWARE FJ")
        print("=" * 90)
        print("1. Ver clientes registrados")
        print("2. Ver servicios registrados")
        print("3. Ver reservas registradas")
        print("4. Ver resumen general")
        print("5. Registrar nuevo cliente")
        print("6. Crear nueva reserva básica")
        print("7. Salir")
        print("=" * 90)

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            print(sistema.listar_clientes())

        elif opcion == "2":
            print(sistema.listar_servicios())

        elif opcion == "3":
            print(sistema.listar_reservas())

        elif opcion == "4":
            print(sistema.generar_resumen_general())

        elif opcion == "5":
            registrar_cliente_desde_menu(sistema)

        elif opcion == "6":
            crear_reserva_desde_menu(sistema)

        elif opcion == "7":
            print("Finalizando sistema Software FJ.")
            logging.info("Sistema finalizado desde el menú interactivo.")
            break

        else:
            print("Opción no válida. Intente nuevamente.")
            logging.warning("El usuario ingresó una opción no válida en el menú interactivo.")


def registrar_cliente_desde_menu(sistema):
    """Permite registrar un cliente desde el menú interactivo."""

    print("\nREGISTRO DE NUEVO CLIENTE")

    nombre = input("Nombre completo: ")
    documento = input("Documento: ")
    correo = input("Correo electrónico: ")
    telefono = input("Teléfono: ")

    ejecutar_operacion(
        "Registro manual de cliente desde menú",
        sistema.registrar_cliente,
        nombre,
        documento,
        correo,
        telefono
    )


def crear_reserva_desde_menu(sistema):
    """Permite crear y procesar una reserva desde el menú interactivo."""

    print("\nCREACIÓN DE RESERVA DESDE MENÚ")

    if not sistema.clientes:
        print("No hay clientes registrados.")
        return

    if not sistema.servicios:
        print("No hay servicios registrados.")
        return

    print("\nClientes disponibles:")
    for indice, cliente in enumerate(sistema.clientes, start=1):
        print(f"{indice}. {cliente.nombre} - Documento: {cliente.documento}")

    print("\nServicios disponibles:")
    for indice, servicio in enumerate(sistema.servicios, start=1):
        estado = "Disponible" if servicio.disponible else "No disponible"
        print(f"{indice}. {servicio.nombre} - {estado}")

    try:
        indice_cliente = int(input("\nSeleccione el número del cliente: "))
        indice_servicio = int(input("Seleccione el número del servicio: "))
        duracion = float(input("Ingrese la duración en horas: "))

        if indice_cliente < 1 or indice_cliente > len(sistema.clientes):
            raise DatoInvalidoError("El número de cliente seleccionado no existe.")

        if indice_servicio < 1 or indice_servicio > len(sistema.servicios):
            raise DatoInvalidoError("El número de servicio seleccionado no existe.")

        cliente = sistema.clientes[indice_cliente - 1]
        servicio = sistema.servicios[indice_servicio - 1]

        reserva = ejecutar_operacion(
            "Creación manual de reserva desde menú",
            sistema.crear_reserva,
            cliente,
            servicio,
            duracion
        )

        if reserva:
            ejecutar_operacion(
                "Procesamiento manual de reserva desde menú",
                reserva.procesar,
                impuesto=0.19,
                descuento=0
            )

    except ValueError:
        logging.error("Error de conversión en menú de reserva.", exc_info=True)
        print("ERROR CONTROLADO: Debe ingresar valores numéricos válidos.")

    except SistemaFJError as error:
        logging.error(f"Error controlado en menú de reserva: {error}", exc_info=True)
        print(f"ERROR CONTROLADO: {error}")

    except Exception as error:
        logging.critical(f"Error inesperado en menú de reserva: {error}", exc_info=True)
        print(f"ERROR INESPERADO: {error}")

    finally:
        logging.info("Finalizó intento de creación manual de reserva desde menú.")


# ============================================================
# PUNTO DE ENTRADA DEL PROGRAMA
# ============================================================

if __name__ == "__main__":
    sistema_fj = ejecutar_pruebas_simuladas()

    respuesta = input("\n¿Desea abrir el menú interactivo? S/N: ").strip().lower()

    if respuesta == "s":
        menu_interactivo(sistema_fj)
    else:
        print("\nPrograma finalizado correctamente.")
        print("Revise el archivo 'eventos_sistema.log' para verificar el registro de eventos y errores.")
        logging.info("Programa finalizado sin abrir menú interactivo.")
