"""Type atn.params.simpleresistivehydronic, version 000"""
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

from gwatn.enums import DistributionTariff
from gwatn.enums import EnergySupplyType
from gwatn.enums import RecognizedCurrencyUnit


class DistributionTariff000SchemaEnum:
    enum_name: str = "distribution.tariff.000"
    symbols: List[str] = [
        "00000000",
        "2127aba6",
        "ea5c675a",
        "54aec3a7",
    ]

    @classmethod
    def is_symbol(cls, candidate: str) -> bool:
        if candidate in cls.symbols:
            return True
        return False


class DistributionTariff000(StrEnum):
    Unknown = auto()
    VersantA1StorageHeatTariff = auto()
    VersantATariff = auto()
    VersantA20HeatTariff = auto()

    @classmethod
    def default(cls) -> "DistributionTariff000":
        return cls.Unknown

    @classmethod
    def values(cls) -> List[str]:
        return [elt.value for elt in cls]


class DistributionTariffMap:
    @classmethod
    def type_to_local(cls, symbol: str) -> DistributionTariff:
        if not DistributionTariff000SchemaEnum.is_symbol(symbol):
            raise SchemaError(f"{symbol} must belong to DistributionTariff000 symbols")
        versioned_enum = cls.type_to_versioned_enum_dict[symbol]
        return as_enum(versioned_enum, DistributionTariff, DistributionTariff.default())

    @classmethod
    def local_to_type(cls, distribution_tariff: DistributionTariff) -> str:
        if not isinstance(distribution_tariff, DistributionTariff):
            raise SchemaError(
                f"{distribution_tariff} must be of type {DistributionTariff}"
            )
        versioned_enum = as_enum(
            distribution_tariff, DistributionTariff000, DistributionTariff000.default()
        )
        return cls.versioned_enum_to_type_dict[versioned_enum]

    type_to_versioned_enum_dict: Dict[str, DistributionTariff000] = {
        "00000000": DistributionTariff000.Unknown,
        "2127aba6": DistributionTariff000.VersantA1StorageHeatTariff,
        "ea5c675a": DistributionTariff000.VersantATariff,
        "54aec3a7": DistributionTariff000.VersantA20HeatTariff,
    }

    versioned_enum_to_type_dict: Dict[DistributionTariff000, str] = {
        DistributionTariff000.Unknown: "00000000",
        DistributionTariff000.VersantA1StorageHeatTariff: "2127aba6",
        DistributionTariff000.VersantATariff: "ea5c675a",
        DistributionTariff000.VersantA20HeatTariff: "54aec3a7",
    }


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


class EnergySupplyType000SchemaEnum:
    enum_name: str = "energy.supply.type.000"
    symbols: List[str] = [
        "00000000",
        "cb18f937",
        "e9dc99a6",
    ]

    @classmethod
    def is_symbol(cls, candidate: str) -> bool:
        if candidate in cls.symbols:
            return True
        return False


class EnergySupplyType000(StrEnum):
    Unknown = auto()
    StandardOffer = auto()
    RealtimeLocalLmp = auto()

    @classmethod
    def default(cls) -> "EnergySupplyType000":
        return cls.Unknown

    @classmethod
    def values(cls) -> List[str]:
        return [elt.value for elt in cls]


