import csv
import uuid
from typing import List

import numpy as np
import pendulum
import satn.dev_utils.price.distp_sync_100_handler as distp_sync_100_handler
import satn.dev_utils.price.eprt_sync_100_handler as eprt_sync_100_handler
import satn.dev_utils.weather.weather_forecast_sync_100_handler as weather_forecast_sync_100_handler
import satn.strategies.heatpumpwithbooststore.flo_utils as flo_utils
import satn.strategies.heatpumpwithbooststore.strategy_utils as strategy_utils
from satn.enums import ShDistPumpFeedbackModel
from satn.enums import ShMixingValveFeedbackModel
from satn.strategies.heatpumpwithbooststore.flo import Flo__HeatpumpWithBoostStore
from satn.strategies.heatpumpwithbooststore.tea_config import TeaParams
from satn.strategies.heatpumpwithbooststore.tea_output import export_xlsx
from satn.types.flo_params_heatpumpwithbooststore import (
    FloParamsHeatpumpwithbooststore as FloParams,
)

import gwatn.errors as errors
from gwatn.enums import DistributionTariff
from gwatn.enums import EnergySupplyType
from gwatn.enums import RecognizedCurrencyUnit
from gwatn.enums import RecognizedTemperatureUnit
from gwatn.types.ps_distprices_gnode.r_distp_sync.r_distp_sync_1_0_0 import (
    Payload as DistpSync100Payload,
)
from gwatn.types.ps_electricityprices_gnode.r_eprt_sync.r_eprt_sync_1_0_0 import (
    Payload as EprtSync100Payload,
)
from gwatn.types.ws_forecast_gnode.r_weather_forecast_sync.r_weather_forecast_sync_1_0_0 import (
    Payload as RWeatherForecastSync100Payload,
)


def get_electricity_prices(tea_params: TeaParams) -> EprtSync100Payload:
    ep = eprt_sync_100_handler.payload_from_file(
        eprt_type_name=tea_params.real_time_electricity_price_type_name,
        eprt_csv=tea_params.real_time_electricity_price_csv,
        csv_starting_offset_hours=tea_params.price_csv_starting_offset_hours,
        flo_total_time_hrs=tea_params.flo_total_time_hrs,
    )
    if ep.CurrencyUnit != tea_params.currency_unit:
        raise Exception(
            f"Currency unit for {tea_params.real_time_electricity_price_csv} does not match params.currency_unit of {tea_params.currency_unit}"
        )
    return ep


def get_flo_start_utc(tea_params: TeaParams) -> pendulum.datetime:
    ep = get_electricity_prices(tea_params)
    return pendulum.datetime(
        year=ep.StartYearUtc,
        month=ep.StartMonthUtc,
        day=ep.StartDayUtc,
        hour=ep.StartHourUtc,
        minute=ep.StartMinuteUtc,
    )


def get_distribution_prices(
    tea_params: TeaParams, flo_start_utc: pendulum.datetime
) -> DistpSync100Payload:
    dp = distp_sync_100_handler.payload_from_file(
        distp_type_name=tea_params.dist_price_type_name,
        distp_csv=tea_params.dist_price_csv,
        flo_start_utc=flo_start_utc,
        flo_total_time_hrs=tea_params.flo_total_time_hrs,
    )
    if dp.CurrencyUnit != tea_params.currency_unit:
        raise Exception(
            f"currency unit for {tea_params.dist_price_type_name} does not match params.currency_unit of {tea_params.currency_unit}"
        )
    return dp


def get_weather_forecasts(
    tea_params: TeaParams, flo_start_utc: pendulum.datetime
) -> RWeatherForecastSync100Payload:
    wp = weather_forecast_sync_100_handler.payload_from_file(
        file_name=tea_params.weather_csv,
        request_start_datetime_utc=flo_start_utc,
        total_time_hrs=tea_params.flo_total_time_hrs,
    )
    if wp.TempUnit != tea_params.temp_unit:
        raise Exception(
            f"temp unit for {tea_params.weather_csv} does not match params.temp_unit of {tea_params.temp_unit}"
        )
    return wp


