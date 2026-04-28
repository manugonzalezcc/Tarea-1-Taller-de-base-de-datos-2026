# Tarea 1 — Taller de Base de Datos (2026)

Sistema simple de gestión de deportistas y competencias, implementado en Python con enfoque en Programación Orientada a Objetos.

## Cómo ejecutar
1. Abre una terminal en esta carpeta.
2. Ejecuta:

```bash
python "Gestión_de_deportistas.py"
```

El script incluye una simulación mínima (`__main__`) que registra deportistas, crea una competencia, inscribe participantes y muestra rankings/resultados.

## Qué incluye
- Clase abstracta `Deportista` (encapsulamiento de puntaje y competencias).
- `Registro` para almacenar, buscar y mostrar rankings.
- `Competencia` para inscripción y registro de resultados (validaciones con excepciones).
- Subclases `Futbolista`, `Tenista` y `Atleta` con polimorfismo en `obtener_informacion_basica()`.