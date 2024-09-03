from __future__ import annotations

from litestar.dto.config import DTOConfig
from litestar.dto.msgspec_dto import MsgspecDTO
from msgspec import Struct, field

__all__ = (
    "Campus",
    "Career",
    "ClassInfo",
    "CourseClassListDTO",
    "CourseDetail",
    "CourseDetailDTO",
    "CourseSearch",
    "CriticalDates",
    "Group",
    "Meetings",
    "Subject",
    "Term",
    "lower_camel",
)


def lower_camel(word: str) -> str:
    word = word.lower()
    return word.split("_")[0] + "".join(x.capitalize() or "_" for x in word.split("_")[1:])


class Career(Struct, rename=lower_camel):
    FIELDVALUE: str = field(name="value")
    XLATLONGNAME: str = field(name="name")


class Campus(Struct, rename=lower_camel):
    CAMPUS: str
    DESCR: str


class Subject(Struct, rename=lower_camel):
    SUBJECT: str
    DESCR: str


class Term(Struct, rename=lower_camel):
    TERM: str
    DESCR: str
    ACAD_YEAR: str
    CURRENT: str


class CourseSearch(Struct, rename=lower_camel):
    ACAD_CAREER: str
    ACAD_CAREER_DESCR: str
    CAMPUS: str
    CATALOG_NBR: str
    CLASS_NBR: str
    COURSE_ID: str
    COURSE_OFFER_NBR: str
    COURSE_TITLE: str
    SUBJECT: str
    YEAR: str
    TERM: str
    TERM_DESCR: str
    UNITS: str


class CriticalDates(Struct, rename=lower_camel):
    CENSUS_DT: str
    LAST_DAY: str
    LAST_DAY_TO_WF: str
    LAST_DAY_TO_WFN: str


class CourseDetail(CourseSearch):
    ASSESSMENT: str
    ASSUMED_KNOWLEDGE: str
    AVAILABLE_FOR_NON_AWARD_STUDY: str
    AVAILABLE_FOR_STUDY_ABROAD: str
    BIENNIAL_COURSE: str
    CAMPUS_CD: str
    CONTACT: str
    COUNTRY: str
    CO_REQUISITE: str
    CRITICAL_DATES: CriticalDates
    EFTLS: float
    INCOMPATIBLE: str
    PRE_REQUISITE: str
    QUOTA: str
    QUOTA_TXT: str
    RESTRICTION: str
    RESTRICTION_TXT: str
    SESSION_CD: str
    SYLLABUS: str
    URL: str


class CourseDetailDTO(MsgspecDTO[CourseDetail]):
    config = DTOConfig(rename_strategy=lower_camel)


class Meetings(Struct):
    dates: str
    days: str
    start_time: str
    end_time: str
    location: str


class ClassInfo(Struct):
    class_nbr: str
    section: str
    size: int
    enrolled: int
    available: int
    institution: str
    component: str
    meetings: list[Meetings]


class Group(Struct):
    type: str
    classes: list[ClassInfo]


class CourseClassListDTO(MsgspecDTO[Group]):
    config = DTOConfig(rename_strategy=lower_camel)
