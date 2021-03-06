import os
import datadog
import time
import math
import functools


def initialize():
    api_key = os.environ.get('DATADOG_API_KEY')
    app_key = os.environ.get('DATADOG_APP_KEY')
    api_host = os.environ.get('DATADOG_API_HOST')

    # those values are handled by the datadog module anyway, but explicit
    # hard-blocking errors save time on debug
    if not api_key:
        raise 'you must define an API key (setenv DATADOG_API_KEY)'
    if not app_key:
        raise 'you must define an APP key (setenv DATADOG_APP_KEY)'
    if not api_host:
        raise 'you must define a HOST (setenv DATADOG_API_HOST)'

    options = {
        'api_key': api_key,
        'app_key': app_key,
        'api_host': api_host,
    }

    print("init api_key=%s... app_key=%s... api_host=%s" %
          (api_key[:8], app_key[:12], api_host))
    print

    datadog.initialize(**options)

# if we only have zeroes or two small values, at least, scale should be this
MAX_VALUE_LIMIT = 0.000000001

# with this, the higest value in the data set is at least 20% of the max
AUTOSCALE_LOGBASE = 5


def _float(v):
    try:
        return max(float(v), 0.0)
    except:
        return 0.0


def simple_normalize(input):
    first_col = [_float(x[1]) for x in input]
    max_value = functools.reduce(lambda a, b: max(a, b), first_col)
    max_value = max(MAX_VALUE_LIMIT, max_value)
    max_scale = math.pow(AUTOSCALE_LOGBASE, math.ceil(
        math.log(max_value, AUTOSCALE_LOGBASE)))
    scaled = [x / max_scale for x in first_col]
    return scaled

DEFAULT_QUERY = 'avg:system.cpu.idle{*}'  # CPU is always available as a metric
DEFAULT_DELAY = 600                       # 10 minutes


def get_simple_data(query=DEFAULT_QUERY, delay=DEFAULT_DELAY):
    # Get a single row of data from datadog
    # TODO: remove the api_key and app_key args -> they are useless, prototype makes no sense (env vars...)
    #       instead, introduce a time range (the 3600 below...
    try:
        res = datadog.api.Metric.query(start=int(time.time()) - delay, end=int(time.time()),
                                       query=query)
    except Exception as e:
        print("error fetching data", e)
        return []

    pointlist = []
    try:
        pointlist = res['series'][0]['pointlist']
    except Exception as e:
        print("bad data %s: %s" % (res, e))
        return []

    return simple_normalize(pointlist)

MONITOR_STATUS_ALERT = 'Alert'
MONITOR_STATUS_WARN = 'Warn'
MONITOR_STATUS_OK = 'OK'
MONITOR_STATUS_NO_DATA = 'No Data'


def get_monitor_status(monitor_id):
    try:
        res = datadog.api.Monitor.get(monitor_id)
        status = res['overall_state']
        print(status)
        return status  # One of the three constants above
    except:
        return MONITOR_STATUS_NO_DATA


def get_demo_data():
    return [max(0.0, math.sin((i + time.time()) / 5)) for i in range(100)]
