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

    print("init api_key=%s... app_key=%s... api_host=%s" % (api_key[:8],app_key[:12],api_host))
    print

    datadog.initialize(**options)

# if we only have zeroes or two small values, at least, scale should be this
MAX_VALUE_LIMIT=0.000000001
def simple_normalize(input):
    first_col=[x[0] for x in input]
    max_value = functools.reduce (lambda a, b: max(a,b), first_col)
    max_value = max(MAX_VALUE_LIMIT, max_value)
    max_scale = math.pow(10, math.ceil(math.log10(max_value)))
    scaled = [x/max_scale for x in first_col]
    return scaled

DEFAULT_QUERY='avg:system.cpu.idle{*}' # CPU is always available as a metric
DEFAULT_DELAY=300                      # 5 minutes
def get_simple_data(query=DEFAULT_QUERY,delay=DEFAULT_DELAY):
    # Get a single row of data from datadog
    # TODO: remove the api_key and app_key args -> they are useless, prototype makes no sense (env vars...)
    #       instead, introduce a time range (the 3600 below...
    res=datadog.api.Metric.query(start=int(time.time()) - delay, end=int(time.time()),
                               query=query)
    pointlist=[]
    try:
        pointlist=res['series'][0]['pointlist']
    except:
        raise "bad data %s" % res

    print(simple_normalize(pointlist))

    True # TODO !
