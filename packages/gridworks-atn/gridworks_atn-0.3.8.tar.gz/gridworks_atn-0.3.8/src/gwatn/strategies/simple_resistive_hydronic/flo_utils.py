from typing import List

import gridworks.conversion_factors as cf  # TODO change to from gwatn import conversion_factors as cf
from satn.enums import ShDistPumpFeedbackModel
from satn.enums import ShMixingValveFeedbackModel
from satn.types import FloParamsHeatpumpwithbooststore as FloParams

import gwatn.errors as errors


def get_max_store_kwh_th(params: FloParams) -> float:
    """Can be duck-typed with AtnParams as well"""
    return (
        cf.KWH_TH_PER_GALLON_PER_DEG_F
        * params.StoreSizeGallons
        * (params.MaxStoreTempF - params.ZeroPotentialEnergyWaterTempF)
    )


def get_house_worst_case_heat_output_avg_kw(params: FloParams) -> float:
    design_t = params.HouseWorstCaseTempF
    this_run_t = min(params.OutsideTempF)
    room_t = params.RoomTempF
    p = params.PowerRequiredByHouseFromSystemAvgKwList
    this_run_max_system_kw = max(p)
    this_run_max_kw_in = this_run_max_system_kw + params.AmbientPowerInKw
    dd_max_kw_in = this_run_max_kw_in * (room_t - design_t) / (room_t - this_run_t)
    return dd_max_kw_in - params.AmbientPowerInKw


def get_source_water_temp_f_list(params: FloParams) -> List[float]:
    """The SourceWaterTemp or SWT is the water in the hydronic pipes
    going into the emitters, after the mixing valve. This
    temperature is determined by the outside temperature and
    is regulated by the emitter circulator pump feedback mechanism and,
    when the SWT is above the MaxHeatPumpSourceWaterTempF, the mixing valve
    that mixes the water coming from the boost and the
    IntermediateWaterTemp (see graphic in explanatory artifact)

    Explanatory artifact: LINK

    Args:
        params: TeaParams.
        power_required_by_house_from_system_avg_kw: A list (by time slice) of the
        power required by the house from the system. This will be less than the
        the actual power required by the house by the ambient power supplied from
        other sources (other electrical appliances, ambient solar, animals)
    """

    swt: List[float] = []
    system_heat_list = params.PowerRequiredByHouseFromSystemAvgKwList
    for i in range(len(system_heat_list)):
        system_heat_avg_kw = system_heat_list[i]
        try:
            this_slice_swt = get_source_water_temp_f(
                params=params, system_heat_kw=system_heat_avg_kw
            )
        except errors.PhysicalSystemFailure:
            raise Exception(
                f"Trouble for slice {i} and system_heat_avg_kw {system_heat_avg_kw}"
            )
        swt.append(this_slice_swt)
    swt.append(params.ZeroPotentialEnergyWaterTempF)
    return swt


def get_source_water_temp_f(params: FloParams, system_heat_kw: float) -> float:
    """Returns SourceWaterTempF for given this system_heat_avg_kw,
        and ShDistPumpFeedbackModel of ConstantGpm. Does not
        let SourceWaterTempF go below params.ZeroPotentialEnergyWaterTempF

    Args:
        params (FloParams): Params for the Flo.
        system_heat_avg_kw (float): the heat the system is putting
        into the house

    Raises:
        errors.PhysicalSystemFailure: raised if derived
        SourceWaterTempF exceeds EmitterMaxSafeSwtF

    Returns:
        float: SourceWaterTempF
    """
    if system_heat_kw < 0:
        raise Exception(f"System does not TAKE heat from house")
    if system_heat_kw == 0:
        return params.ZeroPotentialEnergyWaterTempF
    if params.DistPumpFeedbackModel == ShDistPumpFeedbackModel.ConstantDeltaT:
        return get_constant_delta_t_swt(params=params, system_heat_kw=system_heat_kw)
    else:
        return get_constant_gpm_swt(params=params, system_heat_kw=system_heat_kw)


