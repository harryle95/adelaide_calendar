# helpers.py

from typing import Any, Self

import requests
from requests import Response

from . import dto

__all__ = (
    "Paginator",
    "ParamsBuilder",
    "ResponseParser",
)


class ParamsBuilder:
    def __init__(self, **kwargs: Any):
        self._params: dict[str, Any] = {}
        self.add(**kwargs)
        if not self._params:
            raise ValueError("Params must have at least one search criteria")

    def set(self, key: str, value: Any) -> None:
        self._params[key] = value

    def add(self, **kwargs: Any) -> None:
        for k, v in kwargs.items():
            if v is not None:
                self._params[k] = v

    @property
    def params(self) -> str:
        return "&".join(f"{k}={v}" for k, v in self._params.items())


class ResponseParser:
    mapping = {
        dto.CampusDTO: dto.CAMPUS_MAPPING,
        dto.CareerDTO: dto.CAREER_MAPPING,
        dto.CourseSearchDTO: dto.COURSE_SEARCH_MAPPING,
        dto.TermDTO: dto.TERM_MAPPING,
        dto.SubjectDTO: dto.SUBJECT_MAPPING,
    }

    def __init__(self, response: Response, response_dto: Any) -> None:
        self.response = response
        self.dto = response_dto
        self.response_mapping = self.mapping[response_dto]

        # Validate
        try:
            self.response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise e

        body: dict[str, Any] = self.response.json()
        status = body.get("status", "unsuccessful")
        if status != "success":
            raise Exception("Server response with unsuccessful query")

        # Extract query data
        data: dict[str, Any] = body.get("data", {})
        self.query: dict[str, Any] = data.get("query", {})
        rows = self.query.get("rows", [])
        self.rows = []
        for row in rows:
            args = {}
            for k, v in self.response_mapping.items():
                args[v] = row.get(k, None)
            self.rows.append(self.dto(**args))
        self.num_rows = len(self.rows)
        self.total_rows = self.query.get("total_rows", -1)


class Paginator:
    def __init__(
        self,
        end_point: str,
        params: ParamsBuilder,
        response_dto: Any,
        page_size: int = 25,
    ):
        self.end_point = end_point
        self.params = params
        self.page_size = page_size
        self.dto = response_dto
        self.page_number = 0
        self._has_next = True

    def __iter__(self) -> Self:
        self.page_number = 0
        self._has_next = True
        return self

    def __next__(self) -> ResponseParser:
        if self._has_next:
            self.params.set("page_number", self.page_number)
            raw_response = requests.get(self.end_point, params=self.params.params)  # noqa: S113
            response = ResponseParser(raw_response, self.dto)
            self.page_number += 1
            if (
                response.total_rows == -1
                or response.total_rows <= (self.page_number - 1) * self.page_size + response.num_rows
            ):
                self._has_next = False
            return response
        raise StopIteration
