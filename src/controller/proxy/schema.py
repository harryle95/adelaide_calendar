from __future__ import annotations

from src.utils.schema import CamelizedBaseStruct

__all__ = (
    "Campus",
    "Career",
    "CourseSearch",
    "Subject",
    "Term",
)


CAREER_MAPPING = {"FIELDVALUE": "value", "XLATLONGNAME": "name"}
CAMPUS_MAPPING = {"CAMPUS": "name", "DESCR": "description"}
SUBJECT_MAPPING = {"SUBJECT": "name", "DESCR": "description"}
TERM_MAPPING = {
    "TERM": "id",
    "DESCR": "description",
    "ACAD_YEAR": "year",
    "CURRENT": "current",
}
COURSE_SEARCH_MAPPING = {
    "COURSE_ID": "course_id",
    "COURSE_OFFER_NBR": "course_offer_number",
    "YEAR": "year",
    "TERM": "term",
    "TERM_DESCR": "term_description",
    "SUBJECT": "subject",
    "CATALOG_NBR": "catalog_number",
    "ACAD_CAREER": "academic_career",
    "ACAD_CAREER_DESCR": "academic_description",
    "COURSE_TITLE": "course_title",
    "UNITS": "units",
    "CAMPUS": "campus",
    "CLASS_NBR": "class_number",
}


class Career(CamelizedBaseStruct):
    value: str
    name: str


class Campus(CamelizedBaseStruct):
    name: str
    description: str


class Subject(CamelizedBaseStruct):
    name: str
    description: str


class Term(CamelizedBaseStruct):
    id: str
    description: str
    year: str
    current: bool


class CourseSearch(CamelizedBaseStruct):
    course_id: str
    course_offer_number: str
    year: str
    term: str
    term_description: str
    subject: str
    catalog_number: str
    academic_career: str
    academic_description: str
    course_title: str
    units: int
    campus: str
    class_number: int
