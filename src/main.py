# Constants
import argparse

from street_lines_cli import calculate_parking_rectangles

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--latitude_top_left", type=float, required=True, help="Latitude of the top-left corner")
    parser.add_argument("--longitude_top_left", type=float, required=True, help="Longitude of the top-left corner")
    parser.add_argument("--latitude_bottom_right", type=float, required=True, help="Latitude of the bottom-right corner")
    parser.add_argument("--longitude_bottom_right", type=float, required=True, help="Longitude of the bottom-right corner")
    args = parser.parse_args()

    rectangles_json = calculate_parking_rectangles(
        args.latitude_top_left,
        args.longitude_top_left,
        args.latitude_bottom_right,
        args.longitude_bottom_right
    )

    print(rectangles_json)

if __name__ == "__main__":
    main()