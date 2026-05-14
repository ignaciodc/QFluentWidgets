# Manual de QFluentWidgets

Este documento explica el framework QFluentWidgets y describe cómo se usa en la aplicación CRUD de este proyecto.

Para la parte de bibliotecas Python (PyQt y PySide), consulta el documento separado `docs/manual_python_gui.md`.

## 1. ¿Qué es QFluentWidgets?

QFluentWidgets es una biblioteca de componentes basados en Qt que sigue el estilo Fluent Design de Microsoft. Su objetivo es facilitar el desarrollo de interfaces modernas, con:

- Widgets ya estilizados.
- Efectos y animaciones suaves.
- Soporte de tema claro y oscuro.
- Controles de navegación y tarjetas.
- Notificaciones y diálogos modernos.

El paquete se importa con `qfluentwidgets`, y se utiliza junto con Qt estándar.

## 2. Instalación

Para instalar QFluentWidgets con PyQt5:

```powershell
pip install PyQt-Fluent-Widgets
```

Si utilizas PySide en otro proyecto, existen paquetes equivalentes como:

- `PySide2-Fluent-Widgets`
- `PySide6-Fluent-Widgets`

No conviene instalar varias variantes simultáneamente porque todas comparten el nombre del paquete `qfluentwidgets`.

