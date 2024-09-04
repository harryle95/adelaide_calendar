from enum import Enum

__all__ = ("ProxyURL",)


class ProxyURL(Enum):
    CAMPUS = "/proxy/campus"
    ACADEMIC_CAREER = "/proxy/academicCareer"
    TERM = "/proxy/term"
    SUBJECT = "/proxy/subject"
    COURSE = "/proxy/course"
    COURSE_DETAIL = "/proxy/courseDetail"
    COURSE_CLASS_LIST = "/proxy/courseClassList"