class EnergySupplyTypeMap:
    @classmethod
    def type_to_local(cls, symbol: str) -> EnergySupplyType:
        if not EnergySupplyType000SchemaEnum.is_symbol(symbol):
            raise SchemaError(f"{symbol} must belong to EnergySupplyType000 symbols")
        versioned_enum = cls.type_to_versioned_enum_dict[symbol]
        return as_enum(versioned_enum, EnergySupplyType, EnergySupplyType.default())

    @classmethod
    def local_to_type(cls, energy_supply_type: EnergySupplyType) -> str:
        if not isinstance(energy_supply_type, EnergySupplyType):
            raise SchemaError(
                f"{energy_supply_type} must be of type {EnergySupplyType}"
            )
        versioned_enum = as_enum(
            energy_supply_type, EnergySupplyType000, EnergySupplyType000.default()
        )
        return cls.versioned_enum_to_type_dict[versioned_enum]

    type_to_versioned_enum_dict: Dict[str, EnergySupplyType000] = {
        "00000000": EnergySupplyType000.Unknown,
        "cb18f937": EnergySupplyType000.StandardOffer,
        "e9dc99a6": EnergySupplyType000.RealtimeLocalLmp,
    }

    versioned_enum_to_type_dict: Dict[EnergySupplyType000, str] = {
        EnergySupplyType000.Unknown: "00000000",
        EnergySupplyType000.StandardOffer: "cb18f937",
        EnergySupplyType000.RealtimeLocalLmp: "e9dc99a6",
    }


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


class AtnParamsSimpleresistivehydronic(BaseModel):
    """ """

    GNodeAlias: str = Field(
        title="GNodeAlias",
    )
    HomeCity: str = Field(
        title="HomeCity",
    )
    TimezoneString: str = Field(
        title="TimezoneString",
    )
    StorageSteps: int = Field(
        title="StorageSteps",
        default=100,
    )
    FloSlices: int = Field(
        title="FloSlices",
        default=48,
    )
    SliceDurationMinutes: int = Field(
        title="SliceDurationMinutes",
        default=60,
    )
    CurrencyUnit: RecognizedCurrencyUnit = Field(
        title="CurrencyUnit",
        default=RecognizedCurrencyUnit.USD,
    )
    Tariff: DistributionTariff = Field(
        title="Tariff",
        default=DistributionTariff.VersantA1StorageHeatTariff,
    )
    EnergyType: EnergySupplyType = Field(
        title="EnergyType",
        default=EnergySupplyType.RealtimeLocalLmp,
    )
    StandardOfferPriceDollarsPerMwh: int = Field(
        title="StandardOfferPriceDollarsPerMwh",
        default=110,
    )
    DistributionTariffDollarsPerMwh: int = Field(
        title="DistributionTariffDollarsPerMwh",
        default=113,
    )
    StoreSizeGallons: int = Field(
        title="StoreSizeGallons",
        default=240,
    )
    MaxStoreTempF: int = Field(
        title="MaxStoreTempF",
        default=210,
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
        default=5.5,
    )
    ReturnWaterFixedDeltaT: int = Field(
        title="ReturnWaterFixedDeltaT",
        default=20,
    )
    AnnualHvacKwhTh: int = Field(
        title="AnnualHvacKwhTh",
        default=25000,
    )
    AmbientPowerInKw: float = Field(
        title="AmbientPowerInKw",
        default=1.2,
    )
    HouseWorstCaseTempF: int = Field(
        title="HouseWorstCaseTempF",
        default=-7,
    )
    RoomTempF: int = Field(
        title="RoomTempF",
        default=68,
    )
    TypeName: Literal[
        "atn.params.simpleresistivehydronic"
    ] = "atn.params.simpleresistivehydronic"
    Version: str = "000"

    @validator("GNodeAlias")
    def _check_g_node_alias(cls, v: str) -> str:
        try:
            check_is_left_right_dot(v)
        except ValueError as e:
            raise ValueError(f"GNodeAlias failed LeftRightDot format validation: {e}")
        return v

    @validator("CurrencyUnit")
    def _check_currency_unit(cls, v: RecognizedCurrencyUnit) -> RecognizedCurrencyUnit:
        return as_enum(v, RecognizedCurrencyUnit, RecognizedCurrencyUnit.UNKNOWN)

    @validator("Tariff")
    def _check_tariff(cls, v: DistributionTariff) -> DistributionTariff:
        return as_enum(v, DistributionTariff, DistributionTariff.Unknown)

    @validator("EnergyType")
    def _check_energy_type(cls, v: EnergySupplyType) -> EnergySupplyType:
        return as_enum(v, EnergySupplyType, EnergySupplyType.Unknown)

    def as_dict(self) -> Dict[str, Any]:
        d = self.dict()
        del d["CurrencyUnit"]
        CurrencyUnit = as_enum(
            self.CurrencyUnit, RecognizedCurrencyUnit, RecognizedCurrencyUnit.default()
        )
        d["CurrencyUnitGtEnumSymbol"] = RecognizedCurrencyUnitMap.local_to_type(
            CurrencyUnit
        )
        del d["Tariff"]
        Tariff = as_enum(self.Tariff, DistributionTariff, DistributionTariff.default())
        d["TariffGtEnumSymbol"] = DistributionTariffMap.local_to_type(Tariff)
        del d["EnergyType"]
        EnergyType = as_enum(
            self.EnergyType, EnergySupplyType, EnergySupplyType.default()
        )
        d["EnergyTypeGtEnumSymbol"] = EnergySupplyTypeMap.local_to_type(EnergyType)
        return d

    def as_type(self) -> str:
        return json.dumps(self.as_dict())

    def __hash__(self):
        return hash((type(self),) + tuple(self.__dict__.values()))  # noqa


