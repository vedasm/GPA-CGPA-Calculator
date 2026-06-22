from typing import List, Dict, Tuple

GRADE_POINTS: Dict[str, int] = {
    "O": 10,
    "A+": 9,
    "A": 8,
    "B+": 7,
    "B": 6,
    "C": 5,
    "P": 4,
    "F": 0,
}

class Subject:
    def __init__(self, name: str, credits: int, grade: str):
        self.name = name
        self.credits = credits
        self.grade = grade
class Semester:
    def __init__(self, semester_no, gpa, credits):
        self.semester_no = semester_no
        self.gpa = gpa
        self.credits = credits


def get_grade_point(grade: str) -> int:
    return GRADE_POINTS.get((grade or "").strip().upper(), -1)


def calculate_gpa(subjects: List[Subject]) -> Tuple[float, int]:
    total_credits = 0
    total_points = 0

    if not subjects:
        return 0.0, 0

    for subject in subjects:
        if not subject.name.strip():
            raise ValueError("Subject name cannot be empty.")
        if subject.credits <= 0:
            raise ValueError(f"Credits for '{subject.name}' must be greater than 0.")

        gp = get_grade_point(subject.grade)
        if gp == -1:
            raise ValueError(f"Invalid grade '{subject.grade}' for subject '{subject.name}'.")

        total_credits += subject.credits
        total_points += subject.credits * gp

    return round(total_points / total_credits, 2), total_credits


def calculate_cgpa(semesters: List[Semester]) -> Tuple[float, int]:
    total_credits = 0
    weighted_sum = 0.0

    if not semesters:
        return 0.0, 0

    for sem in semesters:
        if sem.semester_no <= 0:
            raise ValueError("Semester number must be positive.")
        if sem.credits <= 0:
            raise ValueError(f"Credits for semester {sem.semester_no} must be greater than 0.")
        if sem.gpa < 0 or sem.gpa > 10:
            raise ValueError(f"GPA for semester {sem.semester_no} must be between 0 and 10.")

        total_credits += sem.credits
        weighted_sum += sem.gpa * sem.credits

    return round(weighted_sum / total_credits, 2), total_credits


def cgpa_to_percentage(cgpa: float) -> float:
    return round(cgpa * 10, 2)
