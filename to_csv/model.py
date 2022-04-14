import json
from datetime import datetime

from as_models.models import model

from senaps_utils import SenapsUtils

@model("eratos.examples.to_csv")
def to_csv(context):
    # extract ports (see manifest.json)
    input_streams = getattr(context.ports, 'input_streams', None)
    output = getattr(context.ports, 'output', None)
    settings = getattr(context.ports, 'settings', None)

    if settings and settings.value:
        json_settings = json.loads(settings.value)
    else:
        json_settings = {}

    streamids = [s.stream_id for s in input_streams]

    # unpack settings json values...
    start_date = json_settings.get('start_date', None)
    end_date = json_settings.get('end_date', None)
    desc = json_settings.get('desc', True)
    limit = json_settings.get('limit', 1000)

    # download timeseries data - returns a pandas dataframe
    result = SenapsUtils.download_observations(streamids, context.sensor_client, start=start_date, end=end_date, total_limit=limit, sort='descending' if desc else 'ascending')

    # assign the value directly to the output port will internally write the result back to Senaps.
    output.value = result.to_csv(index=True, date_format='%Y-%m-%dT%H:%M:%S.%fZ')