class AtnParamsSimpleresistivehydronic_Maker:
    type_name = "atn.params.simpleresistivehydronic"
    version = "000"

    def __init__(
        self,
        g_node_alias: str,
        home_city: str,
        timezone_string: str,
        storage_steps: int,
        flo_slices: int,
        slice_duration_minutes: int,
        currency_unit: RecognizedCurrencyUnit,
        tariff: DistributionTariff,
        energy_type: EnergySupplyType,
        standard_offer_price_dollars_per_mwh: int,
        distribution_tariff_dollars_per_mwh: int,
        store_size_gallons: int,
        max_store_temp_f: int,
        element_max_power_kw: float,
        required_source_water_temp_f: int,
        fixed_pump_gpm: float,
        return_water_fixed_delta_t: int,
        annual_hvac_kwh_th: int,
        ambient_power_in_kw: float,
        house_worst_case_temp_f: int,
        room_temp_f: int,
    ):
        self.tuple = AtnParamsSimpleresistivehydronic(
            GNodeAlias=g_node_alias,
            HomeCity=home_city,
            TimezoneString=timezone_string,
            StorageSteps=storage_steps,
            FloSlices=flo_slices,
            SliceDurationMinutes=slice_duration_minutes,
            CurrencyUnit=currency_unit,
            Tariff=tariff,
            EnergyType=energy_type,
            StandardOfferPriceDollarsPerMwh=standard_offer_price_dollars_per_mwh,
            DistributionTariffDollarsPerMwh=distribution_tariff_dollars_per_mwh,
            StoreSizeGallons=store_size_gallons,
            MaxStoreTempF=max_store_temp_f,
            ElementMaxPowerKw=element_max_power_kw,
            RequiredSourceWaterTempF=required_source_water_temp_f,
            FixedPumpGpm=fixed_pump_gpm,
            ReturnWaterFixedDeltaT=return_water_fixed_delta_t,
            AnnualHvacKwhTh=annual_hvac_kwh_th,
            AmbientPowerInKw=ambient_power_in_kw,
            HouseWorstCaseTempF=house_worst_case_temp_f,
            RoomTempF=room_temp_f,
            #
        )

    @classmethod
    def tuple_to_type(cls, tuple: AtnParamsSimpleresistivehydronic) -> str:
        """
        Given a Python class object, returns the serialized JSON type object
        """
        return tuple.as_type()

    @classmethod
    def type_to_tuple(cls, t: str) -> AtnParamsSimpleresistivehydronic:
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
    def dict_to_tuple(cls, d: dict[str, Any]) -> AtnParamsSimpleresistivehydronic:
        d2 = dict(d)
        if "GNodeAlias" not in d2.keys():
            raise SchemaError(f"dict {d2} missing GNodeAlias")
        if "HomeCity" not in d2.keys():
            raise SchemaError(f"dict {d2} missing HomeCity")
        if "TimezoneString" not in d2.keys():
            raise SchemaError(f"dict {d2} missing TimezoneString")
        if "StorageSteps" not in d2.keys():
            raise SchemaError(f"dict {d2} missing StorageSteps")
        if "FloSlices" not in d2.keys():
            raise SchemaError(f"dict {d2} missing FloSlices")
        if "SliceDurationMinutes" not in d2.keys():
            raise SchemaError(f"dict {d2} missing SliceDurationMinutes")
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
        if "TariffGtEnumSymbol" not in d2.keys():
            raise SchemaError(f"dict {d2} missing TariffGtEnumSymbol")
        if d2["TariffGtEnumSymbol"] in DistributionTariff000SchemaEnum.symbols:
            d2["Tariff"] = DistributionTariffMap.type_to_local(d2["TariffGtEnumSymbol"])
        else:
            d2["Tariff"] = DistributionTariff.default()
        if "EnergyTypeGtEnumSymbol" not in d2.keys():
            raise SchemaError(f"dict {d2} missing EnergyTypeGtEnumSymbol")
        if d2["EnergyTypeGtEnumSymbol"] in EnergySupplyType000SchemaEnum.symbols:
            d2["EnergyType"] = EnergySupplyTypeMap.type_to_local(
                d2["EnergyTypeGtEnumSymbol"]
            )
        else:
            d2["EnergyType"] = EnergySupplyType.default()
        if "StandardOfferPriceDollarsPerMwh" not in d2.keys():
            raise SchemaError(f"dict {d2} missing StandardOfferPriceDollarsPerMwh")
        if "DistributionTariffDollarsPerMwh" not in d2.keys():
            raise SchemaError(f"dict {d2} missing DistributionTariffDollarsPerMwh")
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
        if "AnnualHvacKwhTh" not in d2.keys():
            raise SchemaError(f"dict {d2} missing AnnualHvacKwhTh")
        if "AmbientPowerInKw" not in d2.keys():
            raise SchemaError(f"dict {d2} missing AmbientPowerInKw")
        if "HouseWorstCaseTempF" not in d2.keys():
            raise SchemaError(f"dict {d2} missing HouseWorstCaseTempF")
        if "RoomTempF" not in d2.keys():
            raise SchemaError(f"dict {d2} missing RoomTempF")
        if "TypeName" not in d2.keys():
            raise SchemaError(f"dict {d2} missing TypeName")

        return AtnParamsSimpleresistivehydronic(
            GNodeAlias=d2["GNodeAlias"],
            HomeCity=d2["HomeCity"],
            TimezoneString=d2["TimezoneString"],
            StorageSteps=d2["StorageSteps"],
            FloSlices=d2["FloSlices"],
            SliceDurationMinutes=d2["SliceDurationMinutes"],
            CurrencyUnit=d2["CurrencyUnit"],
            Tariff=d2["Tariff"],
            EnergyType=d2["EnergyType"],
            StandardOfferPriceDollarsPerMwh=d2["StandardOfferPriceDollarsPerMwh"],
            DistributionTariffDollarsPerMwh=d2["DistributionTariffDollarsPerMwh"],
            StoreSizeGallons=d2["StoreSizeGallons"],
            MaxStoreTempF=d2["MaxStoreTempF"],
            ElementMaxPowerKw=d2["ElementMaxPowerKw"],
            RequiredSourceWaterTempF=d2["RequiredSourceWaterTempF"],
            FixedPumpGpm=d2["FixedPumpGpm"],
            ReturnWaterFixedDeltaT=d2["ReturnWaterFixedDeltaT"],
            AnnualHvacKwhTh=d2["AnnualHvacKwhTh"],
            AmbientPowerInKw=d2["AmbientPowerInKw"],
            HouseWorstCaseTempF=d2["HouseWorstCaseTempF"],
            RoomTempF=d2["RoomTempF"],
            TypeName=d2["TypeName"],
            Version="000",
        )
