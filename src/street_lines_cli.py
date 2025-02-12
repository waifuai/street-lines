import json
import math
import random

# Constants
EARTH_RADIUS = 6371000  # Earth's radius in meters


def degrees_to_radians(degrees):
    return degrees * math.pi / 180


def calculate_distance(lat1, lon1, lat2, lon2):
    """Calculates the Haversine distance between two points on the Earth."""

    # Convert latitude and longitude from degrees to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lat2)

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
    e_squared = 1 - (b**2 / a**2)  # eccentricity squared

    return a * (1 - e_squared) / (1 - e_squared * math.sin(math.radians(latitude))**2)**(3/2)


def calculate_prime_vertical_radius_of_curvature(latitude):
    """Calculates the prime vertical radius of curvature at a given latitude using the WGS84 ellipsoid."""
    a = 6378137.0  # Semi-major axis (equatorial radius) of WGS84 ellipsoid
    b = 6356752.314245  # Semi-minor axis (polar radius) of WGS84 ellipsoid
    e_squared = 1 - (b**2 / a**2)

    return a / math.sqrt(1 - e_squared * math.sin(math.radians(latitude))**2)


def transform_coordinates(points, rotation_matrix, normalization_matrix, street_center_longitude, street_center_latitude):
    """Transforms a list of points using rotation and geographic normalization.

    Args:
        points: A list of (x, y) tuples representing the points to transform.
        rotation_matrix: The rotation matrix.
        normalization_matrix: The geographic normalization matrix.
        street_center_longitude: The longitude of the street center.
        street_center_latitude: The latitude of the street center.

    Returns:
        A list of (longitude, latitude) tuples representing the transformed points.
    """

    transformed_points = []
    for x, y in points:
        # Rotate the point
        rotated_x = x * rotation_matrix[0][0] + y * rotation_matrix[1][0]
        rotated_y = x * rotation_matrix[0][1] + y * rotation_matrix[1][1]

        # Apply geographic normalization
        geo_x = rotated_x * normalization_matrix[0][0] + rotated_y * normalization_matrix[1][0]
        geo_y = rotated_x * normalization_matrix[0][1] + rotated_y * normalization_matrix[1][1]

        # Append the transformed coordinates (longitude, latitude)
        transformed_points.append((geo_x + street_center_longitude, geo_y + street_center_latitude))

    return transformed_points


def construct_rectangles(transformed_points):
    """Constructs a list of rectangles from a list of transformed points.

    Args:
        transformed_points: A list of (longitude, latitude) tuples representing the rectangle vertices.

    Returns:
        A list of dictionaries representing the rectangles.
    """

    rectangles = [{
        "id": 1,
        "a_longitude": transformed_points[0][0], "a_latitude": transformed_points[0][1],
        "b_longitude": transformed_points[1][0], "b_latitude": transformed_points[1][1],
        "c_longitude": transformed_points[2][0], "c_latitude": transformed_points[2][1],
        "d_longitude": transformed_points[3][0], "d_latitude": transformed_points[3][1]
    }]

    return rectangles


def calculate_parking_rectangles(latitude_top_left, longitude_top_left, latitude_bottom_right, longitude_bottom_right):
    """Calculates parking rectangles based on bounding box coordinates.

    Args:
        latitude_top_left: Latitude of the top-left corner of the bounding box.
        longitude_top_left: Longitude of the top-left corner of the bounding box.
        latitude_bottom_right: Latitude of the bottom-right corner of the bounding box.
        longitude_bottom_right: Longitude of the bottom-right corner of the bounding box.

    Returns:
        A JSON string representing the calculated parking rectangles. Returns an empty list if no rectangles are found.
    """

    # Input validation
    if not all(isinstance(arg, (int, float)) for arg in [latitude_top_left, longitude_top_left, latitude_bottom_right, longitude_bottom_right]):
        raise ValueError("All input coordinates must be numeric.")

    # Simulate street center and orientation.  In a real application, these values would come from an external source (e.g., Google Maps API).
    # The street orientation is a random angle for simulation purposes.
    street_center_latitude = (latitude_top_left + latitude_bottom_right) / 2
    street_center_longitude = (longitude_top_left + longitude_bottom_right) / 2
    street_orientation_radians = random.uniform(0, 2 * math.pi)

    # 1. Geographic Normalization (G)
    r_lat = calculate_meridian_radius_of_curvature(street_center_latitude)
    r_lon = calculate_prime_vertical_radius_of_curvature(street_center_latitude)
    g_lat = r_lat * (math.pi / 180)
    g_lon = r_lon * math.cos(street_center_latitude * math.pi / 180) * (math.pi / 180)

    # Geographic Normalization Matrix
    normalization_matrix = [[1/g_lat, 0], [0, 1/g_lon]]

    # 2. Rotation Transform (R)
    cos_theta = math.cos(street_orientation_radians)
    sin_theta = math.sin(street_orientation_radians)

    # Rotation matrix
    rotation_matrix = [[cos_theta, -sin_theta], [sin_theta, cos_theta]]

    # 3. Vertex Template Matrix (M)
    K = 2.0  # Distance from street center to rectangle edge (meters)
    H = 5.0  # Height along the street (meters)
    W = 2.5  # Width perpendicular to the street (meters)

    # Vertex Template Matrix
    M = [[-W/2, K], [-W/2, K + H], [W/2, K+H], [W/2, K]]

    # 4. Transformations
    # Apply rotation and geographic normalization to each point in M
    transformed_points = transform_coordinates(M, rotation_matrix, normalization_matrix, street_center_longitude, street_center_latitude)

    # 5. Construct Rectangles
    rectangles = construct_rectangles(transformed_points)

    return json.dumps(rectangles, indent=4)