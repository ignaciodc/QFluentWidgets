from __future__ import annotations

import re
import sys
from pathlib import Path

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QAbstractItemView,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QSizePolicy,
    QHeaderView,
    QTableWidget,
    QTableWidgetItem,
    QTextBrowser,
    QVBoxLayout,
)
from qfluentwidgets import (
    BodyLabel,
    CardWidget,
    ComboBox,
    FluentIcon as FIF,
    FluentWindow,
    InfoBar,
    InfoBarPosition,
    LineEdit,
    MessageBox,
    NavigationItemPosition,
    PrimaryPushButton,
    PushButton,
    SearchLineEdit,
    SpinBox,
    StrongBodyLabel,
    SubtitleLabel,
    SwitchButton,
    TextEdit,
    Theme,
    TitleLabel,
    setTheme,
)

from database import Student, StudentRepository


COURSES = ["Python", "Bases de datos", "Interfaces", "Programacion", "Sistemas"]
EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def is_system_dark_mode() -> bool:
    if sys.platform != "win32":
        return False

    try:
        import winreg

        with winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize",
        ) as key:
            value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
            return value == 0
    except Exception:
        return False


class StudentsPage(QFrame):
    def __init__(self, repository: StudentRepository) -> None:
        super().__init__()
        self.repository = repository
        self.selected_student_id: int | None = None
        self.setObjectName("studentsPage")

        self.title = TitleLabel("Alumnos")
        self.subtitle = BodyLabel("CRUD con QFluentWidgets, PyQt5 y SQLite")

        self.name_input = LineEdit()
        self.name_input.setPlaceholderText("Nombre completo")

        self.email_input = LineEdit()
        self.email_input.setPlaceholderText("correo@ejemplo.com")

        self.course_input = ComboBox()
        self.course_input.addItems(COURSES)

        self.age_input = SpinBox()
        self.age_input.setRange(14, 99)
        self.age_input.setValue(18)

        self.notes_input = TextEdit()
        self.notes_input.setPlaceholderText("Observaciones")
        self.notes_input.setFixedHeight(96)

        self.save_button = PrimaryPushButton(FIF.SAVE, "Guardar")
        self.new_button = PushButton(FIF.ADD, "Nuevo")
        self.delete_button = PushButton(FIF.DELETE, "Eliminar")
        self.delete_button.setEnabled(False)

        self.search_input = SearchLineEdit()
        self.search_input.setPlaceholderText("Buscar por nombre, email o notas")

        self.filter_input = ComboBox()
        self.filter_input.addItems(["Todos", *COURSES])

        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(["ID", "Nombre", "Email", "Curso", "Edad"])
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)

        self._build_layout()
        self._connect_signals()
        self.refresh_table()

    def _build_layout(self) -> None:
        page_layout = QVBoxLayout(self)
        page_layout.setContentsMargins(28, 28, 28, 28)
        page_layout.setSpacing(18)
        page_layout.addWidget(self.title)
        page_layout.addWidget(self.subtitle)

        form_card = CardWidget()
        form_card.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        form_card.setMaximumWidth(380)
        form_card.setMaximumHeight(420)
        form_layout = QGridLayout(form_card)
        form_layout.setContentsMargins(8, 8, 8, 8)
        form_layout.setHorizontalSpacing(10)
        form_layout.setVerticalSpacing(6)

        form_layout.addWidget(StrongBodyLabel("Datos del alumno"), 0, 0, 1, 2)
        form_layout.addWidget(BodyLabel("Nombre"), 1, 0)
        form_layout.addWidget(self.name_input, 1, 1)
        form_layout.addWidget(BodyLabel("Email"), 2, 0)
        form_layout.addWidget(self.email_input, 2, 1)
        form_layout.addWidget(BodyLabel("Curso"), 3, 0)
        form_layout.addWidget(self.course_input, 3, 1)
        form_layout.addWidget(BodyLabel("Edad"), 4, 0)
        form_layout.addWidget(self.age_input, 4, 1)
        form_layout.addWidget(BodyLabel("Notas"), 5, 0, Qt.AlignTop)
        form_layout.addWidget(self.notes_input, 5, 1)

        button_row = QHBoxLayout()
        button_row.addWidget(self.save_button)
        button_row.addWidget(self.new_button)
        button_row.addStretch()
        form_layout.addLayout(button_row, 6, 1)

        table_card = CardWidget()
        table_card.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        table_layout = QVBoxLayout(table_card)
        table_layout.setContentsMargins(18, 18, 18, 18)
        table_layout.setSpacing(12)

        filter_row = QHBoxLayout()
        filter_row.addWidget(self.search_input, 1)
        filter_row.addWidget(self.filter_input)
        filter_row.addWidget(self.delete_button)
        table_layout.addLayout(filter_row)
        table_layout.addWidget(self.table)

        # Colocar el formulario a la izquierda y la lista a la derecha
        main_row = QHBoxLayout()
        main_row.setSpacing(18)
        main_row.addWidget(form_card)
        main_row.addWidget(table_card, 1)
        main_row.setStretch(0, 0)
        main_row.setStretch(1, 1)
        page_layout.addLayout(main_row)

    def _connect_signals(self) -> None:
        self.save_button.clicked.connect(self.save_student)
        self.new_button.clicked.connect(self.clear_form)
        self.delete_button.clicked.connect(self.confirm_delete)
        self.search_input.textChanged.connect(self.refresh_table)
        self.filter_input.currentTextChanged.connect(self.refresh_table)
        self.table.itemSelectionChanged.connect(self.load_selected_student)

    def refresh_table(self) -> None:
        students = self.repository.list_students(
            search=self.search_input.text().strip(),
            course=self.filter_input.currentText(),
        )

        self.table.setRowCount(len(students))
        for row_index, student in enumerate(students):
            values = [student.id, student.name, student.email, student.course, student.age]
            for column_index, value in enumerate(values):
                item = QTableWidgetItem(str(value))
                item.setData(Qt.UserRole, student)
                if column_index in (0, 4):
                    item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row_index, column_index, item)

    def load_selected_student(self) -> None:
        selected_items = self.table.selectedItems()
        if not selected_items:
            return

        student = selected_items[0].data(Qt.UserRole)
        if not isinstance(student, Student):
            return

        self.selected_student_id = student.id
        self.name_input.setText(student.name)
        self.email_input.setText(student.email)
        self.course_input.setCurrentText(student.course)
        self.age_input.setValue(student.age)
        self.notes_input.setPlainText(student.notes)
        self.delete_button.setEnabled(True)

    def save_student(self) -> None:
        student = self._student_from_form()
        if student is None:
            return

        if self.selected_student_id is None:
            new_id = self.repository.create_student(student)
            self.selected_student_id = new_id
            self._show_success("Alumno creado", "El registro se ha anadido correctamente.")
        else:
            student.id = self.selected_student_id
            self.repository.update_student(student)
            self._show_success("Alumno actualizado", "Los cambios se han guardado correctamente.")

        self.refresh_table()
        self.clear_form()

    def confirm_delete(self) -> None:
        if self.selected_student_id is None:
            return

        dialog = MessageBox(
            "Eliminar alumno",
            "Esta accion borrara el registro seleccionado. Quieres continuar?",
            self.window(),
        )

        if dialog.exec():
            self.repository.delete_student(self.selected_student_id)
            self._show_success("Alumno eliminado", "El registro se ha borrado correctamente.")
            self.refresh_table()
            self.clear_form()

    def clear_form(self) -> None:
        self.selected_student_id = None
        self.table.clearSelection()
        self.name_input.clear()
        self.email_input.clear()
        self.course_input.setCurrentIndex(0)
        self.age_input.setValue(18)
        self.notes_input.clear()
        self.delete_button.setEnabled(False)
        self.name_input.setFocus()

    def _student_from_form(self) -> Student | None:
        name = self.name_input.text().strip()
        email = self.email_input.text().strip()
        course = self.course_input.currentText()
        age = int(self.age_input.value())
        notes = self.notes_input.toPlainText().strip()

        if not name:
            self._show_error("Falta el nombre", "Introduce el nombre completo del alumno.")
            return None

        if not EMAIL_PATTERN.match(email):
            self._show_error("Email no valido", "Introduce un correo electronico correcto.")
            return None

        return Student(
            id=self.selected_student_id,
            name=name,
            email=email,
            course=course,
            age=age,
            notes=notes,
        )

    def _show_success(self, title: str, content: str) -> None:
        InfoBar.success(
            title=title,
            content=content,
            parent=self.window(),
            position=InfoBarPosition.TOP_RIGHT,
            duration=2500,
        )

    def _show_error(self, title: str, content: str) -> None:
        InfoBar.error(
            title=title,
            content=content,
            parent=self.window(),
            position=InfoBarPosition.TOP_RIGHT,
            duration=3500,
        )


