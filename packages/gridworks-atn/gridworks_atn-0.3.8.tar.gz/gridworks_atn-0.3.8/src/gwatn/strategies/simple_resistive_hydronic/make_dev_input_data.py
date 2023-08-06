import csv
import json

import pendulum
from satn.types import AtnParamsHeatpumpwithbooststore as AtnParams
from satn.types import AtnParamsHeatpumpwithbooststore_Maker as AtnParams_Maker

from gwatn.types import AtnParamsReport_Maker


params_file = "input_data/atn_params_data.csv"
params = []
with open(params_file) as csv_file:
    reader = csv.reader(csv_file)
    for row in reader:
        params.append(row)
start = pendulum.datetime(year=2020, month=1, day=1, hour=4)

for j in range(1, 19):
    alias = params[1][j]
    atn_params = AtnParams(
        GNodeAlias=alias,
        BetaOt=params[2][j],
        HouseHeatingCapacity=params[3][j],
        AmbientPowerInKw=params[4][j],
        AnnualHvacKwhTh=params[5][j],
        StoreSizeGallons=params[8][j],
        RatedHeatpumpElectricityKw=params[9][j],
        StoreMaxPowerKw=params[10][j],
        SystemMaxHeatOutputDeltaTempF=params[11][j],
        SystemMaxHeatOutputGpm=params[12][j],
        SystemMaxHeatOutputSwtF=params[13][j],
        FloSlices=48,
        SliceDurationMinutes=60,
    )

    params_dict = atn_params.as_dict()
    try:
        report = AtnParamsReport_Maker(
            g_node_alias=alias,
            g_node_instance_id="00000000-0000-0000-0000-000000000000",
            atn_params_type_name=AtnParams_Maker.type_name,
            time_unix_s=start.int_timestamp,
            params=atn_params,
            irl_time_unix_s=None,
        ).tuple
    except:
        print(f"Problem with {alias}")

    file_name = f"input_data/eventstore/{alias}-{AtnParamsReport_Maker.type_name}-{start.int_timestamp * 1000}.json"

    r = report.as_dict()
    r["Params"] = atn_params.as_dict()
    json_object = json.dumps(r, indent=4)

    # Writing to sample.json
    with open(file_name, "w") as outfile:
        outfile.write(json_object)
