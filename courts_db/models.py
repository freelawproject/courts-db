from typing import NotRequired

from typing_extensions import TypedDict


class DateRange(TypedDict):
    start: str | None
    end: str | None
    reorganization: NotRequired[list[str]]
    notes: NotRequired[str]
    name: NotRequired[str]
    reason: NotRequired[str]


class CourtDict(TypedDict):
    active: NotRequired[bool]
    case_types: NotRequired[list[str]]
    citation_string: str
    court_url: NotRequired[str]
    dates: list[DateRange]
    examples: list[str]
    id: str
    level: NotRequired[str | None]
    location: str
    name: str
    regex: list[str]
    system: str
    type: str | None
    notes: NotRequired[str | None]
    name_abbreviation: NotRequired[str | None]
    jurisdiction: NotRequired[str | None]
    parent: NotRequired[str | None]
    locations: NotRequired[int]
    cites: NotRequired[list[str]]
    sub_names: NotRequired[list[str]]
    divisions: NotRequired[list[str]]
    division_type: NotRequired[str]
    federal_circuit: NotRequired[int]
    lower_courts: NotRequired[list[str]]
    appeal_to: NotRequired[str | None]
