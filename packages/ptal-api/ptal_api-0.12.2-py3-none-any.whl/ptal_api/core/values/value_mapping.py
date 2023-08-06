from abc import ABCMeta, abstractmethod
from datetime import date
from typing import Any, Dict, Type, Union

from sgqlc.types import Input

from ptal_api.schema.api_schema import (
    DateInput,
    DateTimeValueInput,
    DoubleValueInput,
    IntValueInput,
    LinkValueInput,
    StringValueInput,
    ValueInput,
)
from .date_dataclass import PartialDateValue


class AbstractValueMapper(metaclass=ABCMeta):
    @staticmethod
    @abstractmethod
    def get_value_input(value: Any) -> Input:
        pass

    @staticmethod
    @abstractmethod
    def get_tdm_value_format(value: Any) -> Dict:
        pass


class StringValueMapper(AbstractValueMapper):
    @staticmethod
    def get_value_input(value: str) -> Input:
        string_input = StringValueInput()
        string_input.value = value

        value_input = ValueInput()
        value_input.string_value_input = string_input
        return value_input

    @staticmethod
    def get_tdm_value_format(value: str) -> Dict:
        return {"value": value}


class IntValueMapper(AbstractValueMapper):
    @staticmethod
    def get_value_input(value: int) -> Input:
        int_input = IntValueInput()
        int_input.value = value

        value_input = ValueInput()
        value_input.int_value_input = int_input
        return value_input

    @staticmethod
    def get_tdm_value_format(value: int) -> Dict:
        return {"value": value}


class DoubleValueMapper(AbstractValueMapper):
    @staticmethod
    def get_value_input(value: float) -> Input:
        double_input = DoubleValueInput()
        double_input.value = value

        value_input = ValueInput()
        value_input.double_value_input = double_input
        return value_input

    @staticmethod
    def get_tdm_value_format(value: float) -> Dict:
        return {"value": value}


class DateValueMapper(AbstractValueMapper):
    @staticmethod
    def get_value_input(value: Union[date, PartialDateValue]) -> Input:
        date_obj = DateInput()
        date_obj.day = value.day
        date_obj.month = value.month
        date_obj.year = value.year

        date_input = DateTimeValueInput()
        date_input.date = date_obj

        value_input = ValueInput()
        value_input.date_time_value_input = date_input
        return value_input

    @staticmethod
    def get_tdm_value_format(value: date) -> Dict:
        return {"date": {"day": value.day, "month": value.month, "year": value.year}}


class LinkValueMapper(AbstractValueMapper):
    @staticmethod
    def get_value_input(value: str) -> Input:
        link_input = LinkValueInput()
        link_input.link = value

        value_input = ValueInput()
        value_input.link_value_input = link_input
        return value_input

    @staticmethod
    def get_tdm_value_format(value: str) -> Dict:
        return {"link": value}


STRING_VALUE = "StringValue"
INT_VALUE = "IntValue"
DOUBLE_VALUE = "DoubleValue"
DATE_VALUE = "DateValue"
DATE_TIME_VALUE = "DateTimeValue"
LINK_VALUE = "LinkValue"
COMPOSITE_VALUE = "CompositeValue"


def get_map_helper(value_type: str) -> Type[AbstractValueMapper]:
    if value_type in ("String", STRING_VALUE):
        return StringValueMapper
    if value_type in ("Int", INT_VALUE):
        return IntValueMapper
    if value_type in ("Double", DOUBLE_VALUE):
        return DoubleValueMapper
    if value_type in ("Date", DATE_VALUE, DATE_TIME_VALUE):
        return DateValueMapper
    if value_type in ("Link", LINK_VALUE):
        return LinkValueMapper
    raise NotImplementedError(f"{value_type} type not implemented")