class ManualPage(QFrame):
    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("manualPage")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 28, 28, 28)
        layout.setSpacing(16)

        layout.addWidget(TitleLabel("Como crear un proyecto con PyQt5 y QFluentWidgets"))

        self.markdown_view = QTextBrowser(self)
        self.markdown_view.setOpenExternalLinks(True)
        self.markdown_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.markdown_view.setMinimumWidth(720)
        self.markdown_view.setStyleSheet("background: transparent; border: none;")

        markdown_path = Path(__file__).resolve().parents[1] / "docs" / "manual_crear_proyecto.md"
        try:
            markdown_text = markdown_path.read_text(encoding="utf-8")
            self.markdown_view.setMarkdown(markdown_text)
        except Exception:
            self.markdown_view.setPlainText("No se pudo cargar el manual desde docs/manual_crear_proyecto.md.")

        layout.addWidget(self.markdown_view, 1)


class SummaryPage(QFrame):
    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("summaryPage")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 28, 28, 28)
        layout.setSpacing(16)

        layout.addWidget(TitleLabel("Resumen de la práctica"))
        layout.addWidget(SubtitleLabel("Información y recursos"))

        card = CardWidget()
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(18, 18, 18, 18)
        card_layout.setSpacing(10)
        card_layout.addWidget(BodyLabel("Esta aplicación usa PyQt5 como binding de Qt."))
        card_layout.addWidget(BodyLabel("QFluentWidgets aporta componentes modernos de estilo Fluent Design."))
        card_layout.addWidget(BodyLabel("SQLite guarda los datos en un fichero local sin servidor."))
        card_layout.addWidget(BodyLabel("Manuales disponibles en la carpeta docs:"))
        card_layout.addWidget(BodyLabel("• docs/manual_crear_proyecto.md"))
        card_layout.addWidget(BodyLabel("• docs/manual_python_librerias_PyQt_PySide.md"))
        card_layout.addWidget(BodyLabel("• docs/manual_qfluentwidgets.md"))

        layout.addWidget(card)
        layout.addStretch()


