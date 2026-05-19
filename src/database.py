from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Student:
    id: int | None
    name: str
    email: str
    course: str
    age: int
    notes: str


class StudentRepository:
    """Small SQLite repository used by the desktop CRUD."""

    def __init__(self, database_path: Path) -> None:
        self.database_path = database_path
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        self._create_schema()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        return connection

    def _create_schema(self) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL,
                    course TEXT NOT NULL,
                    age INTEGER NOT NULL,
                    notes TEXT NOT NULL DEFAULT '',
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

    def list_students(self, search: str = "", course: str = "Todos") -> list[Student]:
        query = "SELECT id, name, email, course, age, notes FROM students"
        clauses: list[str] = []
        params: list[object] = []

        if search:
            clauses.append("(LOWER(name) LIKE ? OR LOWER(email) LIKE ? OR LOWER(notes) LIKE ?)")
            pattern = f"%{search.lower()}%"
            params.extend([pattern, pattern, pattern])

        if course != "Todos":
            clauses.append("course = ?")
            params.append(course)

        if clauses:
            query += " WHERE " + " AND ".join(clauses)

        # Ordenar por id para mostrar los registros en el orden de insercion
        query += " ORDER BY id ASC"

        with self._connect() as connection:
            rows = connection.execute(query, params).fetchall()

        return [self._row_to_student(row) for row in rows]

    def create_student(self, student: Student) -> int:
        with self._connect() as connection:
            cursor = connection.execute(
                """
                INSERT INTO students (name, email, course, age, notes)
                VALUES (?, ?, ?, ?, ?)
                """,
                (student.name, student.email, student.course, student.age, student.notes),
            )
            return int(cursor.lastrowid)

    def update_student(self, student: Student) -> None:
        if student.id is None:
            raise ValueError("Cannot update a student without an id")

        with self._connect() as connection:
            connection.execute(
                """
                UPDATE students
                SET name = ?, email = ?, course = ?, age = ?, notes = ?
                WHERE id = ?
                """,
                (student.name, student.email, student.course, student.age, student.notes, student.id),
            )

    def delete_student(self, student_id: int) -> None:
        with self._connect() as connection:
            connection.execute("DELETE FROM students WHERE id = ?", (student_id,))

    @staticmethod
    def _row_to_student(row: sqlite3.Row) -> Student:
        return Student(
            id=int(row["id"]),
            name=str(row["name"]),
            email=str(row["email"]),
            course=str(row["course"]),
            age=int(row["age"]),
            notes=str(row["notes"]),
        )
