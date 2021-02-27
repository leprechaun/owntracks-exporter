#!/usr/bin/env python

import os
import requests
import json
import time

from prometheus_client import start_http_server
from prometheus_client import Gauge

from math import radians, cos, sin, asin, sqrt


h = Gauge('owntracks_distance_from_poi', 'distance between me and a POI', ['poi'])

POI = json.loads(os.environ['POI'])
OT_LAST_URL = os.environ['OT_LAST_URL']
PROMETHEUS_PORT = int(os.environ['PROMETHEUS_PORT'])
OT_POLLING_DELAY = int(os.environ['OT_POLLING_DELAY'])
OT_TID = os.environ['OT_TID']

def haversine(point1, point2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [point1[1], point1[0], point2[1], point2[0]])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r




def update():
    r = requests.get(OT_LAST_URL)
    last = r.json()

    tracker  = list(filter(lambda x: x['tid'] == OT_TID, last))[0]
    me = (tracker['lat'], tracker['lon'])
    for poi in POI:
        distance = haversine(me, POI[poi])
        print("tracker '%s' is %f KM from POI '%s'" %(OT_TID, distance, poi))
        h.labels(poi).set(distance)

start_http_server(int(PROMETHEUS_PORT))

while True:
    update()
    time.sleep(OT_POLLING_DELAY)
