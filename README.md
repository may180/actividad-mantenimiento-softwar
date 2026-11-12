# Manteni — control de mantenimiento

Proyecto académico individual para el taller de mantenimiento de software. La aplicación estática permite consultar activos y órdenes de trabajo, registrar activos, crear órdenes con prioridad y revisar las cinco historias de usuario implementadas.

## Datos del estudiante

- **Nombre:** Maikol Lozano
- **Correo informado:** maikollozano6@gmail.com
- **IdBanner:** may180
- **Repositorio:** https://github.com/may180/actividad-mantenimiento-softwar

## Ejecutar el proyecto

Abra `index.html` en un navegador. No requiere instalación ni servicios externos. Los cambios de activos y órdenes se mantienen solo en memoria y se reinician al recargar la página; es un prototipo de demostración, no un sistema de producción.

## Historias de usuario

1. **HU-01:** Como técnico, quiero consultar el inventario de activos para planificar su mantenimiento.
2. **HU-02:** Como supervisor, quiero registrar activos con ubicación para mantener el inventario actualizado.
3. **HU-03:** Como técnico, quiero crear órdenes de trabajo con prioridad y activo asociado.
4. **HU-04:** Como coordinador, quiero revisar el estado de órdenes y activos para priorizar tareas.
5. **HU-05:** Como estudiante, quiero consultar mis historias y los cambios de mi repositorio para verificar mi trabajo individual.

## Estructura

- `index.html`: estructura semántica, panel, formularios y navegación.
- `styles.css`: estilos adaptables y estados visuales.
- `app.js`: datos de demostración y lógica de interacción.
- `docs/historias-de-usuario.md`: historias, criterios de aceptación y estado.
- `docs/taller-mantenimiento.pdf`: informe individual del taller.
- `create_report.py`: generador reproducible del informe PDF.

## Flujo de trabajo Git

El historial del repositorio permite revisar los cambios individuales. El PDF documenta el flujo de clonación, estado, ramas, staging, commits y push, e incluye evidencia visual de la aplicación y del historial publicado. El taller original describe equipos de hasta tres estudiantes; esta versión se presenta como individual a solicitud del estudiante, por lo que debe confirmarse con el docente-tutor que acepta esta modalidad.

El archivo `.gitignore` excluye archivos locales que no deben versionarse. El repositorio se consulta en https://github.com/may180/actividad-mantenimiento-softwar.
