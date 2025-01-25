// Types
/**
 * @typedef {Object} Point
 * @property {number} lat - Latitude
 * @property {number} lng - Longitude
 */

/**
 * @typedef {Object} Spot
 * @property {number} x - X coordinate
 * @property {number} y - Y coordinate
 * @property {number} angle - Angle in radians
 */

// Constants
const CONSTANTS = {
  SCOUT_POINTS: 4,
  SPOT_DISTANCE: 6, // meters
  RECTANGLE: {
    DISTANCE_FROM_CENTER: 0.5,
    HEIGHT: 5,
    WIDTH: 2.5
  }
};

// Map Service
class MapService {
  constructor(map, directionsService) {
    this.map = map;
    this.directionsService = directionsService;
    this.markers = [];
  }

  addMarker(location) {
    const marker = new google.maps.Marker({
      position: location,
      map: this.map
    });
    this.markers.push(marker);
  }

  clearMarkers() {
    this.markers.forEach(marker => marker.setMap(null));
    this.markers = [];
  }

  drawRectangles(rectangles) {
    rectangles.forEach(coords => {
      new google.maps.Polygon({
        paths: coords,
        strokeColor: '#FF0000',
        strokeOpacity: 0.8,
        strokeWeight: 2,
        fillColor: '#FF0000',
        fillOpacity: 0.35,
        map: this.map
      });
    });
  }

  async getScoutPoint(position) {
    const request = {
      origin: position,
      destination: position,
      travelMode: google.maps.DirectionsTravelMode.DRIVING
    };

    return new Promise((resolve, reject) => {
      this.directionsService.route(request, (response, status) => {
        if (status === google.maps.DirectionsStatus.OK) {
          const point = response.routes[0].legs[0];
          resolve({
            x: point.start_location.lat(),
            y: point.start_location.lng()
          });
        } else {
          reject(new Error(`Direction service failed: ${status}`));
        }
      });
    });
  }
}

// Geometry Service
class GeometryService {
  /**
   * Calculate distance between two points using Haversine formula
   */
  static calculateDistance(point1, point2, inKilometers = false) {
    const EARTH_RADIUS = 6371; // km
    const DEG_TO_RAD = Math.PI / 180;

    const dLat = (point2.lat - point1.lat) * DEG_TO_RAD;
    const dLon = (point2.lng - point1.lng) * DEG_TO_RAD;
    const lat1 = point1.lat * DEG_TO_RAD;
    const lat2 = point2.lat * DEG_TO_RAD;

    const a = Math.sin(dLat / 2) ** 2 + 
              Math.sin(dLon / 2) ** 2 * Math.cos(lat1) * Math.cos(lat2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    const distanceKm = EARTH_RADIUS * c;

    return inKilometers ? distanceKm : distanceKm * 1000;
  }

  static findClosestPoint(point, points) {
    if (points.length === 0) return null;

    return points.reduce((closest, current) => {
      const currentDistance = this.calculateDistance(point, current);
      const closestDistance = this.calculateDistance(point, closest);
      return currentDistance < closestDistance ? current : closest;
    });
  }

  static generateSpots(startPoint, endPoint, distance) {
    const totalDistance = this.calculateDistance(startPoint, endPoint);
    const numSpots = Math.floor(totalDistance / distance);
    
    const spots = [];
    const dx = (endPoint.x - startPoint.x) / numSpots;
    const dy = (endPoint.y - startPoint.y) / numSpots;
    const angle = Math.atan2(dy, dx);

    for (let i = 0; i < numSpots; i++) {
      spots.push({
        x: startPoint.x + i * dx,
        y: startPoint.y + i * dy,
        angle
      });
    }

    return spots;
  }

  static generateRectangles(spot, bounds) {
    const { DISTANCE_FROM_CENTER, HEIGHT, WIDTH } = CONSTANTS.RECTANGLE;
    const { x, y, angle } = spot;

    // Calculate scaling factors
    const scaleX = Math.abs(bounds.bx - bounds.tx) / 
                   this.calculateDistance(
                     {lat: bounds.bx, lng: bounds.by},
                     {lat: bounds.tx, lng: bounds.by}
                   );
    const scaleY = Math.abs(bounds.by - bounds.ty) / 
                   this.calculateDistance(
                     {lat: bounds.bx, lng: bounds.by},
                     {lat: bounds.bx, lng: bounds.ty}
                   );

    const cos = Math.cos(angle);
    const sin = Math.sin(angle);

    // Generate rectangle coordinates with proper scaling
    return [
      this.generateRectangleSide(x, y, -DISTANCE_FROM_CENTER, HEIGHT, WIDTH, cos, sin, scaleX, scaleY),
      this.generateRectangleSide(x, y, DISTANCE_FROM_CENTER, HEIGHT, WIDTH, cos, sin, scaleX, scaleY)
    ];
  }

  static generateRectangleSide(x, y, k, h, w, cos, sin, scaleX, scaleY) {
    return [
      {lat: x + scaleX * (k * cos), lng: y + scaleY * (-k * sin)},
      {lat: x + scaleX * (k * cos - h * sin), lng: y + scaleY * (-k * sin - h * cos)},
      {lat: x + scaleX * (k * cos - h * sin + w * cos), lng: y + scaleY * (-k * sin - h * cos - w * sin)},
      {lat: x + scaleX * (k * cos + w * cos), lng: y + scaleY * (-k * sin - w * sin)}
    ];
  }
}

// Street Mapper
class StreetMapper {
  constructor(mapService) {
    this.mapService = mapService;
    this.spots = [];
    this.rectangles = [];
    this.extremePoints = [];
  }

  async scout(bounds) {
    const { SCOUT_POINTS } = CONSTANTS;
    const dx = (bounds.bx - bounds.tx) / SCOUT_POINTS;
    const dy = (bounds.ty - bounds.by) / SCOUT_POINTS;
    
    this.mapService.clearMarkers();
    
    const scoutPoints = [];
    for (let x = bounds.tx + dx / 2; x < bounds.bx; x += dx) {
      for (let y = bounds.by + dy / 2; y < bounds.ty; y += dy) {
        const point = await this.mapService.getScoutPoint({lat: x, lng: y});
        scoutPoints.push(point);
        this.mapService.addMarker({lat: x, lng: y});
      }
    }
    
    return scoutPoints;
  }

  processStreet(points) {
    const extremePoints = this.findExtremePoints(points);
    this.connectPoints(points[0], points.slice(1), CONSTANTS.SPOT_DISTANCE);
    this.mapService.drawRectangles(this.rectangles);
  }

  findExtremePoints(points) {
    // Implementation of Graham Scan convex hull algorithm would go here
    // For now, returning original points as placeholder
    return points;
  }

  connectPoints(startPoint, remainingPoints, distance) {
    if (remainingPoints.length === 0) return;

    const nextPoint = GeometryService.findClosestPoint(startPoint, remainingPoints);
    if (!nextPoint) return;

    if (GeometryService.calculateDistance(startPoint, nextPoint) < distance) {
      const spots = GeometryService.generateSpots(startPoint, nextPoint, distance);
      this.spots.push(...spots);
      
      spots.forEach(spot => {
        const rectangles = GeometryService.generateRectangles(spot, this.bounds);
        this.rectangles.push(...rectangles);
        this.mapService.addMarker({lat: spot.x, lng: spot.y});
      });

      const remaining = remainingPoints.filter(p => p !== nextPoint);
      this.connectPoints(nextPoint, remaining, distance);
    }
  }
}

export { StreetMapper, MapService, GeometryService, CONSTANTS };