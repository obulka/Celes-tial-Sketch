import base64
import json
import os
import multiprocessing as mp
import random
import time

import numpy as np

# Local Imports
from .fit_constellation import match, drawing_edges_to_star_edges
from .star_map import StarMap
from .star_parser import parse_star_query


def get_chunks():
    """"""
    division = len(chunks) / self._num_processes
    return [
        chunks[round(division * process):round(division * (process + 1))]
        for process in range(self._num_processes)
    ]


def create_star_map(request_data):
    num_stars_str = request_data.get("numStars")
    resolution_x_str = request_data.get("resolutionX")
    resolution_y_str = request_data.get("resolutionY")
    path = request_data.get("path")
    edges_str = request_data.get("edges")
    vertices_str = request_data.get("vertices")

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

    # base_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)))
    # data = parse_star_query(os.path.join(
    #     base_dir,
    #     os.pardir,
    #     os.pardir,
    #     "BrowseTargets.25333.1587902116",
    # ))
    start = time.time()

    num_processes = mp.cpu_count()

    star_map = StarMap(num_stars) #.from_database(data)
    chunk_size = 100

    chunks = np.array_split(
        star_map.angular_positions,
        star_map.num_stars / chunk_size + 1,
    )

    manager = mp.Manager()
    return_dict = manager.dict()

    jobs = []
    for index, chunk in enumerate(chunks):
        job = mp.Process(
            target=match,
            args=(index, return_dict, chunk, star_map, vertices, edges),
        )
        jobs.append(job)
        job.start()

    for job in jobs:
        job.join()

    lowest_weight = None
    best_match = None
    print(return_dict)
    for process_best in return_dict.values():
        if lowest_weight is None or process_best["weight"] < lowest_weight:
            best_match = process_best["match"]
            lowest_weight = process_best["weight"]

    print(lowest_weight)
    star_map.add_edges(drawing_edges_to_star_edges(edges, best_match))
    star_map.write_texture(resolution, path)

    print(time.time() - start)

    return json.dumps({"success": True}), 201
