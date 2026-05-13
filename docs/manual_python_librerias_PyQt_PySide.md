# Manual de bibliotecas gráficas en Python: PyQt y PySide

## 1. Introducción

Qt es un framework multiplataforma para crear interfaces gráficas. En Python se usan bindings que exponen las clases de Qt y permiten construir aplicaciones de escritorio.

Las dos bibliotecas más conocidas son:

- **PyQt**: desarrollada por Riverbank Computing.
- **PySide**: desarrollada y mantenida por The Qt Company.

Ambas permiten crear ventanas, botones, formularios, tablas, menús y todo tipo de componentes visuales, además de gestionar eventos, señales y estilos.

## 2. ¿Por qué usar Qt en Python?

Qt es ideal para aplicaciones de escritorio porque ofrece:

- Widgets ricos y consistentes en varias plataformas.
- Un sistema de diseño y posicionamiento responsive con layouts.
- Mecanismos de señal-slot para gestionar eventos.
- Soporte para temas, iconos, animaciones y estilos.
- Integración con bases de datos y abiertas de archivo.

Python aporta productividad y facilidad para escribir lógica de aplicación, mientras Qt aporta la interfaz profesional.

## 3. PyQt vs PySide

### 3.1 Licencia

- **PyQt** usa GPL o licencia comercial. Esto puede ser limitante si no se quiere publicar el código bajo GPL.
- **PySide** usa LGPL, más permisiva para proyectos privados o comerciales.

### 3.2 Compatibilidad y nombres

La API es muy similar entre ambas, pero hay algunas diferencias en nombres de módulos y en el ciclo de vida de la aplicación.

Por ejemplo:

- PyQt5 usa `from PyQt5.QtWidgets import QApplication`.
- PySide6 usa `from PySide6.QtWidgets import QApplication`.

En la mayoría de los casos, cambiar entre ellos es cuestión de cambiar el prefijo del paquete.

### 3.3 Ejecución

Ambas bibliotecas usan el método `app.exec()` en versiones recientes. En versiones más antiguas de PyQt se usaba `exec_()`.

### 3.4 Recomendación

- Usa **PyQt** si ya tienes experiencia con su licencia o si tu proyecto es open source bajo GPL.
- Usa **PySide** si necesitas una licencia más flexible (LGPL) o si prefieres el soporte oficial de Qt.

## 4. Instalación

Instalar PyQt5:

```powershell
pip install PyQt5
```

Instalar PySide6:

```powershell
pip install PySide6
```

Los nombres cambian si se quiere usar Qt6 o Qt5:

- `PyQt5`, `PyQt6`
- `PySide2`, `PySide6`

No conviene mezclar bindings diferentes en el mismo proyecto.

## 5. Estructura básica de una aplicación Qt

Una aplicación Qt básica sigue estos pasos:

1. Crear un objeto `QApplication`.
2. Crear una ventana o widget principal.
3. Añadir widgets hijos y layouts.
4. Conectar señales a slots.
5. Ejecutar el bucle de eventos con `app.exec()`.

Ejemplo mínimo con PyQt5:

```python
import sys
from PyQt5.QtWidgets import QApplication, QLabel

app = QApplication(sys.argv)
label = QLabel("Hola Qt")
label.resize(240, 80)
label.show()
sys.exit(app.exec())
```

Ejemplo mínimo con PySide6:

```python
import sys
from PySide6.QtWidgets import QApplication, QLabel

app = QApplication(sys.argv)
label = QLabel("Hola Qt")
label.resize(240, 80)
label.show()
sys.exit(app.exec())
```

## 6. Widgets comunes

Algunos widgets básicos que se usan con frecuencia:

- `QWidget`: widget genérico que puede contener otros widgets.
- `QMainWindow`: ventana principal con barra de menús, barra de herramientas y área central.
- `QPushButton`: botón de clic.
- `QLabel`: etiqueta de texto.
- `QLineEdit`: campo de entrada de texto.
- `QTextEdit`: editor de texto multilínea.
- `QComboBox`: lista desplegable.
- `QTableWidget`: tabla de datos.
- `QVBoxLayout`, `QHBoxLayout`, `QGridLayout`: layouts para organizar widgets.

## 7. Señales y slots

Qt usa el modelo de señales y slots para eventos. Una señal es un evento producido por un widget; un slot es la función que responde a ese evento.

Ejemplo:

```python
button.clicked.connect(self.on_button_clicked)

def on_button_clicked(self):
    print("El botón fue presionado")
```

Algunos eventos comunes:

- `clicked`: cuando se pulsa un botón.
- `textChanged`: cuando cambia el texto de un campo.
- `currentIndexChanged`: cuando cambia el elemento seleccionado en un combo box.
- `itemSelectionChanged`: cuando cambia la selección en una tabla.

## 8. Layouts y organización de la interfaz

Usar layouts evita posicionar widgets con coordenadas absolutas. Los layouts funcionan así:

- `QVBoxLayout`: organiza widgets en columna.
- `QHBoxLayout`: organiza widgets en fila.
- `QGridLayout`: organiza widgets en una cuadrícula.

Ejemplo:

```python
layout = QVBoxLayout()
layout.addWidget(label)
layout.addWidget(button)
widget.setLayout(layout)
```

## 9. Buenas prácticas con PyQt/PySide

- Separar la lógica de negocio de la interfaz gráfica.
- Validar los datos antes de guardarlos.
- Usar nombres claros para widgets y métodos.
- No bloquear el hilo principal con operaciones largas.
- Crear clases para cada ventana o página importante.
- Manejar errores de base de datos y de usuario.

## 10. Aplicación CRUD como ejemplo

Un CRUD básico de alumnos usa:

- `QLineEdit` para nombre y email.
- `QComboBox` para curso.
- `QSpinBox` para edad.
- `QTextEdit` para notas.
- `QTableWidget` para listar registros.
- `QPushButton` para guardar, editar y eliminar.

Este manual se complementa con el documento de QFluentWidgets, que explica cómo usar componentes modernos basados en Qt.
