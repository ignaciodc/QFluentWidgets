# Manual de construcción de la aplicación desde `main.py`

Este manual explica cómo se ha creado la aplicación paso a paso, con foco en cada sección de la interfaz y cómo encaja en el proyecto.

## Índice

1. [¿Qué hace este proyecto?](#1-qué-hace-este-proyecto)
2. [Archivos principales](#2-archivos-principales)
3. [Importaciones y constantes](#3-importaciones-y-constantes)
4. [Detectar el tema oscuro del sistema](#4-detectar-el-tema-oscuro-del-sistema)
5. [Página de alumnos: `StudentsPage`](#5-página-de-alumnos-studentspage)
6. [Página "Manual": `AboutPage`](#6-página-manual-aboutpage)
7. [Página de ajustes: `SettingsPage`](#7-página-de-ajustes-settingspage)
8. [Ventana principal: `MainWindow`](#8-ventana-principal-mainwindow)
9. [Punto de entrada: `main()`](#9-punto-de-entrada-main)
10. [Cómo añadir una nueva página](#10-cómo-añadir-una-nueva-página)
11. [Cómo leer este código si no sabes nada](#11-cómo-leer-este-código-si-no-sabes-nada)
12. [Consejos para crear una aplicación parecida](#12-consejos-para-crear-una-aplicación-parecida)
13. [Resumen breve](#13-resumen-breve)

---

## 1. ¿Qué hace este proyecto?

La aplicación es una ventana de escritorio que contiene varias secciones:

- una página de `Alumnos` con formulario y lista,
- una página de `Manual` con información,
- una página de `Ajustes` para cambiar el tema.

La idea es mostrar cómo se organiza una aplicación con `PyQt5` y `QFluentWidgets`.

---

## 2. Archivos principales

- `src/main.py`: crea la ventana y define todas las páginas.
- `src/database.py`: guarda los datos de los alumnos en SQLite.

---

## 3. Primera parte: importaciones y constantes

En `src/main.py` se prepara todo lo necesario antes de crear la ventana.

### 3.1 Importaciones básicas

- `sys`, `re`, `Path` son utilidades generales de Python.
- `QApplication`, `QFrame`, `QVBoxLayout`, `QTableWidget`, etc., vienen de `PyQt5`.
- Los widgets modernos como `CardWidget`, `FluentWindow`, `LineEdit`, `ComboBox`, `SwitchButton`, `InfoBar` y `MessageBox` vienen de `qfluentwidgets`.

### 3.2 Constantes

- `COURSES`: define los nombres de los cursos usados en los menús.
- `EMAIL_PATTERN`: expresión regular para validar si un email tiene formato correcto.

Estas constantes se usan después para crear formularios y validaciones.

---

## 4. Detectar el tema oscuro del sistema

Se crea una función llamada `is_system_dark_mode()`.

- Comprueba si el sistema operativo es Windows.
- Lee el valor `AppsUseLightTheme` del registro de Windows.
- Si el valor es `0`, significa que Windows está en modo oscuro.

Esto permite que la aplicación abra con un tema visual que coincide con el sistema.

---

## 5. Página de alumnos: `StudentsPage`

`StudentsPage` es la parte más grande de la aplicación. Es una clase que hereda de `QFrame` y monta toda la interfaz de la sección "Alumnos".

### 5.1 Inicio de la página

Dentro de `__init__()` se hacen estas tareas:

- se guarda una referencia a `repository` para acceder a los datos.
- se crea una variable para el ID del alumno seleccionado.
- se define el nombre del objeto con `setObjectName("studentsPage")`.
- se crean los controles del formulario y la tabla.
- se construye el diseño con `_build_layout()`.
- se conectan los botones y campos con `_connect_signals()`.
- se carga la tabla inicial llamando a `refresh_table()`.

### 5.2 Crear los campos del formulario

Se añaden controles visuales uno por uno:

- `name_input = LineEdit()` para el nombre.
- `email_input = LineEdit()` para el email.
- `course_input = ComboBox()` y luego `addItems(COURSES)` para el curso.
- `age_input = SpinBox()` con rango `14` a `99`.
- `notes_input = TextEdit()` para notas.

Cada control recibe también texto de ayuda, como `setPlaceholderText()`.

### 5.3 Crear los botones

Se crean tres botones:

- `PrimaryPushButton(FIF.SAVE, "Guardar")` para guardar cambios.
- `PushButton(FIF.ADD, "Nuevo")` para limpiar el formulario.
- `PushButton(FIF.DELETE, "Eliminar")` para borrar el registro.

El botón de eliminar se inicia desactivado con `setEnabled(False)` porque no hay selección al principio.

### 5.4 Crear filtros y tabla

- `search_input = SearchLineEdit()` para buscar alumnos.
- `filter_input = ComboBox()` con los cursos más la opción `Todos`.
- `table = QTableWidget(0, 5)` para mostrar la lista de alumnos.

La tabla se configura para:

- no permitir edición directa,
- seleccionar filas completas,
- ajustar el ancho de las columnas de forma razonable.

### 5.5 Diseñar la página

El método `_build_layout()` organiza los widgets.

Pasos:

1. Crear un `QVBoxLayout` principal para toda la página.
2. Añadir un título y un subtítulo.
3. Construir un `CardWidget` para el formulario.
4. Colocar labels y controles en una cuadrícula (`QGridLayout`).
5. Añadir un `QHBoxLayout` con los botones del formulario.
6. Construir otro `CardWidget` para la tabla y los filtros.
7. Colocar el formulario y la tabla en un `QHBoxLayout` horizontal.

Este diseño da una apariencia dividida: formulario a la izquierda y tabla a la derecha.

### 5.6 Conectar acciones con eventos

El método `_connect_signals()` vincula cada evento a una función:

- `save_button.clicked` llama a `save_student()`.
- `new_button.clicked` llama a `clear_form()`.
- `delete_button.clicked` llama a `confirm_delete()`.
- `search_input.textChanged` y `filter_input.currentTextChanged` llaman a `refresh_table()`.
- `table.itemSelectionChanged` llama a `load_selected_student()`.

Así, cada interacción del usuario tiene una respuesta.

### 5.7 Crear métodos específicos

La clase define varios métodos que son bloques pequeños de trabajo:

- `refresh_table()`: repinta la tabla con los datos actuales.
- `load_selected_student()`: rellena el formulario cuando se selecciona una fila.
- `save_student()`: guarda el alumno nuevo o actualiza el existente.
- `confirm_delete()`: muestra un cuadro de confirmación antes de borrar.
- `clear_form()`: restablece el formulario.
- `_student_from_form()`: toma los valores de los campos y crea un objeto `Student`.
- `_show_success()` y `_show_error()`: muestran avisos de estado.

Estas funciones organizan el código en partes pequeñas y fáciles de entender.

---

## 6. Página "Manual": `AboutPage`

`AboutPage` es una página simple que informa al usuario sobre la aplicación.

### 6.1 Estructura de la página

- Hereda de `QFrame`.
- Usa un `QVBoxLayout` para colocar widgets verticalmente.
- Añade un título `TitleLabel` y un subtítulo `SubtitleLabel`.
- Crea un `CardWidget` con `BodyLabel` para mostrar texto explicativo.

### 6.2 Propósito

Esta página no tiene lógica compleja. Su función es mostrar texto estático de resumen.

---

## 7. Página de ajustes: `SettingsPage`

`SettingsPage` permite cambiar el tema de la aplicación.

### 7.1 Crear el interruptor de tema

- Se crea un `SwitchButton("Modo oscuro")`.
- Se marca como activo si el tema inicial es oscuro.
- Se conecta `checkedChanged` a `change_theme()`.

### 7.2 Cambiar el tema

`change_theme(checked)` llama a `setTheme()` con `Theme.DARK` o `Theme.LIGHT`.

Esto actualiza la apariencia de toda la ventana en tiempo real.

---

## 8. Ventana principal: `MainWindow`

`MainWindow` es la clase que agrupa todas las páginas en una sola ventana.

### 8.1 Heredar de `FluentWindow`

La ventana principal usa `FluentWindow`, que viene de `QFluentWidgets` y ya trae el estilo visual.

### 8.2 Crear la base de datos y el repositorio

Dentro de `__init__()` se hace:

- `database_path = Path(__file__).resolve().parents[1] / "data" / "academia.db"`
- `repository = StudentRepository(database_path)`

Esto garantiza que el directorio `data/` exista y que la base de datos se cree automáticamente.

### 8.3 Crear las páginas

Se instancian las tres páginas:

- `StudentsPage(repository)`
- `AboutPage()`
- `SettingsPage(initial_theme)`

### 8.4 Añadir las subinterfaces

Se usan `addSubInterface()` para incorporar cada página al menú lateral:

- `Alumnos` con icono `FIF.PEOPLE`
- `Manual` con icono `FIF.DOCUMENT`
- `Ajustes` con icono `FIF.SETTING`, colocado en la parte inferior

### 8.5 Ajustes finales

- `setWindowTitle("Academia Fluent")`
- `resize(1100, 760)`

Así se define el título y el tamaño de la ventana al abrirla.

---

## 9. Punto de entrada: `main()`

La función `main()` arranca la aplicación.

Pasos:

1. Crear `QApplication(sys.argv)`.
2. Definir `system_theme` usando `is_system_dark_mode()`.
3. Aplicar el tema con `setTheme(system_theme)`.
4. Crear `window = MainWindow(system_theme)`.
5. Mostrar la ventana con `window.show()`.
6. Ejecutar el bucle de eventos con `app.exec()`.

Esta es la parte que convierte el código en una aplicación en ejecución.

---

## 10. Cómo añadir una nueva página

Para crear una nueva sección similar a `AboutPage` o `SettingsPage`:

1. Crear una clase que herede de `QFrame`.
2. Configurar su layout en `__init__()`.
3. Añadir widgets con `QVBoxLayout`, `CardWidget`, `TitleLabel`, etc.
4. Instanciarla en `MainWindow`.
5. Llamar a `addSubInterface()` para mostrarla en el menú.

Esto es el patrón básico para ampliar la aplicación.

---

## 11. Cómo leer este código si no sabes nada

Si nunca has usado `PyQt5`, piensa en estas partes:

- `QApplication`: es el motor que hace que la ventana funcione.
- `QFrame`: es un contenedor donde pones botones y campos.
- `QVBoxLayout` / `QHBoxLayout`: son las reglas para ordenar los componentes.
- `LineEdit`, `ComboBox`, `PushButton`: son los controles que el usuario usa.
- `connect(...)`: une un botón o campo con la acción que debe ejecutar.

En `main.py` se usa este patrón varias veces para construir cada pantalla.

---

## 12. Consejos para crear una aplicación parecida

1. Decide cuántas páginas quieres.
2. Para cada página, crea una clase que herede de `QFrame`.
3. Haz un método de diseño que coloque los controles.
4. Separa la lógica de los datos (aquí se usa `StudentRepository`).
5. Usa `addSubInterface()` en una ventana principal para unirlas.

Con esos pasos tendrás una aplicación modular y fácil de extender.

---

## 13. Resumen breve

- `main.py` crea la ventana y organiza las páginas.
- `StudentsPage` construye el formulario y la lista.
- `AboutPage` muestra información estática.
- `SettingsPage` cambia el tema.
- `MainWindow` une todo en un menú.
- `main()` inicia la aplicación.

Este manual está pensado para que alguien que empieza pueda entender cómo construir una aplicación similar leyendo cada parte.

---

## 14. Pasos rápidos para crear una aplicación similar

1. Crea un nuevo archivo `main.py`.
2. Importa `QApplication`, layouts y widgets de `PyQt5`.
3. Usa `qfluentwidgets` si quieres un estilo moderno y visualmente atractivo.
4. Crea una clase para cada pantalla, heredando de `QFrame`.
5. Dentro de cada clase, monta un layout con controles y tarjetas.
6. Crea una ventana principal que agrupe las páginas con `addSubInterface()`.
7. Inicializa `QApplication` y muestra la ventana en `main()`.
8. Si quieres datos persistentes, añade una clase de repositorio para SQLite.

Con estos pasos tendrás la estructura básica para una aplicación de escritorio multipágina.
