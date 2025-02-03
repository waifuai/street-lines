# street-lines: Approximating Road Line Segments and Parking Spaces

**street-lines** is a tool that approximates road line segments and potential curbside parking spots using a combination of mathematical algorithms and data from the Google Maps API. It is designed for developers who need to infer street geometry and parking spot locations without relying on massive datasets such as OpenStreetMap.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Setup & Installation](#setup--installation)
- [Usage](#usage)
- [Documentation](#documentation)
- [Testing](#testing)
- [License](#license)
- [Contributing](#contributing)

---

## Overview

The **street-lines** project takes a bounding box defined by geographic coordinates and uses the Google Maps API to query the nearest street points. With these data, the core algorithm calculates parking rectangles aligned with the street’s orientation. These rectangles are generated by:
- Translating geographic coordinates into a local Cartesian system.
- Creating a template rectangle with specific dimensions and an offset from the street center.
- Rotating and normalizing the coordinates to accurately approximate real-world positions.

This approach leverages mathematical transformations to produce accurate estimations of road and parking geometries in areas where direct data might not be available.

---

## Features

- **Mathematical Precision:** Uses a series of transformations (rotation, geographic normalization) to generate parking rectangles.
- **Google Maps API Integration:** Obtains street location data by querying the Google Maps API.
- **Error Analysis & Validation:** Provides documentation on error sources (e.g., the flat-Earth approximation) and methods for validation.
- **Comprehensive Documentation:** Detailed derivations and proofs are available to understand the algorithm’s mathematical foundations.
- **CLI and Web Integration:** A command-line interface (`src/main.py`) allows users to generate parking rectangles from bounding box coordinates.
- **Unit Testing:** Includes a suite of tests to verify the correctness of the algorithm.

---

## Architecture

The repository is structured as follows:

```
.
├── .gitignore             # Ignores __pycache__ directories and other unwanted files
├── LICENSE                # MIT No Attribution License
├── README.md              # Project overview and usage documentation
├── docs
│   ├── 1-proof.md         # Comprehensive proof and explanation of the algorithm
│   └── 2-derivation.md    # Intuitive step-by-step derivation of the algorithm
├── src
│   ├── main.py            # CLI entry point to calculate parking rectangles
│   └── street_lines_cli.py# Core implementation of the parking rectangle algorithm
└── tests
    └── test_street_lines_cli.py # Unit tests for validating the algorithm
```

---

## Setup & Installation

1. **Obtain a Google Maps API Key:**
   - Register on [Google Cloud](https://cloud.google.com/) and enable the Google Maps API.
   - Set the API key as an environment variable:
     ```bash
     export GOOGLE_MAPS_API_KEY=your_api_key_here
     ```

2. **Install Required Packages:**
   - Install dependencies using pip:
     ```bash
     pip install --user googlemaps requests
     ```

3. **Clone the Repository:**
   - Clone this repo to your local machine:
     ```bash
     git clone https://github.com/yourusername/street-lines.git
     cd street-lines
     ```

---

## Usage

### Command-Line Interface (CLI)

The main entry point is provided by the `src/main.py` script. Run it with the required bounding box coordinates:

```bash
python src/main.py --latitude_top_left 0.0 --longitude_top_left 1.0 --latitude_bottom_right 2.0 --longitude_bottom_right 3.0
```

This command calculates the parking rectangle(s) for the specified area and outputs a JSON array similar to:

```json
[
    {
        "id": 1,
        "a_longitude": 1.9999964079515018,
        "a_latitude": 1.0000208872816896,
        "b_longitude": 2.000013573713654,
        "b_latitude": 1.000062447060844,
        "c_longitude": 2.0000344904203717,
        "c_latitude": 1.0000539203207877,
        "d_longitude": 2.00001732465822,
        "d_latitude": 1.0000123605416336
    }
]
```

### Web Interface

A simple web interface is available via `index.html` (if provided separately). When opened in a browser, it automatically calls the `startConnect()` function after 3 seconds. You can also manually invoke this function from your browser’s JavaScript console to refine results.

---

## Documentation

Detailed documentation is provided in the `docs/` directory:

- **1-proof.md:**  
  Contains a comprehensive proof and explanation of the parking rectangle algorithm, including mathematical foundations, geometric interpretations, and error analysis.

- **2-derivation.md:**  
  Provides an intuitive, step-by-step derivation of the algorithm, explaining the conversion between geographic and local Cartesian coordinates, the construction of the template rectangle, and the rotation and normalization processes.

Refer to these documents for a deeper understanding of the underlying calculations and design decisions.

---

## Testing

Unit tests are provided to ensure the reliability and correctness of the algorithm. To run the tests, use:

```bash
python -m unittest discover tests
```

The tests cover:
- Validation of bounding box input.
- Correct JSON structure and content of the generated parking rectangles.
- Handling of invalid input parameters.

---

## License

This project is licensed under the **MIT No Attribution** License. See the [LICENSE](./LICENSE) file for details.

---

## Contributing

Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Write tests to cover your changes.
4. Submit a pull request detailing your changes.

For major changes, please open an issue first to discuss what you would like to change.

---

By combining rigorous mathematical methods with real-world data from the Google Maps API, **street-lines** provides a powerful solution for approximating road geometries and parking spaces. Whether you’re a developer working on mapping applications or a researcher exploring urban planning algorithms, this project offers a robust foundation that is both practical and well-documented.

---

*© 2025 WaifuAI*