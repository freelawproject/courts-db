from typing import NotRequired, TypedDict, final


@final
class DateRange(TypedDict):
    start: str | None
    end: str | None
    reorganization_dates: NotRequired[list[str]]
    reorganization: NotRequired[list[str] | str]
    reorg: NotRequired[list[str]]
    notes: NotRequired[str]
    name: NotRequired[str]
    reason: NotRequired[str]


@final
class CourtDict(TypedDict):
    active: NotRequired[bool]
    case_types: NotRequired[list[str] | str | None]
    citation_string: str
    court_url: NotRequired[str | None]
    dates: list[DateRange]
    examples: list[str]
    id: str
    level: NotRequired[str | None]
    location: str
    name: str
    regex: list[str]
    system: str
    type: str | None
    reorganization_dates: NotRequired[list[str]]
    url: NotRequired[str]
    bankruptcy: NotRequired[None]
    notes: NotRequired[str | None]
    name_abbreviation: NotRequired[str | None]
    jurisdiction: NotRequired[str | None]
    parent: NotRequired[str | None]
    locations: NotRequired[int]
    cites: NotRequired[list[str]]
    sub_names: NotRequired[list[str]]
    divisions: NotRequired[list[str]]
    division: NotRequired[list[str] | str]
    division_type: NotRequired[str]
    federal_circuit: NotRequired[int]
    lower_courts: NotRequired[list[str]]
    appeal_to: NotRequired[list[str] | str | None]
