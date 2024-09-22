from enum import Enum

__all__ = ("ProxyURL",)


class ProxyURL(Enum):
    CAMPUS = "/proxy/campus"
    ACAD_CAREER = "/proxy/academicCareer"
    TERM = "/proxy/term"
    SUBJECT = "/proxy/subject"
    COURSE = "/proxy/course"
