import base64
import json
import os

from .fit_constellation import match, drawing_edges_to_star_edges
from .star_map import StarMap
from .star_parser import parse_star_query


def create_star_map(request_data):
    num_stars_str = request_data.get("numStars")
    resolution_x_str = request_data.get("resolutionX")
    resolution_y_str = request_data.get("resolutionY")
    path = request_data.get("path")
    edges_str = request_data.get("edges")
    vertices_str = request_data.get("vertices")
    database = False # request_data.get("database")

    if not num_stars_str or not resolution_x_str or not resolution_y_str or not path or not edges_str or not vertices_str:
        return json.dumps({"success": False, "failureInfo": "Request data missing"}), 400

    try:
        resolution = (int(resolution_x_str), int(resolution_y_str))
        num_stars = int(num_stars_str)
    except ValueError:
        return json.dumps({"success": False, "failureInfo": "Invalid resolution/num_stars format"}), 400

    try:
        edges = json.loads(edges_str)
        vertices = json.loads(vertices_str)
    except json.JSONDecodeError:
        return json.dumps({"success": False, "failureInfo": "Invalid edges/vertices format"}), 400

    if database:
        base_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)))
        data = parse_star_query(os.path.join(
            base_dir,
            os.pardir,
            os.pardir,
            "BrowseTargets.25333.1587902116",
        ))
        star_map = StarMap.from_database(data)
    else:
        star_map = StarMap(num_stars)
    star_map.add_edges(drawing_edges_to_star_edges(edges, match(star_map, vertices, edges)))
    star_map.write_texture(resolution, path)

    return json.dumps({"success": True}), 201
