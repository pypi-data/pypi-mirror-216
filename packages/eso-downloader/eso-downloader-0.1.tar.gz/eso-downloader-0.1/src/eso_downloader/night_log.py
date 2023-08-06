"""
Helper tools and functions for parsing the night log file produced for ESO
observations.
"""
from enum import Enum
import re

from attrs import define, field

GRADE_RE = re.compile(r"Grade:\s+(?P<grade>A|B|C|D|X|_)")


class Grade(Enum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"
    X = "X"
    _ = "_"
    NOT_FOUND = None


COMPLETED = {
    Grade.A,  # Completed, in constraints
    Grade.B,  # Completed, partially in constraints
    Grade.D,  # Completed, not in constraints, but won't be reobserved
}
ACCEPTABLE = {
    Grade.A,
    Grade.B,
}


@define
class NightLog:
    grade = field(converter=Grade)

    @classmethod
    def from_str(cls, s):
        match = GRADE_RE.search(s)
        if match is None:
            grade = None
        else:
            grade = match["grade"]
        return cls(grade=grade)

    @classmethod
    def from_file(cls, file):
        return cls.from_str(file.read())

    @classmethod
    def from_path(cls, path):
        with open(path, encoding="utf-8") as file:
            return cls.from_file(file)

    @property
    def is_completed(self):
        return self.grade in COMPLETED

    @property
    def is_acceptable(self):
        return self.grade in ACCEPTABLE
