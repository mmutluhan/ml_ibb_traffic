# This code parses date/times, so please
#
#     pip install python-dateutil
#
# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = traffic_response_from_dict(json.loads(json_string))

from dataclasses import dataclass
from typing import Optional, Any, List, TypeVar, Type, cast, Callable
from datetime import datetime
from uuid import UUID
import dateutil.parser


T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_datetime(x: Any) -> datetime:
    return dateutil.parser.parse(x)


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def to_float(x: Any) -> float:
    assert isinstance(x, float)
    return x


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


@dataclass
class Info:
    notes: Optional[str] = None
    type_override: Optional[str] = None
    label: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Info':
        assert isinstance(obj, dict)
        notes = from_union([from_str, from_none], obj.get("notes"))
        type_override = from_union([from_str, from_none], obj.get("type_override"))
        label = from_union([from_str, from_none], obj.get("label"))
        return Info(notes, type_override, label)

    def to_dict(self) -> dict:
        result: dict = {}
        result["notes"] = from_union([from_str, from_none], self.notes)
        result["type_override"] = from_union([from_str, from_none], self.type_override)
        result["label"] = from_union([from_str, from_none], self.label)
        return result


@dataclass
class Field:
    type: Optional[str] = None
    id: Optional[str] = None
    info: Optional[Info] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Field':
        assert isinstance(obj, dict)
        type = from_union([from_str, from_none], obj.get("type"))
        id = from_union([from_str, from_none], obj.get("id"))
        info = from_union([Info.from_dict, from_none], obj.get("info"))
        return Field(type, id, info)

    def to_dict(self) -> dict:
        result: dict = {}
        result["type"] = from_union([from_str, from_none], self.type)
        result["id"] = from_union([from_str, from_none], self.id)
        result["info"] = from_union([lambda x: to_class(Info, x), from_none], self.info)
        return result


@dataclass
class Links:
    start: Optional[str] = None
    next: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Links':
        assert isinstance(obj, dict)
        start = from_union([from_str, from_none], obj.get("start"))
        next = from_union([from_str, from_none], obj.get("next"))
        return Links(start, next)

    def to_dict(self) -> dict:
        result: dict = {}
        result["start"] = from_union([from_str, from_none], self.start)
        result["next"] = from_union([from_str, from_none], self.next)
        return result


@dataclass
class Record:
    id: Optional[int] = None
    date_time: Optional[datetime] = None
    longitude: Optional[float] = None
    latitude: Optional[float] = None
    geohash: Optional[str] = None
    minimum_speed: Optional[int] = None
    maximum_speed: Optional[int] = None
    average_speed: Optional[int] = None
    number_of_vehicles: Optional[int] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Record':
        assert isinstance(obj, dict)
        id = from_union([from_int, from_none], obj.get("_id"))
        date_time = from_union([from_datetime, from_none], obj.get("DATE_TIME"))
        longitude = from_union([from_float, from_none], obj.get("LONGITUDE"))
        latitude = from_union([from_float, from_none], obj.get("LATITUDE"))
        geohash = from_union([from_str, from_none], obj.get("GEOHASH"))
        minimum_speed = from_union([from_int, from_none], obj.get("MINIMUM_SPEED"))
        maximum_speed = from_union([from_int, from_none], obj.get("MAXIMUM_SPEED"))
        average_speed = from_union([from_int, from_none], obj.get("AVERAGE_SPEED"))
        number_of_vehicles = from_union([from_int, from_none], obj.get("NUMBER_OF_VEHICLES"))
        return Record(id, date_time, longitude, latitude, geohash, minimum_speed, maximum_speed, average_speed, number_of_vehicles)

    def to_dict(self) -> dict:
        result: dict = {}
        result["_id"] = from_union([from_int, from_none], self.id)
        result["DATE_TIME"] = from_union([lambda x: x.isoformat(), from_none], self.date_time)
        result["LONGITUDE"] = from_union([to_float, from_none], self.longitude)
        result["LATITUDE"] = from_union([to_float, from_none], self.latitude)
        result["GEOHASH"] = from_union([from_str, from_none], self.geohash)
        result["MINIMUM_SPEED"] = from_union([from_int, from_none], self.minimum_speed)
        result["MAXIMUM_SPEED"] = from_union([from_int, from_none], self.maximum_speed)
        result["AVERAGE_SPEED"] = from_union([from_int, from_none], self.average_speed)
        result["NUMBER_OF_VEHICLES"] = from_union([from_int, from_none], self.number_of_vehicles)
        return result


@dataclass
class Result:
    include_total: Optional[bool] = None
    resource_id: Optional[UUID] = None
    fields: Optional[List[Field]] = None
    records_format: Optional[str] = None
    records: Optional[List[Record]] = None
    limit: Optional[int] = None
    links: Optional[Links] = None
    total: Optional[int] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Result':
        assert isinstance(obj, dict)
        include_total = from_union([from_bool, from_none], obj.get("include_total"))
        resource_id = from_union([lambda x: UUID(x), from_none], obj.get("resource_id"))
        fields = from_union([lambda x: from_list(Field.from_dict, x), from_none], obj.get("fields"))
        records_format = from_union([from_str, from_none], obj.get("records_format"))
        records = from_union([lambda x: from_list(Record.from_dict, x), from_none], obj.get("records"))
        limit = from_union([from_int, from_none], obj.get("limit"))
        links = from_union([Links.from_dict, from_none], obj.get("_links"))
        total = from_union([from_int, from_none], obj.get("total"))
        return Result(include_total, resource_id, fields, records_format, records, limit, links, total)

    def to_dict(self) -> dict:
        result: dict = {}
        result["include_total"] = from_union([from_bool, from_none], self.include_total)
        result["resource_id"] = from_union([lambda x: str(x), from_none], self.resource_id)
        result["fields"] = from_union([lambda x: from_list(lambda x: to_class(Field, x), x), from_none], self.fields)
        result["records_format"] = from_union([from_str, from_none], self.records_format)
        result["records"] = from_union([lambda x: from_list(lambda x: to_class(Record, x), x), from_none], self.records)
        result["limit"] = from_union([from_int, from_none], self.limit)
        result["_links"] = from_union([lambda x: to_class(Links, x), from_none], self.links)
        result["total"] = from_union([from_int, from_none], self.total)
        return result


@dataclass
class TrafficResponse:
    help: Optional[str] = None
    success: Optional[bool] = None
    result: Optional[Result] = None

    @staticmethod
    def from_dict(obj: Any) -> 'TrafficResponse':
        assert isinstance(obj, dict)
        help = from_union([from_str, from_none], obj.get("help"))
        success = from_union([from_bool, from_none], obj.get("success"))
        result = from_union([Result.from_dict, from_none], obj.get("result"))
        return TrafficResponse(help, success, result)

    def to_dict(self) -> dict:
        result: dict = {}
        result["help"] = from_union([from_str, from_none], self.help)
        result["success"] = from_union([from_bool, from_none], self.success)
        result["result"] = from_union([lambda x: to_class(Result, x), from_none], self.result)
        return result


def traffic_response_from_dict(s: Any) -> TrafficResponse:
    return TrafficResponse.from_dict(s)


def traffic_response_to_dict(x: TrafficResponse) -> Any:
    return to_class(TrafficResponse, x)
