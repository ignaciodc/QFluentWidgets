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

## 3. Estructura de una aplicación QFluentWidgets

Una aplicación con QFluentWidgets sigue la misma estructura que una aplicación Qt normal, pero usa widgets específicos del framework.

Componentes comunes:

- `FluentWindow`: ventana principal con barra de navegación.
- `CardWidget`: tarjeta para agrupar contenido.
- `PushButton`, `PrimaryPushButton`: botones estándar y de acción principal.
- `LineEdit`, `SearchLineEdit`: campos de texto.
- `ComboBox`, `SpinBox`, `TextEdit`: controles de formulario.
- `InfoBar`: notificaciones.
- `MessageBox`: diálogos de confirmación.
- `FluentIcon`: iconos integrados.
- `setTheme` / `Theme`: cambiar el modo claro u oscuro.

Ejemplo básico:

```python
from qfluentwidgets import FluentWindow, PushButton, LineEdit, setTheme, Theme

class MainWindow(FluentWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mi App Fluent")
        self.setMinimumSize(800, 600)

        self.input = LineEdit()
        self.button = PushButton("Enviar")
        self.button.clicked.connect(self.on_submit)

        self.layout().addWidget(self.input)
        self.layout().addWidget(self.button)

    def on_submit(self):
        print(self.input.text())

app = QApplication(sys.argv)
setTheme(Theme.LIGHT)
window = MainWindow()
window.show()
sys.exit(app.exec())
```

## 4. Componentes clave de QFluentWidgets

### 4.1 FluentWindow

`FluentWindow` es la ventana principal que permite agregar subinterfaces con navegación lateral. Es ideal para apps con varias páginas.

### 4.2 CardWidget

`CardWidget` crea bloques visuales con borde y sombra suaves. Se usa para agrupar formularios, tablas y resúmenes.

### 4.3 Botones

- `PushButton`: botón secundario.
- `PrimaryPushButton`: botón destacado para la acción principal.

### 4.4 Campos de formulario

- `LineEdit`: campo de texto simple.
- `SearchLineEdit`: campo con estilo de búsqueda.
- `ComboBox`: lista desplegable.
- `SpinBox`: entrada numérica.
- `TextEdit`: área de texto multilineal.

### 4.5 Notificaciones y diálogos

- `InfoBar.success(...)`: muestra mensajes de éxito.
- `InfoBar.error(...)`: muestra mensajes de error.
- `MessageBox`: diálogo de confirmación.

## 5. Aplicación CRUD del proyecto

El proyecto implementa un CRUD de alumnos con estas páginas:

- `StudentsPage`: formulario y tabla de alumnos.
- `AboutPage`: resumen del proyecto y tecnologías.
- `SettingsPage`: cambio de tema claro/oscuro.

La ventana principal `MainWindow` usa `addSubInterface(...)` para agregar estas páginas a la navegación lateral.

### 5.1 StudentsPage

Incluye:

- formulario con `LineEdit`, `ComboBox`, `SpinBox`, `TextEdit`.
- botones `Guardar` y `Nuevo` en el formulario, y el botón `Eliminar` junto a la lista de alumnos.
- filtro con `SearchLineEdit` y `ComboBox` para buscar y filtrar registros.
- tabla `QTableWidget` para listar los registros.
- diseño en columnas: el formulario está a la izquierda y la lista de alumnos a la derecha.
- la tabla muestra los alumnos ordenados por `id` ascendente.

### 5.2 Interacción

- `save_button.clicked.connect(self.save_student)` guarda o actualiza un alumno.
- `new_button.clicked.connect(self.clear_form)` limpia el formulario.
- `delete_button.clicked.connect(self.confirm_delete)` pide confirmación antes de borrar.
- `search_input.textChanged.connect(self.refresh_table)` actualiza la tabla en tiempo real.
- `filter_input.currentTextChanged.connect(self.refresh_table)` filtra por curso.

### 5.3 Feedback visual

Se usan `InfoBar.success(...)` e `InfoBar.error(...)` para avisos al usuario.

## 6. Código importante del proyecto

### Cambiar tema

```python
class SettingsPage(QFrame):
    def change_theme(self, checked: bool) -> None:
        setTheme(Theme.DARK if checked else Theme.LIGHT)
```

### Añadir subinterfaces

```python
self.addSubInterface(self.students_page, FIF.PEOPLE, "Alumnos")
self.addSubInterface(self.about_page, FIF.DOCUMENT, "Manual")
self.addSubInterface(
    self.settings_page,
    FIF.SETTING,
    "Ajustes",
    position=NavigationItemPosition.BOTTOM,
)
```

## 7. Buenas prácticas con QFluentWidgets

- Usa `CardWidget` para separar visualmente secciones.
- Agrupa campos relacionados en un solo formulario.
- Muestra notificaciones claras con `InfoBar`.
- Valida entradas antes de guardarlas.
- No confíes exclusivamente en el estilo: la aplicación debe funcionar bien aunque el usuario cambie el tema.

## 8. Conclusión

QFluentWidgets es útil cuando buscas una interfaz Qt moderna sin construir todos los estilos manualmente. En este proyecto combina bien con PyQt5 y SQLite, porque mantiene la lógica de la aplicación separada de la presentación visual.