class SettingsPage(QFrame):
    def __init__(self, initial_theme: Theme) -> None:
        super().__init__()
        self.setObjectName("settingsPage")

        self.theme_switch = SwitchButton("Modo oscuro")
        self.theme_switch.setChecked(initial_theme == Theme.DARK)
        self.theme_switch.checkedChanged.connect(self.change_theme)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 28, 28, 28)
        layout.setSpacing(18)
        layout.addWidget(TitleLabel("Ajustes"))
        layout.addWidget(self.theme_switch)
        layout.addStretch()

    def change_theme(self, checked: bool) -> None:
        setTheme(Theme.DARK if checked else Theme.LIGHT)


class MainWindow(FluentWindow):
    def __init__(self, initial_theme: Theme) -> None:
        super().__init__()
        database_path = Path(__file__).resolve().parents[1] / "data" / "academia.db"
        repository = StudentRepository(database_path)

        self.students_page = StudentsPage(repository)
        self.manual_page = ManualPage()
        self.summary_page = SummaryPage()
        self.settings_page = SettingsPage(initial_theme)

        self.addSubInterface(self.students_page, FIF.PEOPLE, "Alumnos")
        self.addSubInterface(self.manual_page, FIF.DOCUMENT, "Manual")
        self.addSubInterface(self.summary_page, FIF.DOCUMENT, "Resumen")
        self.addSubInterface(
            self.settings_page,
            FIF.SETTING,
            "Ajustes",
            position=NavigationItemPosition.BOTTOM,
        )

        self.setWindowTitle("Academia Fluent")
        self.resize(1100, 760)


def main() -> int:
    app = QApplication(sys.argv)
    system_theme = Theme.DARK if is_system_dark_mode() else Theme.LIGHT
    setTheme(system_theme)
    window = MainWindow(system_theme)
    window.show()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
