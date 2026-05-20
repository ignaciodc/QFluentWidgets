# Practica QFluentWidgets

Este proyecto responde al enunciado del PDF `QFluentWidgets.pdf`.

Incluye:

- Dos manuales académicos en `docs/manual_python_librerias_PyQt_PySide.md` y `docs/manual_qfluentwidgets.md`.
- Una aplicación CRUD de escritorio con PyQt5, QFluentWidgets y SQLite.
- Una estructura sencilla para poder ampliarla o subirla a un repositorio.

## Instalacion


```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

## Ejecucion

```powershell
python src\main.py
```

La base de datos se crea automaticamente en `data/academia.db`.

## Estructura

```text
.
|-- docs/
|   `-- manual_python_librerias_PyQt_PySide.md
|   `-- manual_qfluentwidgets.md
|-- src/
|   |-- database.py
|   `-- main.py
|-- data/
|   `-- .gitkeep
|   `-- academia.db
|-- requirements.txt
`-- README.md
```

## Funcionalidad del CRUD

- Crear alumnos.
- Listar alumnos en una tabla.
- Buscar por texto.
- Filtrar por curso.
- Editar el alumno seleccionado.
- Eliminar con confirmacion.
- Cambiar entre tema claro y oscuro.

