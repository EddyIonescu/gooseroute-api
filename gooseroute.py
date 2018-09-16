import datetime
import json
from flask import Flask
from flask import request
import requests

from gooseclean import convert_summaries_to_gooseroutes
from goosequery import GRAPH_QUERY

app = Flask(__name__)

@app.route('/', methods=['POST'])
def gooseroute():
    print(request.args)
    start_lat = request.args['startLat']
    start_lon = request.args['startLon']
    end_lat = request.args['endLat']
    end_lon = request.args['endLon']
    # additonal optional options
    walk_speed = request.args.get('walkSpeed', None) # in m/s
    # includes all TNCs (uber/lyft), does include non-car uber-owned stuff,
    # like JUMP bike - TODO|eddy implement
    # no_uber = request.args.get('noUber', None)
    summaries = make_routing_call(
        start_lat=start_lat,
        start_lon=start_lon,
        end_lat=end_lat,
        end_lon=end_lon,
        walk_speed=walk_speed,
    )
    gooseroutes = convert_summaries_to_gooseroutes(
        summaries=summaries,
    )
    return json.dumps(gooseroutes, default=str)


def make_routing_call(
    start_lat,
    start_lon,
    end_lat,
    end_lon,
    walk_speed=None,
):
    # TODO|eddy - allow choosing a departure range from the client-side
    from_time = datetime.datetime.now() # - datetime.timedelta(hours=6)
    to_time = from_time + datetime.timedelta(minutes=60)
    request_dict = {
        'fromLat': start_lat,
        'fromLon': start_lon,
        'toLat': end_lat,
        'toLon': end_lon,
        'walkSpeed': walk_speed or 1.3,
        'wheelchair': False,
        'fromTime': from_time.replace(tzinfo=TZ()).isoformat(),
        'toTime': to_time.replace(tzinfo=TZ()).isoformat(),
        'minBikeTime': '5',
        'bikeTrafficStress': '4'
    }
    request = requests.post(
        url='http://localhost:8080/otp/routers/default/index/graphql',
        json={
            'query': GRAPH_QUERY,
            'operationName': 'requestPlan',
            'variables': request_dict,
        },
    )
    return request.json()['data']['plan']['options']


class TZ(datetime.tzinfo):
    def utcoffset(self, dt):
        return datetime.timedelta(minutes=0)

