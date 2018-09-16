import json

# takes in r5 reponse and cleans it up, as any goose would like

def generate_transit_geojson(
    start_lat,
    start_lon,
    end_lat,
    end_lon,
):
    # make a geojson line between the points
    return json.dumps({
        'type': 'LineString',
        # geojson is lon, lat
        'coordinates': [
            [start_lon, start_lat],
            [end_lon, end_lat],
        ],
    }, default=str)


def convert_summaries_to_gooseroutes(
    summaries,
):
    # convert summaries (routes that overlap, as do not duplicate info)
    # to gooseroutes (will duplicate stuff, but extra data is
    # insignificant for performance and greatly simplifies processing)
    itineraries = []
    for summary in summaries:
        for trip in summary['itinerary']:
            keys_to_keep = ['startTime', 'endTime', 'duration']
            itinerary = {
                key: trip[key] for key in keys_to_keep
            }
            # get access, transit, then egress segments - order matters
            # aside: may be edge cases where two transit trips connected
            # by car or bike may be desired, that would be an r5 design flaw
            # TODO|eddy find such edge cases and create an issue
            segments = []
            # get access component
            access_idx = trip['connection']['access']
            if access_idx is not None and access_idx >= 0:
                access = summary['access'][access_idx]
                segments.append({
                    'mode': access['mode'],
                    'shape': access['geometryGeoJSON'],
                    'duration': access['duration'],
                    'cost': None,
                })
            # get transit component
            transit_links = trip['connection']['transit']
            if transit_links:
                for transit_link_idx in range(0, len(transit_links)):
                    transit_link = summary['transit'][transit_link_idx]
                    segments.append({
                        'mode': transit_link['mode'],
                        'shape': generate_transit_geojson(
                            start_lat=transit_link['from']['lat'],
                            start_lon=transit_link['from']['lon'],
                            end_lat=transit_link['to']['lat'],
                            end_lon=transit_link['to']['lon'],
                        ),
                        # multiple trip patterns but we'll always use the first one
                        # guaranteed for there to be at least one
                        'startTime': transit_link['segmentPatterns'][0]['fromDepartureTime'][0],
                        'endTime': transit_link['segmentPatterns'][0]['toArrivalTime'][0],
                        'description': '{from_name} to {to_name} via {routes}'.format(
                            from_name=transit_link['from']['name'],
                            to_name=transit_link['to']['name'],
                            routes=[
                                route['shortName'] + ', ' for route in transit_link['routes']
                            ],
                        ),
                    })
            # get egress component
            egress_idx = trip['connection']['egress']
            if egress_idx is not None and egress_idx >= 0:
                egress = summary['egress'][egress_idx]
                segments.append({
                    'mode': egress['mode'],
                    'shape': egress['geometryGeoJSON'],
                    'duration': egress['duration'],
                    'cost': None,
                })
            itinerary['segments'] = segments
            itineraries.append(itinerary)
    return itineraries







