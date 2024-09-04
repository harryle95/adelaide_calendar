# query.py

from __future__ import annotations

from collections.abc import Sequence
from typing import Any, Literal, cast

import aiohttp

import src.controller.proxy.schema as dto

from .helpers import Paginator, ParamsBuilder, ResponseParser

__all__ = ("ProxyQueryService",)


COURSE_SEARCH_TARGET = "/system/COURSE_SEARCH/queryx"
COURSE_DETAIL_TARGET = "/system/COURSE_DTL/queryx"
COURSE_CLASS_LIST_TARGET = "/system/COURSE_CLASS_LIST/queryx"
CAMPUS_TARGET = "/system/CAMPUS/queryx"
CSP_ACAD_CAREER_TARGET = "/system/CSP_ACAD_CAREER/queryx"
TERMS_TARGET = "/system/TERMS/queryx"
SUBJECT_TARGET = "/system/SUBJECTS_BY_YEAR/queryx"
API_END_POINT = "https://courseplanner-api.adelaide.edu.au/api/course-planner-query/v1/"
VIRTUAL = "Y"
YEAR = 2024


class ProxyQueryService:
    @staticmethod
    async def query(
        param_builder: ParamsBuilder, response_dto: Any, extractor: Literal["rows", "groups"] = "rows"
    ) -> Any:
        async with aiohttp.ClientSession() as client:
            raw_response = await client.get(
                url=API_END_POINT,
                params=param_builder.params,
            )
            result = await ResponseParser.parse(raw_response, response_dto, extractor=extractor)
            return result.data

    @staticmethod
    async def campus() -> Sequence[dto.Campus]:
        return cast(
            Sequence[dto.Campus],
            await ProxyQueryService.query(ParamsBuilder(target=CAMPUS_TARGET, MaxRows=9999), dto.Campus),
        )

    @staticmethod
    async def academic_career() -> Sequence[dto.Career]:
        return cast(
            Sequence[dto.Career],
            await ProxyQueryService.query(
                ParamsBuilder(target=CSP_ACAD_CAREER_TARGET, MaxRows=9999),
                dto.Career,
            ),
        )

    @staticmethod
    async def term() -> Sequence[dto.Term]:
        return cast(
            Sequence[dto.Term],
            await ProxyQueryService.query(
                ParamsBuilder(
                    target=TERMS_TARGET,
                    MaxRows=9999,
                    virtual=VIRTUAL,
                    year_from=YEAR,
                    year_to=YEAR,
                ),
                dto.Term,
            ),
        )

    @staticmethod
    async def subjects() -> Sequence[dto.Subject]:
        return cast(
            Sequence[dto.Subject],
            await ProxyQueryService.query(
                ParamsBuilder(
                    target=SUBJECT_TARGET,
                    MaxRows=9999,
                    virtual=VIRTUAL,
                    year_from=YEAR,
                    year_to=YEAR,
                ),
                dto.Subject,
            ),
        )

    @staticmethod
    async def course(
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
    ) -> Sequence[dto.CourseSearch]:
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
            Sequence[dto.CourseSearch],
            await ProxyQueryService.query(
                params_builder,
                dto.CourseSearch,
            ),
        )

    @staticmethod
    async def course_detail(course_id: str, course_offer_number: int, term: int, year: int = YEAR) -> dto.CourseDetail:
        params_builder = ParamsBuilder(
            target=COURSE_DETAIL_TARGET,
            virtual=VIRTUAL,
            year=year,
            courseid=course_id,
            course_offer_nbr=course_offer_number,
            term=term,
        )
        data = await ProxyQueryService.query(
            params_builder,
            dto.CourseDetail,
        )
        return cast(dto.CourseDetail, data[0])

    @staticmethod
    async def course_class_list(
        course_id: str, course_offer_number: int, term: int, session: int = 1
    ) -> Sequence[dto.Group]:
        params_builder = ParamsBuilder(
            target=COURSE_CLASS_LIST_TARGET,
            virtual=VIRTUAL,
            crseid=course_id,
            offer=course_offer_number,
            term=term,
            session=session,
        )
        data = await ProxyQueryService.query(params_builder, dto.Group, extractor="groups")
        return cast(Sequence[dto.Group], data)

    @staticmethod
    async def course_paginator(
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
            response_dto=dto.CourseSearch,
            page_size=page_size,
        )
