"""Type flo.params.simpleresistivehydronic, version 000"""
import json
from enum import auto
from typing import Any
from typing import Dict
from typing import List
from typing import Literal

from fastapi_utils.enums import StrEnum
from gridworks.errors import SchemaError
from gridworks.message import as_enum
from pydantic import BaseModel
from pydantic import Field
from pydantic import validator

from gwatn.enums import RecognizedCurrencyUnit


class RecognizedCurrencyUnit000SchemaEnum:
    enum_name: str = "recognized.currency.unit.000"
    symbols: List[str] = [
        "00000000",
        "e57c5143",
        "f7b38fc5",
    ]

    @classmethod
    def is_symbol(cls, candidate: str) -> bool:
        if candidate in cls.symbols:
            return True
        return False


class RecognizedCurrencyUnit000(StrEnum):
    UNKNOWN = auto()
    USD = auto()
    GBP = auto()

    @classmethod
    def default(cls) -> "RecognizedCurrencyUnit000":
        return cls.UNKNOWN

    @classmethod
    def values(cls) -> List[str]:
        return [elt.value for elt in cls]


class RecognizedCurrencyUnitMap:
    @classmethod
    def type_to_local(cls, symbol: str) -> RecognizedCurrencyUnit:
        if not RecognizedCurrencyUnit000SchemaEnum.is_symbol(symbol):
            raise SchemaError(
                f"{symbol} must belong to RecognizedCurrencyUnit000 symbols"
            )
        versioned_enum = cls.type_to_versioned_enum_dict[symbol]
        return as_enum(
            versioned_enum, RecognizedCurrencyUnit, RecognizedCurrencyUnit.default()
        )

    @classmethod
    def local_to_type(cls, recognized_currency_unit: RecognizedCurrencyUnit) -> str:
        if not isinstance(recognized_currency_unit, RecognizedCurrencyUnit):
            raise SchemaError(
                f"{recognized_currency_unit} must be of type {RecognizedCurrencyUnit}"
            )
        versioned_enum = as_enum(
            recognized_currency_unit,
            RecognizedCurrencyUnit000,
            RecognizedCurrencyUnit000.default(),
        )
        return cls.versioned_enum_to_type_dict[versioned_enum]

    type_to_versioned_enum_dict: Dict[str, RecognizedCurrencyUnit000] = {
        "00000000": RecognizedCurrencyUnit000.UNKNOWN,
        "e57c5143": RecognizedCurrencyUnit000.USD,
        "f7b38fc5": RecognizedCurrencyUnit000.GBP,
    }

    versioned_enum_to_type_dict: Dict[RecognizedCurrencyUnit000, str] = {
        RecognizedCurrencyUnit000.UNKNOWN: "00000000",
        RecognizedCurrencyUnit000.USD: "e57c5143",
        RecognizedCurrencyUnit000.GBP: "f7b38fc5",
    }


def check_is_uuid_canonical_textual(v: str) -> None:
    """
    UuidCanonicalTextual format:  A string of hex words separated by hyphens
    of length 8-4-4-4-12.

    Raises:
        ValueError: if not UuidCanonicalTextual format
    """
    try:
        x = v.split("-")
    except AttributeError as e:
        raise ValueError(f"Failed to split on -: {e}")
    if len(x) != 5:
        raise ValueError(f"{v} split by '-' did not have 5 words")
    for hex_word in x:
        try:
            int(hex_word, 16)
        except ValueError:
            raise ValueError(f"Words of {v} are not all hex")
    if len(x[0]) != 8:
        raise ValueError(f"{v} word lengths not 8-4-4-4-12")
    if len(x[1]) != 4:
        raise ValueError(f"{v} word lengths not 8-4-4-4-12")
    if len(x[2]) != 4:
        raise ValueError(f"{v} word lengths not 8-4-4-4-12")
    if len(x[3]) != 4:
        raise ValueError(f"{v} word lengths not 8-4-4-4-12")
    if len(x[4]) != 12:
        raise ValueError(f"{v} word lengths not 8-4-4-4-12")


def check_is_left_right_dot(v: str) -> None:
    """
    LeftRightDot format: Lowercase alphanumeric words separated by periods,
    most significant word (on the left) starting with an alphabet character.

    Raises:
        ValueError: if not LeftRightDot format
    """
    from typing import List

    try:
        x: List[str] = v.split(".")
    except:
        raise ValueError(f"Failed to seperate {v} into words with split'.'")
    first_word = x[0]
    first_char = first_word[0]
    if not first_char.isalpha():
        raise ValueError(f"Most significant word of {v} must start with alphabet char.")
    for word in x:
        if not word.isalnum():
            raise ValueError(f"words of {v} split by by '.' must be alphanumeric.")
    if not v.islower():
        raise ValueError(f"All characters of {v} must be lowercase.")


