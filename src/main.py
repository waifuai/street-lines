# Constants
import math
import argparse
import asyncio

CONSTANTS = {
    "SCOUT_POINTS": 2,
    "SPOT_DISTANCE": 6,
    "RECTANGLE": {
        "DISTANCE_FROM_CENTER": 2,
        "HEIGHT": 2,
        "WIDTH": 1
    }
}

class GeometryService:
    @staticmethod
    def clamp(value, min_val, max_val):
        return max(min(value, max_val), min_val)

    @staticmethod
    def generate_spots(start_point, end_point, distance):
        dx = end_point['lat'] - start_point['lat']
        dy = end_point['lng'] - start_point['lng']
        angle = math.atan2(dy, dx)
        return [{
            'lat': (start_point['lat'] + end_point['lat']) / 2,
            'lng': (start_point['lng'] + end_point['lng']) / 2,
            'angle': angle
        }]

    @staticmethod
    def generate_rectangles(spot, bounds):
        k = CONSTANTS["RECTANGLE"]["DISTANCE_FROM_CENTER"]
        h = CONSTANTS["RECTANGLE"]["HEIGHT"]
        w = CONSTANTS["RECTANGLE"]["WIDTH"]
        cos_a = math.cos(spot['angle'])
        sin_a = math.sin(spot['angle'])
        
        def clamp_point(p):
            min_lat = min(bounds['bx'], bounds['tx'])
            max_lat = max(bounds['bx'], bounds['tx'])
            min_lng = min(bounds['ty'], bounds['by'])
            max_lng = max(bounds['ty'], bounds['by'])
            return {
                'lat': GeometryService.clamp(p['lat'], min_lat, max_lat),
                'lng': GeometryService.clamp(p['lng'], min_lng, max_lng)
            }

        return [
            [
                clamp_point({'lat': spot['lat'] - k*sin_a, 'lng': spot['lng'] + k*cos_a}),
                clamp_point({'lat': spot['lat'] - k*sin_a - h*cos_a, 'lng': spot['lng'] + k*cos_a - h*sin_a}),
                clamp_point({'lat': spot['lat'] - k*sin_a - h*cos_a + w*sin_a, 'lng': spot['lng'] + k*cos_a - h*sin_a - w*cos_a}),
                clamp_point({'lat': spot['lat'] - k*sin_a + w*sin_a, 'lng': spot['lng'] + k*cos_a - w*cos_a})
            ],
            [
                clamp_point({'lat': spot['lat'] + k*sin_a, 'lng': spot['lng'] - k*cos_a}),
                clamp_point({'lat': spot['lat'] + k*sin_a - h*cos_a, 'lng': spot['lng'] - k*cos_a - h*sin_a}),
                clamp_point({'lat': spot['lat'] + k*sin_a - h*cos_a + w*sin_a, 'lng': spot['lng'] - k*cos_a - h*sin_a - w*cos_a}),
                clamp_point({'lat': spot['lat'] + k*sin_a + w*sin_a, 'lng': spot['lng'] - k*cos_a - w*cos_a})
            ]
        ]

class StreetMapper:
    def __init__(self):
        self.rectangles = []

    async def scout(self, bounds):
        return [
            {'lat': bounds['tx'], 'lng': bounds['ty']},
            {'lat': bounds['bx'], 'lng': bounds['by']}
        ]

    def process_street(self, points, bounds):
        if len(points) < 2: return []
        spot = {
            'lat': (points[0]['lat'] + points[1]['lat'])/2,
            'lng': (points[0]['lng'] + points[1]['lng'])/2,
            'angle': math.atan2(
                points[1]['lng'] - points[0]['lng'],
                points[1]['lat'] - points[0]['lat']
            )
        }
        return GeometryService.generate_rectangles(spot, bounds)

async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--tx", type=float, default=0.0)
    parser.add_argument("--ty", type=float, default=0.0)
    parser.add_argument("--bx", type=float, default=10.0)
    parser.add_argument("--by", type=float, default=10.0)
    args = parser.parse_args()
    
    bounds = {
        'tx': args.tx,  # Northern boundary
        'ty': args.ty,  # Western boundary
        'bx': args.bx,  # Southern boundary
        'by': args.by   # Eastern boundary
    }
    
    mapper = StreetMapper()
    scout_points = await mapper.scout(bounds)
    rectangles = mapper.process_street(scout_points, bounds)
    
    print("Generated Rectangles (2 total):")
    for rect in rectangles[:2]:
        print(["{'lat': %.2f, 'lng': %.2f}" % (p['lat'], p['lng']) for p in rect])

if __name__ == '__main__':
    asyncio.run(main())