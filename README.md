# Sistema Integral de Gestión de Clientes, Servicios y Reservas - Software FJ

## Descripción del proyecto

Este proyecto corresponde a la Fase 4 del curso Programación 213023 de la Universidad Nacional Abierta y a Distancia - UNAD.

El sistema desarrollado permite gestionar clientes, servicios y reservas para la empresa Software FJ, aplicando programación orientada a objetos y manejo avanzado de excepciones.

## Funcionalidades principales

- Registro de clientes.
- Creación de servicios.
- Gestión de reservas.
- Confirmación, cancelación y procesamiento de reservas.
- Validación de datos.
- Manejo de errores mediante excepciones personalizadas.
- Registro de eventos y errores en archivo de logs.
- Simulación de operaciones válidas e inválidas.

## Conceptos aplicados

- Clases abstractas.
- Herencia.
- Polimorfismo.
- Encapsulación.
- Métodos sobrescritos.
- Simulación de sobrecarga mediante parámetros opcionales.
- Manejo de listas internas.
- Excepciones personalizadas.
- Bloques try/except.
- Bloques try/except/else.
- Bloques try/except/finally.
- Encadenamiento de excepciones.
- Archivo de logs.

## Archivos del proyecto

- `main.py`: contiene el código principal del sistema.
- `eventos_sistema.log`: archivo generado durante la ejecución del programa con eventos y errores registrados.
- `README.md`: descripción general del proyecto.

## Ejecución del programa

Para ejecutar el programa, se debe abrir el archivo `main.py` en Visual Studio o Visual Studio Code y ejecutar el archivo con Python.

```bash
python main.py
```

Al ejecutarse, el sistema realiza pruebas simuladas con registros válidos e inválidos, creación de servicios, reservas exitosas, reservas fallidas y manejo controlado de errores.

## Estructura general del sistema

El sistema trabaja sin bases de datos. Toda la información se administra mediante objetos y listas internas.

La arquitectura principal incluye:

- `EntidadSistema`: clase abstracta general.
- `Cliente`: clase para gestionar datos personales de clientes.
- `Servicio`: clase abstracta para servicios.
- `ReservaSala`: servicio especializado de reserva de salas.
- `AlquilerEquipo`: servicio especializado de alquiler de equipos.
- `AsesoriaEspecializada`: servicio especializado de asesorías.
- `Reserva`: clase que integra cliente, servicio, duración, estado y costo.
- `SistemaSoftwareFJ`: clase administradora de clientes, servicios y reservas.

## Manejo de excepciones

El proyecto incorpora excepciones personalizadas para controlar errores del sistema:

- `DatoInvalidoError`
- `ServicioNoDisponibleError`
- `ReservaInvalidaError`
- `CostoInvalidoError`
- `OperacionNoPermitidaError`
- `ClienteDuplicadoError`

También se implementa encadenamiento de excepciones mediante la instrucción `raise ... from ...`, lo cual permite conservar la causa original del error.

## Registro de logs

Durante la ejecución, el programa genera automáticamente el archivo:

```text
eventos_sistema.log
```

Este archivo almacena eventos relevantes, errores controlados, errores críticos, creación de clientes, creación de servicios, reservas, cancelaciones y procesamiento de operaciones.

## Autoría

Trabajo desarrollado como parte del componente práctico de la Fase 4 del curso Programación 213023.
