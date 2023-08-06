"""Settings for the GridWorks Scada, readable from environment and/or from env files."""
from pydantic import BaseSettings
from satn.enums import ShDistPumpFeedbackModel
from satn.enums import ShMixingValveFeedbackModel


DEFAULT_ENV_FILE = "../tea_settings/heatpumpwithbooststore.env"


class TeaParams(BaseSettings):
    """Settings for the HeatPumpWithBoostStore Technoeconomic analysis."""

    house_worst_case_temp_f: int = -7
    emitter_max_safe_swt_f: int = 160
    system_max_heat_output_swt_f: int = 150
    circulator_pump_max_gpm: float = 6
    system_max_heat_output_delta_temp_f: int
    system_max_heat_output_gpm: float
    max_store_temp_f: int = 210
    room_temp_f: int = 70
    ambient_power_in_kw: float = 1.14
    flo_total_time_hrs: int = 48
    export_graph: bool = False
    storage_steps: int = 100
    edge_options: int = 2
    price_csv_starting_offset_hours: int = 0
    timezone_string: str = "US/Eastern"
    zero_heat_delta_f: int = 3
    max_heatpump_source_water_temp_f: int = 140
    design_day_temp_f: int = -7
    store_size_gallons: int = 240
    rated_heatpump_electricity_kw: float = 5.5
    store_max_power_kw: float = 9
    cop_1_temp_f: int = 0
    cop_4_temp_f: int = 50
    store_passive_loss_ratio: float = 0.003
    house_no_energy_needed_temp_f: int = 65
    space_heat_thermostat_setpoint_f: int = 68
    annual_hvac_kwh_th: int = 25000
    annual_solar_gain_kwh_th: int = 5000
    ambient_temp_store_f: int = 65
    currency_unit: str = "USD"
    temp_unit: str = "F"
    home_city: str = "MILLINOCKET_ME"
    standard_offer_price_dollars_per_mwh: float = 110
    flat_tariff_dollars_per_mwh: float = 70
    real_time_electricity_price_type_name: str = "csv.eprt.sync.1_0_0"
    real_time_electricity_price_csv: str = "../gridworks-ps/input_data/electricity_prices/isone/eprt__w.isone.stetson__2020.csv"
    dist_price_type_name: str = "csv.distp.sync.1_0_0"
    dist_price_csv: str = "input_data/electricity_prices/isone/distp__w.isone.stetson__2020__gw.me.versant.a1.res.ets.csv"
    weather_type_name: str = "csv.weather.forecast.sync.1_0_0"
    weather_csv: str = (
        "input_data/weather/us/me/temp__ws.us.me.millinocketairport__2020.csv"
    )
    scaled_heat_profile_csv: str = "input_data/misc/millinocket_heat_profile_2020.csv"
    zero_potential_energy_water_temp_f: int = 100
    emitter_pump_feedback_model_value: ShDistPumpFeedbackModel = (
        ShDistPumpFeedbackModel.ConstantGpm.value
    )
    mixing_valve_feedback_model_value: ShMixingValveFeedbackModel = (
        ShMixingValveFeedbackModel.ConstantSwt.value
    )
    cautious_mixing_valve_temp_delta_f: int = 5
    heatpump_tariff_value: str = "CmpHeatTariff"
    heatpump_energy_supply_type_value: str = "StandardOffer"
    boost_tariff_value: str = "CmpStorageHeatTariff"
    boost_energy_supply_type_value: str = "RealtimeLocalLmp"
    # When this is uncommented, timezone_string disappears
    # @validator('timezone_string')
    # def is_recognized_timezone(cls, v):
    #     assert pytz.timezone(v)

    class Config:
        env_prefix = "TEA_"
        env_nested_delimiter = "__"
        use_enum_values = True
