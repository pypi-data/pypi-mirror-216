from typing import Optional

import gridworks.conversion_factors as cf  # TODO change to from gwatn import conversion_factors as cf
import numpy as np
from pydantic import BaseModel
from satn.strategies.heatpumpwithbooststore.flo import (
    Flo__HeatpumpWithBoostStore as Flo,
)
from satn.types import AtnParamsHeatpumpwithbooststore as AtnParams
from satn.types import FloParamsHeatpumpwithbooststore as FloParams

from gwatn import atn_utils
from gwatn.types import AtnBid
from gwatn.types import MarketSlot


#################################
# Bidding related
#################################


class CostAndQuantityBought(BaseModel):
    QuantityBought: float
    Cost: float


class SlotStuff(BaseModel):
    Slot: MarketSlot
    BidParams: Optional[FloParams] = None
    Flo: Optional[Flo] = None
    Bid: Optional[AtnBid] = None
    Price: Optional[float] = None


def dummy_bid() -> AtnBid:
    return AtnBid(
        BidderAlias="d1.isone.dummy.ta",
        BidderGNodeInstanceId="00000000-0000-0000-0000-000000000000",
        MarketSlotName="rt60gate30b.d1.isone.ver.keene.1577836800",
        PqPairs=[],
        SignedMarketFeeTxn=atn_utils.DUMMY_ALGO_TXN,
    )


def dummy_atn_params() -> AtnParams:
    return AtnParams(
        SliceDurationMinutes=60,
        FloSlices=48,
        GNodeAlias="d1.isone.dummy.ta",
        GNodeInstanceId="00000000-0000-0000-0000-000000000000",
        TypeName="atn.params.heatpumpwithbooststore",
        Version="000",
    )


def dummy_flo_params() -> FloParams:
    return FloParams(
        GNodeAlias="d1.isone.dummy.ta",
        FloParamsUid="00000000-0000-0000-0000-000000000000",
        RtElecPriceUid="00000000-0000-0000-0000-000000000000",
        WeatherUid="00000000-0000-0000-0000-000000000000",
    )


def dummy_slot_stuff(slot: MarketSlot) -> SlotStuff:
    return SlotStuff(
        Slot=slot, FloStartIdx=50, BidParams=dummy_flo_params(), AtnBid=dummy_bid()
    )


def is_dummy_slot_stuff(bid_stuff: SlotStuff) -> bool:
    if is_dummy_flo_params(bid_stuff.BidParams):
        return True
    return False


def is_dummy_atn_params(atn_params: AtnParams) -> bool:
    if atn_params.GNodeAlias == "d1.isone.dummy.ta":
        return True
    return False


def is_dummy_flo_params(flo_params: FloParams) -> bool:
    if flo_params.RtElecPriceUid == "00000000-0000-0000-0000-000000000000":
        return True
    return False


##########################################
# Flo prep (uses AtnParams as variable)
##########################################


def get_k(
    system_max_heat_output_delta_temp_f: int,
    system_max_heat_output_gpm: float,
    system_max_heat_output_swt_f: int,
    room_temp_f: int,
) -> float:
    dt = system_max_heat_output_delta_temp_f
    gpm = system_max_heat_output_gpm
    swt = system_max_heat_output_swt_f
    rt = room_temp_f
    return float(gpm * np.log(1 - dt / (swt - rt)))


def get_system_max_heat_output_kw_avg(
    system_max_heat_output_gpm: float, system_max_heat_output_delta_temp_f: float
) -> float:
    """What is the max heat that the system put out?  ASSUMES that the hydronic
    fluid is water.

    Args:
        tea_params: Uses the system_max_heat_output_delta_temp_f and
        the system_max_heat_output_gpm.

    Returns:
        float: max heat ouput of the heating system, in kw
    """
    gpm = system_max_heat_output_gpm
    delta_temp = system_max_heat_output_delta_temp_f
    c = cf.POUNDS_OF_WATER_PER_GALLON * cf.MINUTES_PER_HOUR / cf.BTU_PER_KWH
    if gpm == 0 or delta_temp == 0:
        raise Exception(
            f"max gpm is {gpm}, max delta_temp is {delta_temp}. Cannot calculate system heat output."
        )
    pwr = c * delta_temp * gpm
    return pwr
