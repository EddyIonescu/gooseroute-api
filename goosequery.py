# GraphQL Query used to perform multi-modal routing queries on R5 by Conveyal
# https://github.com/EddyIonescu/totx-r5
GRAPH_QUERY = """
query requestPlan($fromLat:Float!, $fromLon:Float!,
  $toLat:Float!, $toLon:Float!, $wheelchair:Boolean
  $fromTime: ZonedDateTime!, $toTime:ZonedDateTime!,
  $bikeTrafficStress:Int!, $minBikeTime:Int!
  ) {
plan(fromLat:$fromLat, fromLon:$fromLon, toLat:$toLat,toLon:$toLon, wheelchair:$wheelchair, fromTime:$fromTime, toTime:$toTime, 
 
  directModes:[WALK,BICYCLE,CAR,BICYCLE_RENT],
  accessModes:[WALK,CAR,BICYCLE,BICYCLE_RENT], egressModes:[WALK,BICYCLE,BICYCLE_RENT,CAR],
transitModes:[TRANSIT],
bikeTrafficStress: $bikeTrafficStress, minBikeTime: $minBikeTime) {
  options {
    summary,
    fares {
       type,low,peak,senior, transferReduction, currency
    }
    itinerary {
      waitingTime
      walkTime
      distance
      transfers
      duration
      transitTime
      startTime
      endTime,
      connection {
        access
        egress,
        transit {
          pattern
          time
        }
      }
    }
    transit {
      from {
        name,
        stopId,
        lon,
        lat,
        wheelchairBoarding
      },
       to {
        name,
        stopId,
        lon,
        lat,
        wheelchairBoarding
      },
      mode,
      routes {id, routeIdx shortName, mode, agencyName},
      segmentPatterns {
        patternId,
        patternIdx,
        routeIdx,
        fromIndex,
        toIndex,
        fromDepartureTime
        toArrivalTime,
        tripId
      },
      middle {
        mode,
        duration,
        distance,
        geometryGeoJSON,
      },
      transitEdges {
        id,
        fromStopID,
        toStopID,
        routeID,
        geometry,
      },
    },
    access {
      mode,
      duration,
      distance,
      geometryGeoJSON,
      streetEdges {
        edgeId
        distance
        geometryGeoJSON
        mode
        streetName
        relativeDirection
        absoluteDirection
      }
    },
     egress {
      mode,
      duration,
      distance,
      geometryGeoJSON,
      streetEdges {
        edgeId
        mode
        geometryGeoJSON,
        streetName
        relativeDirection
        absoluteDirection
      }
    }
  } 
  }
} 
"""