class FloParamsSimpleresistivehydronic(BaseModel):
    """ """

    GNodeAlias: str = Field(
        title="GNodeAlias",
    )
    FloParamsUid: str = Field(
        title="FloParamsUid",
    )
    HomeCity: str = Field(
        title="HomeCity",
        default="MILLINOCKET_ME",
    )
    TimezoneString: str = Field(
        title="TimezoneString",
        default="US/Eastern",
    )
    StartYearUtc: int = Field(
        title="StartYearUtc",
        default=2020,
    )
    StartMonthUtc: int = Field(
        title="StartMonthUtc",
        default=1,
    )
    StartDayUtc: int = Field(
        title="StartDayUtc",
        default=1,
    )
    StartHourUtc: int = Field(
        title="StartHourUtc",
        default=0,
    )
    StartMinuteUtc: int = Field(
        title="StartMinuteUtc",
        default=0,
    )
    StoreSizeGallons: int = Field(
        title="StoreSizeGallons",
        default=240,
    )
    MaxStoreTempF: int = Field(
        title="MaxStoreTempF",
        default=190,
    )
    ElementMaxPowerKw: float = Field(
        title="ElementMaxPowerKw",
        default=9.5,
    )
    RequiredSourceWaterTempF: int = Field(
        title="RequiredSourceWaterTempF",
        default=120,
    )
    FixedPumpGpm: float = Field(
        title="FixedPumpGpm",
        default=4.5,
    )
    ReturnWaterFixedDeltaT: int = Field(
        title="ReturnWaterFixedDeltaT",
        default=20,
    )
    SliceDurationMinutes: List[int] = Field(
        title="SliceDurationMinutes",
        default=[60],
    )
    PowerLostFromHouseKwList: List[float] = Field(
        title="PowerLostFromHouseKwList",
        default=[3.42],
    )
    OutsideTempF: List[float] = Field(
        title="OutsideTempF",
        default=[-5.1],
    )
    DistributionPrice: List[float] = Field(
        title="DistributionPrice",
        default=[40.0],
    )
    RealtimeElectricityPrice: List[float] = Field(
        title="RealtimeElectricityPrice",
        default=[10.35],
    )
    RtElecPriceUid: str = Field(
        title="RtElecPriceUid",
    )
    WeatherUid: str = Field(
        title="WeatherUid",
    )
    DistPriceUid: str = Field(
        title="DistPriceUid",
    )
    CurrencyUnit: RecognizedCurrencyUnit = Field(
        title="CurrencyUnit",
        default=RecognizedCurrencyUnit.USD,
    )
    TypeName: Literal[
        "flo.params.simpleresistivehydronic"
    ] = "flo.params.simpleresistivehydronic"
    Version: str = "000"

    @validator("GNodeAlias")
    def _check_g_node_alias(cls, v: str) -> str:
        try:
            check_is_left_right_dot(v)
        except ValueError as e:
            raise ValueError(f"GNodeAlias failed LeftRightDot format validation: {e}")
        return v

    @validator("FloParamsUid")
    def _check_flo_params_uid(cls, v: str) -> str:
        try:
            check_is_uuid_canonical_textual(v)
        except ValueError as e:
            raise ValueError(
                f"FloParamsUid failed UuidCanonicalTextual format validation: {e}"
            )
        return v

    @validator("RtElecPriceUid")
    def _check_rt_elec_price_uid(cls, v: str) -> str:
        try:
            check_is_uuid_canonical_textual(v)
        except ValueError as e:
            raise ValueError(
                f"RtElecPriceUid failed UuidCanonicalTextual format validation: {e}"
            )
        return v

    @validator("WeatherUid")
    def _check_weather_uid(cls, v: str) -> str:
        try:
            check_is_uuid_canonical_textual(v)
        except ValueError as e:
            raise ValueError(
                f"WeatherUid failed UuidCanonicalTextual format validation: {e}"
            )
        return v

    @validator("DistPriceUid")
    def _check_dist_price_uid(cls, v: str) -> str:
        try:
            check_is_uuid_canonical_textual(v)
        except ValueError as e:
            raise ValueError(
                f"DistPriceUid failed UuidCanonicalTextual format validation: {e}"
            )
        return v

    @validator("CurrencyUnit")
    def _check_currency_unit(cls, v: RecognizedCurrencyUnit) -> RecognizedCurrencyUnit:
        return as_enum(v, RecognizedCurrencyUnit, RecognizedCurrencyUnit.UNKNOWN)

    def as_dict(self) -> Dict[str, Any]:
        d = self.dict()
        del d["CurrencyUnit"]
        CurrencyUnit = as_enum(
            self.CurrencyUnit, RecognizedCurrencyUnit, RecognizedCurrencyUnit.default()
        )
        d["CurrencyUnitGtEnumSymbol"] = RecognizedCurrencyUnitMap.local_to_type(
            CurrencyUnit
        )
        return d

    def as_type(self) -> str:
        return json.dumps(self.as_dict())

    def __hash__(self):
        return hash((type(self),) + tuple(self.__dict__.values()))  # noqa


