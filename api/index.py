"""
Vercel serverless function for calculating parking rectangles.

This module provides an API endpoint that accepts bounding box coordinates
and returns parking rectangles calculated using the street lines algorithm.
The endpoint is designed to work with the Street Lines web dashboard.
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.street_lines_cli import calculate_parking_rectangles
import json

def handler(event, context):
    """
    Vercel serverless function handler for parking rectangle calculations
    """
    try:
        # Get query parameters
        query_params = event.get('queryStringParameters', {}) or {}

        # Extract coordinates from query parameters
        latitude_top_left = float(query_params.get('latitude_top_left', 0.0))
        longitude_top_left = float(query_params.get('longitude_top_left', 1.0))
        latitude_bottom_right = float(query_params.get('latitude_bottom_right', 2.0))
        longitude_bottom_right = float(query_params.get('longitude_bottom_right', 3.0))

        # Calculate parking rectangles
        rectangles_json = calculate_parking_rectangles(
            latitude_top_left,
            longitude_top_left,
            latitude_bottom_right,
            longitude_bottom_right
        )

        # Parse the JSON response
        rectangles = json.loads(rectangles_json)

        # Return successful response
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'GET, OPTIONS'
            },
            'body': json.dumps({
                'success': True,
                'data': rectangles
            })
        }

    except ValueError as e:
        # Handle validation errors
        return {
            'statusCode': 400,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'success': False,
                'error': f'Invalid input parameters: {str(e)}'
            })
        }

    except Exception as e:
        # Handle any other errors
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'success': False,
                'error': f'Server error: {str(e)}'
            })
        }