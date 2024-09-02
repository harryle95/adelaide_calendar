from __future__ import annotations

from msgspec import field

from src.utils.schema import CamelizedBaseStruct

__all__ = (
    "Campus",
    "Career",
    "CourseSearch",
    "Subject",
    "Term",
)


class Career(CamelizedBaseStruct, dict=True):
    FIELDVALUE: str = field(name="value")
    XLATLONGNAME: str = field(name="name")


class Campus(CamelizedBaseStruct, dict=True):
    CAMPUS: str = field(name="name")
    DESCR: str = field(name="description")


class Subject(CamelizedBaseStruct):
    SUBJECT: str = field(name="name")
    DESCR: str = field(name="description")


class Term(CamelizedBaseStruct):
    TERM: str = field(name="id")
    DESCR: str = field(name="description")
    ACAD_YEAR: str = field(name="year")
    CURRENT: str = field(name="current")


class CourseSearch(CamelizedBaseStruct):
    COURSE_ID: str = field(name="courseId")
    COURSE_OFFER_NBR: str = field(name="courseOfferNumber")
    YEAR: str = field(name="year")
    TERM: str = field(name="term")
    TERM_DESCR: str = field(name="termDescription")
    SUBJECT: str = field(name="subject")
    CATALOG_NBR: str = field(name="catalogNumber")
    ACAD_CAREER: str = field(name="academicCareer")
    ACAD_CAREER_DESCR: str = field(name="academicDescription")
    COURSE_TITLE: str = field(name="courseTitle")
    UNITS: str = field(name="units")
    CAMPUS: str = field(name="campus")
    CLASS_NBR: str = field(name="classNumber")
