// Map configuration and constants
const MAP_CONFIG = {
  initialLocation: {
    lat: 41.850033,
    lng: -87.6500523
  },
  zoom: 7,
  mapType: 'roadmap'
};

class MapManager {
  constructor(mapElementId) {
    this.mapElementId = mapElementId;
    this.map = null;
    this.marker = null;
    this.directionsService = null;
    this.directionsRenderer = null;
  }

  // Initialize the map and all required services
  initialize() {
    // Initialize services
    this.directionsService = new google.maps.DirectionsService();
    this.directionsRenderer = new google.maps.DirectionsRenderer();
    
    // Create map instance
    this.map = new google.maps.Map(document.getElementById(this.mapElementId), {
      center: new google.maps.LatLng(
        MAP_CONFIG.initialLocation.lat,
        MAP_CONFIG.initialLocation.lng
      ),
      zoom: MAP_CONFIG.zoom,
      mapTypeId: google.maps.MapTypeId[MAP_CONFIG.mapType.toUpperCase()]
    });

    // Setup directions renderer
    this.directionsRenderer.setMap(this.map);

    // Initialize marker
    this.marker = new google.maps.Marker({
      map: null // Initially hidden
    });

    // Add click event listener
    this.map.addListener('click', (event) => this.handleMapClick(event));
  }

  // Handle map click events
  async handleMapClick(event) {
    try {
      // Clear existing marker
      if (this.marker) {
        this.marker.setMap(null);
      }

      const latLng = event.latLng;
      const response = await this.getDirections(latLng);
      
      if (response) {
        const point = response.routes[0].legs[0];
        
        // Update marker position
        this.marker.setOptions({
          map: this.map,
          position: point.start_location
        });

        // Center map on the new location
        this.map.setCenter(point.start_location);
      }
    } catch (error) {
      console.error('Error handling map click:', error);
    }
  }

  // Get directions using the DirectionsService
  getDirections(latLng) {
    const request = {
      origin: latLng,
      destination: latLng,
      travelMode: google.maps.TravelMode.DRIVING
    };

    return new Promise((resolve, reject) => {
      this.directionsService.route(request, (response, status) => {
        if (status === google.maps.DirectionsStatus.OK) {
          resolve(response);
        } else {
          reject(new Error(`Directions request failed: ${status}`));
        }
      });
    });
  }
}

// Initialize map when the page loads
document.addEventListener('DOMContentLoaded', () => {
  const mapManager = new MapManager('map_canvas');
  mapManager.initialize();
});