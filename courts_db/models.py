from typing import Union

from typing_extensions import NotRequired, TypedDict


class DateRange(TypedDict):
    start: Union[str, None]
    end: Union[str, None]
    reorganization_dates: NotRequired[list[str]]
    reorganization: NotRequired[Union[list[str], str]]
    reorg: NotRequired[list[str]]
    notes: NotRequired[str]
    name: NotRequired[str]
    reason: NotRequired[str]


class CourtDict(TypedDict):
    active: NotRequired[bool]
    case_types: NotRequired[Union[list[str], str, None]]
    citation_string: str
    court_url: NotRequired[Union[str, None]]
    dates: list[DateRange]
    examples: list[str]
    id: str
    level: NotRequired[Union[str, None]]
    location: str
    name: str
    regex: list[str]
    system: str
    type: Union[str, None]
    reorganization_dates: NotRequired[list[str]]
    url: NotRequired[str]
    bankruptcy: NotRequired[None]
    notes: NotRequired[Union[str, None]]
    name_abbreviation: NotRequired[Union[str, None]]
    jurisdiction: NotRequired[Union[str, None]]
    parent: NotRequired[Union[str, None]]
    locations: NotRequired[int]
    cites: NotRequired[list[str]]
    sub_names: NotRequired[list[str]]
    divisions: NotRequired[list[str]]
    division: NotRequired[Union[list[str], str]]
    division_type: NotRequired[str]
    federal_circuit: NotRequired[int]
    lower_courts: NotRequired[list[str]]
    appeal_to: NotRequired[Union[str, None]]
