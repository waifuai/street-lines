# street-lines: Approximating Road Line Segments and Parking Spaces

This project approximates road line segments and potential curbside parking spots using mathematical calculations and the Google Maps API. Since Google doesn't directly provide this data, `street-lines` offers a valuable tool for developers who need this information without resorting to large datasets like OpenStreetMap.

## Setup

1. Obtain a Google Maps API key.
2. Replace `INSERT_API_KEY` in `main/index.html` with your API key.

## How it Works

`street-lines` works by querying the Google Maps API for the nearest street point to a grid of coordinates within a specified bounding box. It then uses a mathematical algorithm to infer road lines and potential parking spots based on these points.

## Usage

1. Launch `index.html` in a web browser.
2. The script automatically calls the `startConnect()` function 3 seconds after the page loads. You can also manually execute `startConnect()` in the JavaScript console repeatedly to refine the results.

## Algorithm

The core algorithm generates rectangles representing potential parking spots on both sides of a street.

### Key Concepts

* **Street Center Point (P(x, y)):**  Represents the center of a street segment.
* **Bounding Box:** Defined by top-left $(t_1, t_2)$ and bottom-right $(b_1, b_2)$ latitude/longitude coordinates.
* **Parking Rectangle Dimensions:**
    * **K:** Distance from street center to rectangle edge (meters).
    * **H:** Height along the street (meters).
    * **W:** Width perpendicular to the street (meters).
* **Street Orientation (θ):** Angle between the street segment and true north (radians).
* **Normalization Matrix (G):** Converts meters to degrees latitude/longitude (constant for a fixed bounding box).
* **Haversine Distance (d()):** Calculates the distance between two points on a sphere (approximating Earth).

### Mathematical Formulation

The algorithm uses matrices and vectors to calculate rectangle vertices:

* **Dimension Matrix (B):**  `[[K], [H], [W]]`
* **Vertex Template Matrix (M):**  `[[1, 0, 0], [1, 1, 0], [1, 1, 1], [1, 0, 1]]`
* **Rotation Vectors:**
    * `T₁ = [[cos(θ)], [sin(θ)], [cos(θ)]]`
    * `T₂ = [[sin(θ)], [cos(θ)], [sin(θ)]]`
* **Sign Adjustment Vectors:**
    * `A₁ = [[-1], [-1], [-1]]`
    * `A₂ = [[1], [-1], [1]]`
* **Permutation Matrix (P):** `[[0, 1], [1, 0]]` (for mirroring across the street)
* **Street Center Vector (v):** `[[x], [y]]`
* **Normalization Matrix (G):** `[[|b₁ - t₁| / d((b₁, b₂), (t₁, b₂))], [|b₂ - t₂| / d((b₁, b₂), (b₁, t₂))]]`

**Calculating Rectangle Vertices:**

1. **Translation Vector (dv):** `dv = G * B * M^T * T * A` (where `T = [T₁, T₂]` and `A = [A₁, A₂]`)
2. **Rectangle 1 (R₁):** `R₁ = v + dv`
3. **Rectangle 2 (R₂):** `R₂ = P * R₁`

## Algorithm Specification

**Objective:** Generate parking rectangles along streets within a defined bounding box.

**Constraints:**

* Manageable area size (zoom in on the map).
* Maximum 20 spots per street.
* No overlapping spots.
* Spot dimensions ≈ 2.5m x 5.0m.
* No spots at street corners.
* All streets are two-way.
* Reasonable API request limit (< 10,000).

**Available APIs:**

* `LatLng nearestStreetPoint(LatLng location)`: Returns the nearest street point to a given location.
* `int getDistance(LatLng location1, LatLng location2)`: Returns the distance between two locations in meters.

**Input:**

* `latitude_top_left`, `longitude_top_left`
* `latitude_bottom_right`, `longitude_bottom_right`

**Output:**

JSON array of parking rectangles:

```json
[
  {
    "id": 1,
    "a_latitude": ..., "a_longitude": ...,
    "b_latitude": ..., "b_longitude": ...,
    "c_latitude": ..., "c_longitude": ...,
    "d_latitude": ..., "d_longitude": ...
  },
  ...
]
```

## Example

**Input:**

```
37.423559
-122.085152
37.422971
-122.084319
```

**Output (Example):**

```json
[
  {
    "id": 1,
    "a_latitude": 37.423159, "a_longitude": -122.084858,
    "b_latitude": 37.423147, "b_longitude": -122.084858,
    "c_latitude": 37.423144, "c_longitude": -122.084826,
    "d_latitude": 37.423155, "d_longitude": -122.084824
  },
  ...
]
```