class FloParamsSimpleresistivehydronic_Maker:
    type_name = "flo.params.simpleresistivehydronic"
    version = "000"

    def __init__(
        self,
        g_node_alias: str,
        flo_params_uid: str,
        home_city: str,
        timezone_string: str,
        start_year_utc: int,
        start_month_utc: int,
        start_day_utc: int,
        start_hour_utc: int,
        start_minute_utc: int,
        store_size_gallons: int,
        max_store_temp_f: int,
        element_max_power_kw: float,
        required_source_water_temp_f: int,
        fixed_pump_gpm: float,
        return_water_fixed_delta_t: int,
        slice_duration_minutes: List[int],
        power_lost_from_house_kw_list: List[float],
        outside_temp_f: List[float],
        distribution_price: List[float],
        realtime_electricity_price: List[float],
        rt_elec_price_uid: str,
        weather_uid: str,
        dist_price_uid: str,
        currency_unit: RecognizedCurrencyUnit,
    ):
        self.tuple = FloParamsSimpleresistivehydronic(
            GNodeAlias=g_node_alias,
            FloParamsUid=flo_params_uid,
            HomeCity=home_city,
            TimezoneString=timezone_string,
            StartYearUtc=start_year_utc,
            StartMonthUtc=start_month_utc,
            StartDayUtc=start_day_utc,
            StartHourUtc=start_hour_utc,
            StartMinuteUtc=start_minute_utc,
            StoreSizeGallons=store_size_gallons,
            MaxStoreTempF=max_store_temp_f,
            ElementMaxPowerKw=element_max_power_kw,
            RequiredSourceWaterTempF=required_source_water_temp_f,
            FixedPumpGpm=fixed_pump_gpm,
            ReturnWaterFixedDeltaT=return_water_fixed_delta_t,
            SliceDurationMinutes=slice_duration_minutes,
            PowerLostFromHouseKwList=power_lost_from_house_kw_list,
            OutsideTempF=outside_temp_f,
            DistributionPrice=distribution_price,
            RealtimeElectricityPrice=realtime_electricity_price,
            RtElecPriceUid=rt_elec_price_uid,
            WeatherUid=weather_uid,
            DistPriceUid=dist_price_uid,
            CurrencyUnit=currency_unit,
            #
        )

    @classmethod
    def tuple_to_type(cls, tuple: FloParamsSimpleresistivehydronic) -> str:
        """
        Given a Python class object, returns the serialized JSON type object
        """
        return tuple.as_type()

    @classmethod
    def type_to_tuple(cls, t: str) -> FloParamsSimpleresistivehydronic:
        """
        Given a serialized JSON type object, returns the Python class object
        """
        try:
            d = json.loads(t)
        except TypeError:
            raise SchemaError("Type must be string or bytes!")
        if not isinstance(d, dict):
            raise SchemaError(f"Deserializing {t} must result in dict!")
        return cls.dict_to_tuple(d)

    @classmethod
    def dict_to_tuple(cls, d: dict[str, Any]) -> FloParamsSimpleresistivehydronic:
        d2 = dict(d)
        if "GNodeAlias" not in d2.keys():
            raise SchemaError(f"dict {d2} missing GNodeAlias")
        if "FloParamsUid" not in d2.keys():
            raise SchemaError(f"dict {d2} missing FloParamsUid")
        if "HomeCity" not in d2.keys():
            raise SchemaError(f"dict {d2} missing HomeCity")
        if "TimezoneString" not in d2.keys():
            raise SchemaError(f"dict {d2} missing TimezoneString")
        if "StartYearUtc" not in d2.keys():
            raise SchemaError(f"dict {d2} missing StartYearUtc")
        if "StartMonthUtc" not in d2.keys():
            raise SchemaError(f"dict {d2} missing StartMonthUtc")
        if "StartDayUtc" not in d2.keys():
            raise SchemaError(f"dict {d2} missing StartDayUtc")
        if "StartHourUtc" not in d2.keys():
            raise SchemaError(f"dict {d2} missing StartHourUtc")
        if "StartMinuteUtc" not in d2.keys():
            raise SchemaError(f"dict {d2} missing StartMinuteUtc")
        if "StoreSizeGallons" not in d2.keys():
            raise SchemaError(f"dict {d2} missing StoreSizeGallons")
        if "MaxStoreTempF" not in d2.keys():
            raise SchemaError(f"dict {d2} missing MaxStoreTempF")
        if "ElementMaxPowerKw" not in d2.keys():
            raise SchemaError(f"dict {d2} missing ElementMaxPowerKw")
        if "RequiredSourceWaterTempF" not in d2.keys():
            raise SchemaError(f"dict {d2} missing RequiredSourceWaterTempF")
        if "FixedPumpGpm" not in d2.keys():
            raise SchemaError(f"dict {d2} missing FixedPumpGpm")
        if "ReturnWaterFixedDeltaT" not in d2.keys():
            raise SchemaError(f"dict {d2} missing ReturnWaterFixedDeltaT")
        if "SliceDurationMinutes" not in d2.keys():
            raise SchemaError(f"dict {d2} missing SliceDurationMinutes")
        if "PowerLostFromHouseKwList" not in d2.keys():
            raise SchemaError(f"dict {d2} missing PowerLostFromHouseKwList")
        if "OutsideTempF" not in d2.keys():
            raise SchemaError(f"dict {d2} missing OutsideTempF")
        if "DistributionPrice" not in d2.keys():
            raise SchemaError(f"dict {d2} missing DistributionPrice")
        if "RealtimeElectricityPrice" not in d2.keys():
            raise SchemaError(f"dict {d2} missing RealtimeElectricityPrice")
        if "RtElecPriceUid" not in d2.keys():
            raise SchemaError(f"dict {d2} missing RtElecPriceUid")
        if "WeatherUid" not in d2.keys():
            raise SchemaError(f"dict {d2} missing WeatherUid")
        if "DistPriceUid" not in d2.keys():
            raise SchemaError(f"dict {d2} missing DistPriceUid")
        if "CurrencyUnitGtEnumSymbol" not in d2.keys():
            raise SchemaError(f"dict {d2} missing CurrencyUnitGtEnumSymbol")
        if (
            d2["CurrencyUnitGtEnumSymbol"]
            in RecognizedCurrencyUnit000SchemaEnum.symbols
        ):
            d2["CurrencyUnit"] = RecognizedCurrencyUnitMap.type_to_local(
                d2["CurrencyUnitGtEnumSymbol"]
            )
        else:
            d2["CurrencyUnit"] = RecognizedCurrencyUnit.default()
        if "TypeName" not in d2.keys():
            raise SchemaError(f"dict {d2} missing TypeName")

        return FloParamsSimpleresistivehydronic(
            GNodeAlias=d2["GNodeAlias"],
            FloParamsUid=d2["FloParamsUid"],
            HomeCity=d2["HomeCity"],
            TimezoneString=d2["TimezoneString"],
            StartYearUtc=d2["StartYearUtc"],
            StartMonthUtc=d2["StartMonthUtc"],
            StartDayUtc=d2["StartDayUtc"],
            StartHourUtc=d2["StartHourUtc"],
            StartMinuteUtc=d2["StartMinuteUtc"],
            StoreSizeGallons=d2["StoreSizeGallons"],
            MaxStoreTempF=d2["MaxStoreTempF"],
            ElementMaxPowerKw=d2["ElementMaxPowerKw"],
            RequiredSourceWaterTempF=d2["RequiredSourceWaterTempF"],
            FixedPumpGpm=d2["FixedPumpGpm"],
            ReturnWaterFixedDeltaT=d2["ReturnWaterFixedDeltaT"],
            SliceDurationMinutes=d2["SliceDurationMinutes"],
            PowerLostFromHouseKwList=d2["PowerLostFromHouseKwList"],
            OutsideTempF=d2["OutsideTempF"],
            DistributionPrice=d2["DistributionPrice"],
            RealtimeElectricityPrice=d2["RealtimeElectricityPrice"],
            RtElecPriceUid=d2["RtElecPriceUid"],
            WeatherUid=d2["WeatherUid"],
            DistPriceUid=d2["DistPriceUid"],
            CurrencyUnit=d2["CurrencyUnit"],
            TypeName=d2["TypeName"],
            Version="000",
        )
