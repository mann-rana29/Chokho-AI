from typing import List, Dict , Tuple, Optional
import math
from enum import Enum

class ZoneType(str, Enum):
    RIVER = "river"
    TEMPLE = "temple"
    TOURIST = "tourist"
    PARK = "park"
    MARKET = "market"

ZONE_SENSITIVITY = {
    ZoneType.RIVER: 10,
    ZoneType.TEMPLE: 9,
    ZoneType.PARK: 8,
    ZoneType.TOURIST: 7,
    ZoneType.MARKET: 6,
}

SENSITIVE_LOCATIONS = [
    # RIVERS (Highest Priority - Score 10)
    {'name': 'Har Ki Pauri Ghat', 'type': ZoneType.RIVER, 'lat': 29.9457, 'lng': 78.1642, 'radius_km': 0.5},
    {'name': 'Rishikesh Triveni Ghat', 'type': ZoneType.RIVER, 'lat': 30.1030, 'lng': 78.2949, 'radius_km': 0.3},
    {'name': 'Devprayag Sangam', 'type': ZoneType.RIVER, 'lat': 30.1458, 'lng': 78.5986, 'radius_km': 0.5},
    {'name': 'Gangotri Ganga Origin', 'type': ZoneType.RIVER, 'lat': 30.9992, 'lng': 78.9408, 'radius_km': 1.0},
    {'name': 'Yamunotri Origin', 'type': ZoneType.RIVER, 'lat': 31.0117, 'lng': 78.4270, 'radius_km': 1.0},
    
    # TEMPLES (Score 9)
    {'name': 'Kedarnath Temple', 'type': ZoneType.TEMPLE, 'lat': 30.7346, 'lng': 79.0669, 'radius_km': 1.0},
    {'name': 'Badrinath Temple', 'type': ZoneType.TEMPLE, 'lat': 30.7433, 'lng': 79.4938, 'radius_km': 1.0},
    {'name': 'Mansa Devi Temple', 'type': ZoneType.TEMPLE, 'lat': 29.9792, 'lng': 78.1340, 'radius_km': 0.5},
    {'name': 'Neelkanth Mahadev', 'type': ZoneType.TEMPLE, 'lat': 30.1622, 'lng': 78.4368, 'radius_km': 0.8},
    
    # TOURIST SPOTS (Score 7)
    {'name': 'Nainital Lake', 'type': ZoneType.TOURIST, 'lat': 29.3919, 'lng': 79.4542, 'radius_km': 0.5},
    {'name': 'Mussoorie Mall Road', 'type': ZoneType.TOURIST, 'lat': 30.4598, 'lng': 78.0644, 'radius_km': 0.3},
    {'name': 'Dehradun Paltan Bazaar', 'type': ZoneType.TOURIST, 'lat': 30.3255, 'lng': 78.0436, 'radius_km': 0.5},
    {'name': 'Auli Ski Resort', 'type': ZoneType.TOURIST, 'lat': 30.5373, 'lng': 79.5906, 'radius_km': 1.0},
    
    # NATIONAL PARKS (Score 8)
    {'name': 'Jim Corbett Park Entrance', 'type': ZoneType.PARK, 'lat': 29.5312, 'lng': 78.7698, 'radius_km': 2.0},
    {'name': 'Valley of Flowers', 'type': ZoneType.PARK, 'lat': 30.7264, 'lng': 79.6042, 'radius_km': 1.5},
    
    # MARKETS (Score 6)
    {'name': 'Haridwar Railway Station', 'type': ZoneType.MARKET, 'lat': 29.9459, 'lng': 78.1644, 'radius_km': 0.3},
    {'name': 'Rishikesh Bus Stand', 'type': ZoneType.MARKET, 'lat': 30.1110, 'lng': 78.2886, 'radius_km': 0.3},
]


def haversine_distance(lat1 : float , long1 : float, lat2 : float , long2: float):

    R = 6371

    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    long1_rad = math.radians(long1)
    long2_rad = math.radians(long2)

    dlat = lat2_rad - lat1_rad
    dlong = long2_rad - long1_rad

    # Correct Haversine formula
    a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlong/2)**2
    
    # Clamp 'a' to prevent math domain error due to floating point issues
    a = min(1.0, max(0.0, a))
    
    c = 2 * math.asin(math.sqrt(a))

    return R * c


def calculate_location_sens(lat: float , lng : float) -> Tuple[int, str, Optional[Dict]]:
    max_sens = 3
    closest_location = None
    min_distance = float('inf')
    reason = "Remote/Residential Area"

    for location in SENSITIVE_LOCATIONS:
        distance_km = haversine_distance(lat,lng, location['lat'], location['lng'])

        if distance_km <= location['radius_km']:
            base_score = ZONE_SENSITIVITY[location['type']]

            proximity_score = 1 - (distance_km/location['radius_km'])
            adjusted_score = base_score - (1 - proximity_score)

            if adjusted_score > max_sens:
                max_sens = int(round(adjusted_score))
                closest_location = location
                min_distance = distance_km
                reason = f"Within {location['name']} ({location['type'].value} zone)"
            
        elif distance_km <= location['radius_km'] * 3:
            base_score = ZONE_SENSITIVITY[location['type']]
            nearby_score = base_score - 3

            if nearby_score > max_sens:
                max_sens = max(nearby_score, 4)
                closest_location = location
                min_distance =  distance_km
                reason = f"Near {location['name']} ({distance_km:.1f}km away)"

        if distance_km < min_distance and closest_location is None:
            min_distance = distance_km
            closest_location = location
        
    if max_sens == 3 and closest_location:
        if min_distance < 10:
            max_sens = 4
            reason = f"Outskirts of {closest_location['name']} ({min_distance:.1f}km)"
        else:
            reason = f"Remote area (nearest landmark: {closest_location['name']}, {min_distance:.1f}km away)"
    
    max_sens = max(1,min(10,max_sens))

    location_info = None

    if closest_location:
        location_info = {
            'name': closest_location['name'],
            'type': closest_location['type'].value,
            'distance_km': round(min_distance, 2),
            'within_zone': min_distance <= closest_location['radius_km']
        }
    
    return max_sens, reason, location_info