def get_desired_heat_from_csv(tea_params: TeaParams) -> List[float]:
    ep = get_electricity_prices(tea_params)
    if tea_params.price_csv_starting_offset_hours != 0:
        raise NotImplementedError(
            f"heat profile has not been adjusted to offsets from start of year"
        )

    with open(tea_params.scaled_heat_profile_csv, newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        p = []
        for row in reader:
            p.append(float(row[0]))
    if len(p) != 8784:
        raise Exception(
            f"scaled heat profile {tea_params.scaled_heat_profile_csv} should have 8784 hours"
        )
    annual_desired_house_heat_profile = (
        tea_params.annual_hvac_kwh_th * np.array(p)
    ).tolist()
    return annual_desired_house_heat_profile[0 : len(ep.Prices)]


def get_flo_params(tea_params: TeaParams) -> FloParams:
    ep = get_electricity_prices(tea_params)
    flo_start_utc = get_flo_start_utc(tea_params)
    dp = get_distribution_prices(tea_params, flo_start_utc)
    weather = get_weather_forecasts(tea_params, flo_start_utc)
    pump_model = ShDistPumpFeedbackModel(tea_params.emitter_pump_feedback_model_value)
    mixing_valve_model = ShMixingValveFeedbackModel(
        tea_params.mixing_valve_feedback_model_value
    )
    # PowerRequiredByHouseFromSystemAvgKw
    power_required_by_house_from_system_avg_kw_list: List[
        float
    ] = get_desired_heat_from_csv(tea_params)

    flo_params = FloParams(
        GNodeAlias="d1.tea.atn",
        FloParamsUid=str(uuid.uuid4()),
        PowerRequiredByHouseFromSystemAvgKwList=power_required_by_house_from_system_avg_kw_list,
        HouseWorstCaseTempF=tea_params.house_worst_case_temp_f,
        EmitterMaxSafeSwtF=tea_params.emitter_max_safe_swt_f,
        CirculatorPumpMaxGpm=tea_params.circulator_pump_max_gpm,
        SystemMaxHeatOutputKwAvg=strategy_utils.get_system_max_heat_output_kw_avg(
            system_max_heat_output_gpm=tea_params.system_max_heat_output_gpm,
            system_max_heat_output_delta_temp_f=tea_params.system_max_heat_output_delta_temp_f,
        ),
        RtElecPriceUid=ep.PriceUid,
        DistPriceUid=dp.PriceUid,
        RegPriceUid=None,
        WeatherUid=weather.WeatherUid,
        K=strategy_utils.get_k(
            system_max_heat_output_delta_temp_f=tea_params.system_max_heat_output_delta_temp_f,
            system_max_heat_output_gpm=tea_params.system_max_heat_output_gpm,
            system_max_heat_output_swt_f=tea_params.system_max_heat_output_swt_f,
            room_temp_f=tea_params.room_temp_f,
        ),
        StartYearUtc=ep.StartYearUtc,
        StartMonthUtc=ep.StartMonthUtc,
        StartDayUtc=ep.StartDayUtc,
        StartHourUtc=ep.StartHourUtc,
        StartMinuteUtc=ep.StartMinuteUtc,
        TimezoneString=tea_params.timezone_string,
        SliceDurationMinutes=[ep.UniformSliceDurationHrs * 60] * len(ep.Prices),
        HomeCity=tea_params.home_city,
        AmbientTempStoreF=tea_params.ambient_temp_store_f,
        StorePassiveLossRatio=tea_params.store_passive_loss_ratio,
        SystemMaxHeatOutputDeltaTempF=tea_params.system_max_heat_output_delta_temp_f,
        SystemMaxHeatOutputGpm=tea_params.system_max_heat_output_gpm,
        SystemMaxHeatOutputSwtF=tea_params.system_max_heat_output_swt_f,
        IsRegulating=False,
        OutsideTempF=weather.Temperatures,
        HeatpumpTariff=DistributionTariff(tea_params.heatpump_tariff_value),
        HeatpumpEnergySupplyType=EnergySupplyType(
            tea_params.heatpump_energy_supply_type_value
        ),
        BoostTariff=DistributionTariff(tea_params.boost_tariff_value),
        BoostEnergySupplyType=EnergySupplyType(
            tea_params.boost_energy_supply_type_value
        ),
        StandardOfferPriceDollarsPerMwh=tea_params.standard_offer_price_dollars_per_mwh,
        DistributionTariffDollarsPerMwh=tea_params.flat_tariff_dollars_per_mwh,
        RealtimeElectricityPrice=ep.Prices,
        DistributionPrice=dp.Prices,
        RoomTempF=tea_params.room_temp_f,
        AmbientPowerInKw=tea_params.ambient_power_in_kw,
        MaxHeatpumpSourceWaterTempF=tea_params.max_heatpump_source_water_temp_f,
        ZeroPotentialEnergyWaterTempF=tea_params.zero_potential_energy_water_temp_f,
        MaxStoreTempF=tea_params.max_store_temp_f,
        StorageSteps=tea_params.storage_steps,
        StoreSizeGallons=tea_params.store_size_gallons,
        RatedHeatpumpElectricityKw=tea_params.rated_heatpump_electricity_kw,
        StoreMaxPowerKw=tea_params.store_max_power_kw,
        DistPumpFeedbackModel=pump_model,
        MixingValveFeedbackModel=mixing_valve_model,
        CautiousMixingValveTempDeltaF=tea_params.cautious_mixing_valve_temp_delta_f,
        TempUnit=RecognizedTemperatureUnit(tea_params.temp_unit),
        CurrencyUnit=RecognizedCurrencyUnit(tea_params.currency_unit),
        StartingIdx=int(tea_params.storage_steps / 2),
        Cop1TempF=tea_params.cop_1_temp_f,
        Cop4TempF=tea_params.cop_4_temp_f,
        RegulationPrice=[],
    )

    return flo_params


def get_flo(flo_params: FloParams) -> Flo__HeatpumpWithBoostStore:
    return Flo__HeatpumpWithBoostStore(
        params=flo_params,
        d_graph_id=str(uuid.uuid4()),
    )


if __name__ == "__main__":
    tea_params = TeaParams(_env_file="tea_params/heatpumpwithbooststore.env")
    flo_params = get_flo_params(tea_params)
    p = flo_params.PowerRequiredByHouseFromSystemAvgKwList
    t = flo_params.OutsideTempF
    house_dd_max_heat_kw = flo_utils.get_house_worst_case_heat_output_avg_kw(flo_params)

    print(f"Max required heat this run: {round(max(p),2)} kW")
    print(f"Max required heat on design day:{round(house_dd_max_heat_kw,2)} kW")
    print(
        f"flo_params.SystemMaxHeatOutputKwAvg: {round(flo_params.SystemMaxHeatOutputKwAvg,2)} kW"
    )
    if max(p) > flo_params.SystemMaxHeatOutputKwAvg:
        # if house_dd_max_heat_kw > flo_params.SystemMaxHeatOutputKwAvg:
        raise errors.PhysicalSystemFailure(
            f"House requires {round(house_dd_max_heat_kw,2)} kW on the"
            f" design day but flo_params.SystemMaxHeatOutputKwAvg is only {round(flo_params.SystemMaxHeatOutputKwAvg,2)} kW!"
        )
    if flo_params.CirculatorPumpMaxGpm < flo_params.SystemMaxHeatOutputGpm:
        raise errors.PhysicalSystemFailure(
            f"CirculatorPumpMaxGpm {flo_params.CirculatorPumpMaxGpm} is less than"
            f" SystemMaxHeatOutputKwAvg {round(flo_params.SystemMaxHeatOutputKwAvg,2)}"
        )
    if (
        flo_params.MixingValveFeedbackModel
        == ShMixingValveFeedbackModel.NaiveVariableSwt
    ):
        if flo_params.EmitterMaxSafeSwtF < flo_params.SystemMaxHeatOutputSwtF:
            raise errors.PhysicalSystemFailure(
                f".EmitterMaxSafeSwtF {flo_params.EmitterMaxSafeSwtF} is less than"
                f" SystemMaxHeatOutputSwtF {round(flo_params.SystemMaxHeatOutputSwtF,1)}"
            )
    if (
        flo_params.MixingValveFeedbackModel
        == ShMixingValveFeedbackModel.CautiousVariableSwt
    ):
        if (
            flo_params.EmitterMaxSafeSwtF
            < flo_params.SystemMaxHeatOutputSwtF
            + flo_params.CautiousMixingValveTempDeltaF
        ):
            raise errors.PhysicalSystemFailure(
                "MixingValveModel: CautiousVariableSwt."
                f" EmitterMaxSafeSwtF {flo_params.EmitterMaxSafeSwtF} is less than"
                " SystemMaxHeatOutputSwtF - CautiousMixingValveTempDeltaF: "
                f"{round(flo_params.SystemMaxHeatOutputSwtF - flo_params.CautiousMixingValveTempDeltaF,1)}"
            )

    print(f"Coldest temp this run: {min(t)} F")
    print(f"Design day temp: {flo_params.HouseWorstCaseTempF} F")
    swt = flo_utils.get_source_water_temp_f_list(params=flo_params)

    print(f"Max swt : {round(max(swt),1)}")
    flo = get_flo(flo_params)

    if flo.node[0][50].path_cost > 100000:
        print("FAILED")
    export_xlsx(tea_params=tea_params, flo=flo, export_graph=tea_params.export_graph)
