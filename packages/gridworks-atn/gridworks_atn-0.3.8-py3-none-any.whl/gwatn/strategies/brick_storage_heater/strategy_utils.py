from typing import List
from typing import Optional
from typing import cast

from pydantic import BaseModel

from gwatn.atn_utils import DUMMY_TERMINALASSET_ALIAS
from gwatn.atn_utils import is_dummy_flo_params
from gwatn.brick_storage_heater.flo import Flo__BrickStorageHeater as Flo
from gwatn.types import AtnBid
from gwatn.types import AtnParamsBrickstorageheater as AtnParams
from gwatn.types import AtnParamsBrickstorageheater_Maker as AtnParams_Maker
from gwatn.types import FloParams
from gwatn.types import FloParamsBrickstorageheater
from gwatn.types import MarketSlot


class SlotStuff(BaseModel):
    Slot: MarketSlot
    BidParams: Optional[FloParamsBrickstorageheater] = None
    Flo: Optional[Flo] = None
    Bid: Optional[AtnBid] = None
    Price: Optional[float] = None


def dummy_bid() -> AtnBid:
    return AtnBid(
        BidderAlias="d1.isone.dummy.ta",
    )


def dummy_slot_stuff(slot: MarketSlot) -> SlotStuff:
    return SlotStuff(
        Slot=slot, FloStartIdx=50, BidParams=dummy_flo_params(), AtnBid=dummy_bid()
    )


def is_dummy_slot_stuff(bid_stuff: SlotStuff) -> bool:
    if is_dummy_flo_params(cast(FloParams, bid_stuff.BidParams)):
        return True
    return False


def dummy_atn_params() -> AtnParams:
    return AtnParams(GNodeAlias=DUMMY_TERMINALASSET_ALIAS)


def dummy_flo_params() -> FloParamsBrickstorageheater:
    return FloParamsBrickstorageheater(
        GNodeAlias=DUMMY_TERMINALASSET_ALIAS,
        FloParamsUid="00000000-0000-0000-0000-000000000000",
        RtElecPriceUid="00000000-0000-0000-0000-000000000000",
        WeatherUid="00000000-0000-0000-0000-000000000000",
    )


def get_max_store_kwh_th(max_brick_temp_c: int, c: float, room_temp_f: int) -> float:
    """Use max store temp, room temp, and CF to get max store energy in kWh_th"""
    room_temp_c = (room_temp_f - 32) * 5 / 9
    return (max_brick_temp_c - room_temp_c) * c


def get_house_worst_case_heat_output_avg_kw(
    house_worst_case_temp_f: int,
    room_temp_f: int,
    ambient_power_in_kw: float,
    outside_temp_f_list: List[int],
    power_required_by_house_from_system_avg_kw_list: List[float],
) -> float:
    design_t = house_worst_case_temp_f
    this_run_t = min(outside_temp_f_list)
    room_t = room_temp_f
    p = power_required_by_house_from_system_avg_kw_list
    this_run_max_system_kw = max(p)
    this_run_max_kw_in = this_run_max_system_kw + ambient_power_in_kw
    dd_max_kw_in = this_run_max_kw_in * (room_t - design_t) / (room_t - this_run_t)
    return dd_max_kw_in - ambient_power_in_kw
