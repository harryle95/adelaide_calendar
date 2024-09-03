# helpers.py

from typing import TYPE_CHECKING, Any, Literal, Self, cast

import aiohttp
from aiohttp import ClientResponse as Response
from aiohttp.web_exceptions import HTTPError

if TYPE_CHECKING:
    from src.controller.proxy.schema import Group

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
    ignore_fields = [
        "attr:rownumber",
        "DISCOVERY_EXPERIENCE_GLOBAL",
        "DISCOVERY_EXPERIENCE–COMMUNITY",  # noqa: RUF001
        "DISCOVERY_EXPERIENCE–WORKING",  # noqa: RUF001
        "FIELD_OF_EDUCATION",
        "ISLOP",
        "SSR_HECS_BAND_ID",
    ]

    def __init__(self, data: Any, num_rows: int, total_rows: int) -> None:
        self.data = data
        self.num_rows = num_rows
        self.total_rows = total_rows

    @classmethod
    async def _extract_query(cls, response: Response) -> Any:
        # Validate
        try:
            response.raise_for_status()
        except HTTPError as e:
            raise e

        body: dict[str, Any] = await response.json()
        status = body.get("status", "unsuccessful")
        if status != "success":
            raise Exception("Server response with unsuccessful query")

        # Extract query data
        data: dict[str, Any] = body.get("data", {})
        return data.get("query", {})

    @classmethod
    async def _extract_rows(cls, response: Response) -> Any:
        query = await cls._extract_query(response)
        return query.get("rows", [])

    @classmethod
    async def _extract_groups(cls, response: Response) -> Any:
        rows = await cls._extract_rows(response)
        if rows:
            return cast(list["Group"], rows[0].get("groups", []))
        return []

    @classmethod
    async def parse(
        cls,
        response: Response,
        response_dto: Any,
        extractor: Literal["rows", "groups"] = "rows",
    ) -> "ResponseParser":
        match extractor:
            case "rows":
                query = await cls._extract_query(response)
                total_rows = query.get("total_rows", -1)
                data = query.get("rows", [])
            case "groups":
                data = await cls._extract_groups(response)
                total_rows = 1
            case _:
                raise ValueError(f"Invalid extractor: {extractor}")
        rows = []
        for row in data:
            rows.append(response_dto(**{k: v for k, v in row.items() if k not in cls.ignore_fields}))
        num_rows = len(rows)

        return cls(data=rows, num_rows=num_rows, total_rows=total_rows)


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

    async def __aiter__(self) -> Self:
        self.page_number = 0
        self._has_next = True
        return self

    async def __anext__(self) -> ResponseParser:
        if self._has_next:
            self.params.set("page_number", self.page_number)
            async with aiohttp.ClientSession() as client:
                raw_response = await client.get(self.end_point, params=self.params.params)
            response = await ResponseParser.parse(raw_response, self.dto)
            self.page_number += 1
            if (
                response.total_rows == -1
                or response.total_rows <= (self.page_number - 1) * self.page_size + response.num_rows
            ):
                self._has_next = False
            return response
        raise StopIteration
