import json
import math
import random

def calculate_parking_rectangles(latitude_top_left, longitude_top_left, latitude_bottom_right, longitude_bottom_right):
    """Calculates parking rectangles based on bounding box coordinates.

    Args:
        latitude_top_left: Latitude of the top-left corner of the bounding box.
        longitude_top_left: Longitude of the top-left corner of the bounding box.
        latitude_bottom_right: Latitude of the bottom-right corner of the bounding box.
        longitude_bottom_right: Longitude of the bottom-right corner of the bounding box.

    Returns:
        A JSON string representing the calculated parking rectangles.  Returns an empty list if no rectangles are found.
    """

    # Simulate street center and orientation
    street_center_latitude = (latitude_top_left + latitude_bottom_right) / 2
    street_center_longitude = (longitude_top_left + longitude_bottom_right) / 2
    street_orientation_radians = random.uniform(0, 2 * math.pi)


    # 1. Geographic Normalization (G)
    r_lat = calculate_meridian_radius_of_curvature(street_center_latitude)
    r_lon = calculate_prime_vertical_radius_of_curvature(street_center_latitude)
    g_lat = r_lat * (math.pi / 180)
    g_lon = r_lon * math.cos(street_center_latitude * math.pi / 180) * (math.pi / 180)


    G = [[1/g_lat, 0], [0, 1/g_lon]]

    # 2. Rotation Transform (R)
    cos_theta = math.cos(street_orientation_radians)
    sin_theta = math.sin(street_orientation_radians)
    R = [[cos_theta, -sin_theta], [sin_theta, cos_theta]]

    #3. Vertex Template Matrix (M)
    K = 2.0  # Distance from street center to rectangle edge (meters)
    H = 5.0  # Height along the street (meters)
    W = 2.5  # Width perpendicular to the street (meters)

    M = [[-W/2, K], [-W/2, K + H], [W/2, K+H], [W/2, K]]

        #4. Transformations
    # Apply rotation and geographic normalization to each point in M
    rotated_geo_points = []
    for x,y in M:
        rotated_x = x * R[0][0] + y * R[1][0]
        rotated_y = x * R[0][1] + y * R[1][1]


        geo_x = rotated_x * G[0][0] + rotated_y * G[1][0]
        geo_y = rotated_x * G[0][1] + rotated_y * G[1][1]


        rotated_geo_points.append((geo_x + street_center_longitude, geo_y + street_center_latitude)) #longitude then latitude since that's the order in the example


    #5. Construct Rectangles
    rectangles = [{
        "id": 1,
        "a_longitude": rotated_geo_points[0][0], "a_latitude": rotated_geo_points[0][1],
        "b_longitude": rotated_geo_points[1][0], "b_latitude": rotated_geo_points[1][1],
        "c_longitude": rotated_geo_points[2][0], "c_latitude": rotated_geo_points[2][1],
        "d_longitude": rotated_geo_points[3][0], "d_latitude": rotated_geo_points[3][1]
    }]

    return json.dumps(rectangles, indent=4)

#constants
EARTH_RADIUS = 6371000  # Earth's radius in meters

def degrees_to_radians(degrees):
    return degrees * math.pi / 180

def calculate_distance(lat1, lon1, lat2, lon2):
    """Calculates the Haversine distance between two points on the Earth."""

    # Convert latitude and longitude from degrees to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    # Haversine formula
    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = EARTH_RADIUS * c  # Distance in meters

    return distance


def calculate_meridian_radius_of_curvature(latitude):
  """Calculates the meridian radius of curvature at a given latitude using the WGS84 ellipsoid."""
  a = 6378137.0  # Semi-major axis (equatorial radius) of WGS84 ellipsoid
  b = 6356752.314245  # Semi-minor axis (polar radius) of WGS84 ellipsoid
  e_squared = 1 - (b**2 / a**2) # eccentricity squared

  return a * (1 - e_squared) / (1 - e_squared * math.sin(math.radians(latitude))**2)**(3/2)

def calculate_prime_vertical_radius_of_curvature(latitude):
    """Calculates the prime vertical radius of curvature at a given latitude using the WGS84 ellipsoid."""
    a = 6378137.0  # Semi-major axis (equatorial radius) of WGS84 ellipsoid
    b = 6356752.314245  # Semi-minor axis (polar radius) of WGS84 ellipsoid
    e_squared = 1 - (b**2 / a**2)

    return a / math.sqrt(1 - e_squared * math.sin(math.radians(latitude))**2)