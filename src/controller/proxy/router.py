from collections.abc import Sequence

from litestar import Controller, get

from src.controller.proxy.schema import Campus, Career, CourseSearch, Subject, Term
from src.controller.proxy.services import ProxyQueryService
from src.controller.proxy.urls import ProxyURL

__all__ = ("ProxyController",)


class ProxyController(Controller):
    """Proxy Controller"""

    tags = ["Proxy Controller"]
    dto = None
    return_dto = None
    exclude_from_auth = True

    @get(
        operation_id="GetCampusInfo",
        name="proxy:campus",
        summary="Get Campus Information",
        description="Get Campus Information",
        path=ProxyURL.CAMPUS.value,
        exclude_from_auth=True,
    )
    async def get_campus_info(self) -> Sequence[Campus]:
        return await ProxyQueryService.campus()

    @get(
        operation_id="GetAcademicLevelInfo",
        name="proxy:academicCareer",
        summary="Get Academic Level Info",
        description="Get Academic Level Info",
        path=ProxyURL.ACADEMIC_CAREER.value,
        exclude_from_auth=True,
    )
    async def get_academic_career_info(self) -> Sequence[Career]:
        return await ProxyQueryService.academic_career()

    @get(
        operation_id="GetTermInfo",
        name="proxy:term",
        summary="Get Term Info",
        description="Get Term Info",
        path=ProxyURL.TERM.value,
        exclude_from_auth=True,
    )
    async def get_term_info(self) -> Sequence[Term]:
        return await ProxyQueryService.term()

    @get(
        operation_id="GetSubjectInfo",
        name="proxy:subjects",
        summary="Get Subject Info",
        description="Get Subject Info",
        path=ProxyURL.SUBJECT.value,
        exclude_from_auth=True,
    )
    async def get_subject_info(self) -> Sequence[Subject]:
        return await ProxyQueryService.subjects()

    @get(
        operation_id="GetCourseInfo",
        name="proxy:course",
        summary="Get Course Info",
        description="Get Course Info",
        path=ProxyURL.COURSE.value,
        exclude_from_auth=True,
    )
    async def get_course_info(
        self,
        course_title: str | None = None,
        subject_areas: str | None = None,
        catalogue_number: int | None = None,
        class_number: str | None = None,
        year: int = 2024,
        term: str | None = None,
        academic_career: str | None = None,
        campus: str | None = None,
        page_number: int = 1,
        page_size: int = 25,
    ) -> Sequence[CourseSearch]:
        return await ProxyQueryService.course(
            course_title=course_title,
            subject_areas=subject_areas,
            catalogue_number=catalogue_number,
            class_number=class_number,
            year=year,
            term=term,
            academic_career=academic_career,
            campus=campus,
            page_number=page_number,
            page_size=page_size,
        )
