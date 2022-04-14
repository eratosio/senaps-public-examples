import pandas as pd

from senaps_sensor.parsers import PandasObservationParser

try:
    from urllib import quote  # Python 2.X
except ImportError:
    from urllib.parse import quote  # Python 3+


class SenapsUtils:
    @staticmethod
    def download_observations(stream_ids, sensor_client, start=None, end=None, sort='descending', batch_size=1000,
                              total_limit=None):
        results = pd.DataFrame()

        for obs in SenapsUtils.batch_download_observations(stream_ids, sensor_client, start, end, sort, batch_size,
                                                           total_limit):
            results = results.append(obs)

        results = results.sort_index(ascending=sort != "descending")

        print("Successfully download total %d results" % len(results))
        print(results)
        return results

    @staticmethod
    def batch_download_observations(stream_ids,
                                    sensor_client,
                                    start=None,
                                    end=None,
                                    sort="descending",
                                    batch_size=1000,
                                    total_limit=None):

        stream_ids_str = ','.join(stream_ids)

        result_count = 0
        page_number = 0

        for obs_df in paginate_observations(sensor_client, stream_ids_str, start, end, sort=sort, limit=batch_size):
            yield obs_df

            page_number += 1
            result_count += len(obs_df)

            if total_limit is not None and result_count >= total_limit:
                print('Hard download limit reached: %d.' % total_limit)
                break


def _get_senaps_param_iso_utc_dt_string(original):
    """
    Given an ISO8601 timestamp that has a +HH:MM suffix, replace the suffix with a simple Z for the Zulu/UTC
    timezone. Note that this will COMPLETELY disregard your existing timezone if you had one. You've been warned!
    """
    if original is None:
        return None
    if original.endswith('Z'):
        return original

    if original[-6] == '+':
        return original[:-6] + 'Z'

    return None  # should not be the case we get here.


def paginate_observations(sensor_client, streamids, start_date, end_date, sort=None, limit=1000):
    start = start_date
    end = end_date

    is_first = True

    while True:
        # For the case where we have reached the end of the line exit early...
        if not is_first and start == end:
            break

        response = sensor_client.get_observations(streamid=streamids,
                                                  start=start,
                                                  end=end,
                                                  si='false' if not is_first and sort != 'descending' else None,
                                                  ei='false' if not is_first and sort == 'descending' else None,
                                                  limit=limit,
                                                  sort=sort,
                                                  media="csv",
                                                  parser=PandasObservationParser())

        # print('Page: %s' % response)

        if len(response) > 0:
            print('fetched %d results from %s to %s' % (
                len(response), response.index[0].isoformat(), response.index[-1].isoformat()))
        else:
            print('processed 0 results')

        yield response

        if len(response) < limit:
            break

        if sort == 'descending':
            end = _get_senaps_param_iso_utc_dt_string(response.index[-1].isoformat())
        else:
            start = _get_senaps_param_iso_utc_dt_string(response.index[-1].isoformat())

        is_first = False