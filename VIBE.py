#Patrick Martinez
#CIS216
#WK10 VIBE Coding

"""Student record manager with test scores and grade calculations."""

import csv
import sys
import termios
import tty
from dataclasses import dataclass, field
from pathlib import Path


DATA_FILE = Path("student_grades.txt")


@dataclass
class Student:
    name: str
    id: str
    test_scores: list[float]
    average: float = field(init=False)
    grade: str = field(init=False)

    def __post_init__(self) -> None:
        self.average = sum(self.test_scores) / 3
        if self.average >= 90:
            self.grade = "A"
        elif self.average >= 80:
            self.grade = "B"
        elif self.average >= 70:
            self.grade = "C"
        elif self.average >= 60:
            self.grade = "D"
        else:
            self.grade = "F"


def load_students(file_path: Path = DATA_FILE) -> list[Student]:
    """Load pipe-delimited records from the text file when it exists."""
    if not file_path.exists():
        return []

    students = []
    try:
        with file_path.open(newline="", encoding="utf-8") as file:
            for row in csv.reader(file, delimiter="|"):
                if len(row) != 7:
                    raise ValueError("each record must contain seven pipe-delimited fields")
                students.append(
                    Student(
                        row[0],
                        row[1],
                        [float(row[2]), float(row[3]), float(row[4])],
                    )
                )
    except (OSError, KeyError, TypeError, ValueError) as error:
        print(f"Could not load saved records: {error}")
    return students


def save_students(students: list[Student], file_path: Path = DATA_FILE) -> bool:
    """Save records as name|id|test1|test2|test3|average|grade."""
    try:
        with file_path.open("w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file, delimiter="|", lineterminator="\n")
            for student in students:
                writer.writerow(
                    [
                        student.name,
                        student.id,
                        *[f"{score:.2f}" for score in student.test_scores],
                        f"{student.average:.2f}",
                        student.grade,
                    ]
                )
    except OSError as error:
        print(f"Could not save student records: {error}")
        return False
    return True


def read_score(test_number: int) -> float:
    while True:
        try:
            score = float(input(f"Test {test_number} score (0-100): "))
            if 0 <= score <= 100:
                return score
        except ValueError:
            pass
        print("Please enter a number from 0 through 100.")


def add_student(students: list[Student]) -> None:
    name = input("Student name: ").strip()
    student_id = input("Student ID: ").strip()
    if not name or not student_id:
        print("Name and ID cannot be blank.")
        return
    if any(student.id == student_id for student in students):
        print("A student with that ID already exists.")
        return

    scores = [read_score(test_number) for test_number in range(1, 4)]
    student = Student(name, student_id, scores)
    students.append(student)
    print(f"Added {name}: average {student.average:.2f}, grade {student.grade}")


def display_table(students: list[Student]) -> None:
    if not students:
        print("No student records found.")
        return
    headers = ["Name", "Student ID", "Test 1", "Test 2", "Test 3", "Average", "Grade"]
    rows = [
        [
            student.name,
            student.id,
            *[f"{score:.2f}" for score in student.test_scores],
            f"{student.average:.2f}",
            student.grade,
        ]
        for student in sorted(students, key=lambda item: item.name.lower())
    ]
    widths = [max(len(str(value)) for value in column) for column in zip(headers, *rows)]
    print(" | ".join(f"{header:<{width}}" for header, width in zip(headers, widths)))
    print("-+-".join("-" * width for width in widths))
    for row in rows:
        print(" | ".join(f"{value:<{width}}" for value, width in zip(row, widths)))


def display_statistics(students: list[Student]) -> None:
    if not students:
        print("No student records found.")
        return
    averages = [student.average for student in students]
    highest = max(students, key=lambda student: student.average)
    lowest = min(students, key=lambda student: student.average)
    print(f"Highest average: {highest.average:.2f} ({highest.name})")
    print(f"Lowest average: {lowest.average:.2f} ({lowest.name})")
    print(f"Class average: {sum(averages) / len(averages):.2f}")


def search_students(students: list[Student]) -> None:
    search_term = input("Enter student name to search: ").strip().lower()
    matches = [student for student in students if search_term in student.name.lower()]
    if matches:
        display_table(matches)
    else:
        print("No students matched that name.")


def read_menu_choice() -> str:
    """Read one menu key so ESC can exit immediately in an interactive terminal."""
    if sys.stdin.isatty() and sys.stdout.isatty():
        file_descriptor = sys.stdin.fileno()
        settings = termios.tcgetattr(file_descriptor)
        try:
            tty.setraw(file_descriptor)
            choice = sys.stdin.read(1)
            print(choice if choice != "\x1b" else "ESC")
            return choice
        finally:
            termios.tcsetattr(file_descriptor, termios.TCSADRAIN, settings)
    return input("Choose an option (ESC to exit): ").strip()


def main() -> None:
    students = load_students()
    while True:
        print("\nStudent Record Manager")
        print("1. Add student")
        print("2. Display all students")
        print("3. Display class statistics")
        print("4. Search by student name")
        print("Press ESC to save and exit")
        choice = read_menu_choice()

        if choice == "\x1b":
            if save_students(students):
                print("Records saved. Goodbye!")
            else:
                print("The program is exiting, but the records could not be saved.")
            return
        actions = {"1": add_student, "2": display_table, "3": display_statistics, "4": search_students}
        action = actions.get(choice)
        if action is None:
            print("Please choose 1, 2, 3, 4, or press ESC.")
        else:
            action(students)


if __name__ == "__main__":
    main()