def get_constant_gpm_swt(params: FloParams, system_heat_kw: float) -> float:
    """Returns SourceWaterTempF for given this system_heat_avg_kw,
        and ShDistPumpFeedbackModel of ConstantGpm. Does not
        let SourceWaterTempF go below params.ZeroPotentialEnergyWaterTempF.

    Args:
        params (FloParams): Params for the Flo. Uses
            - RoomTempF
            - SystemMaxHeatOutputDeltaTempF
            - EmitterMaxSafeSwtF
            - SystemMaxHeatOutputSwtF
            - SystemMaxHeatOutputGpm
            system_heat_avg_kw (float): The heat provided by the system
            into the house
        system_heat_avg_kw (float): the heat the system ixs putting
        into the house

    Raises:
        errors.PhysicalSystemFailure: raised if derived
        SourceWaterTempF exceeds EmitterMaxSafeSwtF

    Returns:
        float: SourceWaterTempF
    """
    rt = params.RoomTempF
    ddd = params.SystemMaxHeatOutputDeltaTempF
    dd_gpm = params.SystemMaxHeatOutputGpm
    c = cf.POUNDS_OF_WATER_PER_GALLON * cf.MINUTES_PER_HOUR / cf.BTU_PER_KWH
    dd_swt = params.SystemMaxHeatOutputSwtF
    denominator = c * dd_gpm * (1 - (dd_swt - rt - ddd) / (dd_swt - rt))
    constant_running_swt = rt + (system_heat_kw / denominator)
    constant_running_swt = max(
        constant_running_swt, params.ZeroPotentialEnergyWaterTempF
    )

    if params.MixingValveFeedbackModel == ShMixingValveFeedbackModel.ConstantSwt:
        return params.SystemMaxHeatOutputSwtF
    elif params.MixingValveFeedbackModel == ShMixingValveFeedbackModel.NaiveVariableSwt:
        if constant_running_swt > params.EmitterMaxSafeSwtF:
            raise errors.PhysicalSystemFailure(
                "Pump strategy: ConstantGpm. MixingValve: "
                f"NaiveVariable.  Constant running swt {constant_running_swt} F exceeds"
                f" EmitterMaxSafeSwtF {params.EmitterMaxSafeSwtF}!"
            )
        return constant_running_swt
    elif (
        params.MixingValveFeedbackModel
        == ShMixingValveFeedbackModel.CautiousVariableSwt
    ):
        cautious_swt = constant_running_swt + params.CautiousMixingValveTempDeltaF
        if cautious_swt > params.EmitterMaxSafeSwtF:
            raise errors.PhysicalSystemFailure(
                "Pump strategy: ConstantGpm. MixingValve: "
                f"CautiousVariable.  Cautious {cautious_swt} F  (hotter by {params.CautiousMixingValveTempDeltaF}"
                f" than constant running temp) exceeds"
                f" EmitterMaxSafeSwtF {params.EmitterMaxSafeSwtF}!"
            )
        return cautious_swt
    else:
        raise Exception(
            f"Unknown ShMixingValveFeedbackModel {params.MixingValveFeedbackModel}"
        )


def get_constant_delta_t_swt(params: FloParams, system_heat_kw: float) -> float:
    """Calculates Source Water Temp (SWT) for a system with
        a constant delta T feedback control mechanism for its circulator
        pump/thermostat. Does not
        let SourceWaterTempF go below params.ZeroPotentialEnergyWaterTempF.

        params (FloParams): Params for the Flo. Uses
            - RoomTempF
            - SystemMaxHeatOutputDeltaTempF
            - EmitterMaxSafeSwtF
            - SystemMaxHeatOutputSwtF
            - SystemMaxHeatOutputGpm
            system_heat_avg_kw (float): The heat provided by the system
            into the house
        system_heat_avg_kw (float): the heat the system is putting
        into the house

        Raises:
        errors.PhysicalSystemFailure: raised if derived
        SourceWaterTempF exceeds EmitterMaxSafeSwtF

    Returns:
        float: SourceWaterTempF
    """
    p_req = system_heat_kw
    if p_req <= 0:
        return params.ZeroPotentialEnergyWaterTempF
    rt = params.RoomTempF
    ddd = params.SystemMaxHeatOutputDeltaTempF

    max_e_out = params.SystemMaxHeatOutputKwAvg
    dd_swt = params.SystemMaxHeatOutputSwtF
    base = (dd_swt - rt - ddd) / (dd_swt - rt)
    exp = max_e_out / p_req

    numerator = rt + ddd - rt * (base**exp)
    denominator = 1 - (base**exp)
    if denominator == 0:
        raise Exception(f"About to divide by zero. base = {base} exp = {exp}")
    constant_running_swt: float = numerator / denominator
    constant_running_swt = max(
        constant_running_swt, params.ZeroPotentialEnergyWaterTempF
    )
    if params.MixingValveFeedbackModel == ShMixingValveFeedbackModel.ConstantSwt:
        return params.SystemMaxHeatOutputSwtF
    elif params.MixingValveFeedbackModel == ShMixingValveFeedbackModel.NaiveVariableSwt:
        if constant_running_swt > params.EmitterMaxSafeSwtF:
            raise errors.PhysicalSystemFailure(
                "Pump: ConstantDeltaT, MixingValve: "
                f"NaiveVariable. {constant_running_swt} F exceeds"
                f" EmitterMaxSafeSwtF {params.EmitterMaxSafeSwtF}!"
            )

        return constant_running_swt
    elif (
        params.MixingValveFeedbackModel
        == ShMixingValveFeedbackModel.CautiousVariableSwt
    ):
        cautious_swt: float = (
            constant_running_swt + params.CautiousMixingValveTempDeltaF
        )
        if cautious_swt > params.EmitterMaxSafeSwtF:
            raise errors.PhysicalSystemFailure(
                "Pump strategy: ConstantDeltaT. MixingValve: "
                f"CautiousVariable. Cautious {cautious_swt} F  (hotter by {params.CautiousMixingValveTempDeltaF}"
                f" than constant running temp) exceeds"
                f" EmitterMaxSafeSwtF {params.EmitterMaxSafeSwtF}!"
            )
        return cautious_swt
    else:
        raise Exception(
            f"Unknown ShMixingValveFeedbackModel {params.MixingValveFeedbackModel}"
        )
