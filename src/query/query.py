# query.py

from __future__ import annotations

from collections.abc import Sequence
from typing import Any, cast

import requests

from . import dto
from .helpers import Paginator, ParamsBuilder, ResponseParser

__all__ = ("Query",)


COURSE_SEARCH_TARGET = "/system/COURSE_SEARCH/queryx"
CAMPUS_TARGET = "/system/CAMPUS/queryx"
CSP_ACAD_CAREER_TARGET = "/system/CSP_ACAD_CAREER/queryx"
TERMS_TARGET = "/system/TERMS/queryx"
SUBJECT_TARGET = "/system/SUBJECTS_BY_YEAR/queryx"
API_END_POINT = "https://courseplanner-api.adelaide.edu.au/api/course-planner-query/v1/"
VIRTUAL = "Y"
YEAR = 2024


class Query:
    @staticmethod
    def query(param_builder: ParamsBuilder, response_dto: Any) -> Any:
        raw_response = requests.get(url=API_END_POINT, params=param_builder.params)  # noqa: S113
        return ResponseParser(raw_response, response_dto).rows

    @staticmethod
    def campus() -> Sequence[dto.CampusDTO]:
        return cast(
            Sequence[dto.CampusDTO],
            Query.query(ParamsBuilder(target=CAMPUS_TARGET, MaxRows=9999), dto.CampusDTO),
        )

    @staticmethod
    def academic_career() -> Sequence[dto.CareerDTO]:
        return cast(
            Sequence[dto.CareerDTO],
            Query.query(
                ParamsBuilder(target=CSP_ACAD_CAREER_TARGET, MaxRows=9999),
                dto.CareerDTO,
            ),
        )

    @staticmethod
    def term() -> Sequence[dto.TermDTO]:
        return cast(
            Sequence[dto.TermDTO],
            Query.query(
                ParamsBuilder(
                    target=TERMS_TARGET,
                    MaxRows=9999,
                    virtual=VIRTUAL,
                    year_from=YEAR,
                    year_to=YEAR,
                ),
                dto.TermDTO,
            ),
        )

    @staticmethod
    def subjects() -> Sequence[dto.SubjectDTO]:
        return cast(
            Sequence[dto.SubjectDTO],
            Query.query(
                ParamsBuilder(
                    target=SUBJECT_TARGET,
                    MaxRows=9999,
                    virtual=VIRTUAL,
                    year_from=YEAR,
                    year_to=YEAR,
                ),
                dto.SubjectDTO,
            ),
        )

    @staticmethod
    def course(
        course_title: str | None = None,
        subject_areas: str | None = None,
        catalogue_number: int | None = None,
        class_number: str | None = None,
        year: int = YEAR,
        term: str | None = None,
        academic_career: str | None = None,
        campus: str | None = None,
        page_number: int = 1,
        page_size: int = 25,
    ) -> Sequence[dto.CourseSearchDTO]:
        params_builder = ParamsBuilder(
            course_title=course_title,
            subject_areas=subject_areas,
            catalogue_number=catalogue_number,
            class_number=class_number,
            year=year,
            term=term,
            academic_career=academic_career,
            campus=campus,
        )
        params_builder.add(
            page_number=page_number,
            page_size=page_size,
            target=COURSE_SEARCH_TARGET,
            virtual=VIRTUAL,
        )
        return cast(
            Sequence[dto.CourseSearchDTO],
            Query.query(
                params_builder,
                dto.CourseSearchDTO,
            ),
        )

    @staticmethod
    def course_paginator(
        course_title: str | None = None,
        subject_areas: str | None = None,
        catalogue_number: int | None = None,
        class_number: str | None = None,
        year: int = YEAR,
        term: str | None = None,
        academic_career: str | None = None,
        campus: str | None = None,
        page_size: int = 25,
    ) -> Paginator:
        params_builder = ParamsBuilder(
            course_title=course_title,
            subject_areas=subject_areas,
            catalogue_number=catalogue_number,
            class_number=class_number,
            year=year,
            term=term,
            academic_career=academic_career,
            campus=campus,
        )
        params_builder.add(
            page_size=page_size,
            target=COURSE_SEARCH_TARGET,
            virtual=VIRTUAL,
        )
        return Paginator(
            end_point=API_END_POINT,
            params=params_builder,
            response_dto=dto.CourseSearchDTO,
            page_size=page_size,
        )
