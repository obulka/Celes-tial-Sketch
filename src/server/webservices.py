import base64
import json

from flask import Flask, request
import numpy as np
import cv2


class StarMap:

    def __init__(
            self,
            num_stars,
            background_colour=[0, 0, 0],
            star_colour=[255, 255, 255],
            stellar_radii=1):
        self._num_stars = num_stars
        self._background_colour = background_colour
        self._star_colour = star_colour
        self._stellar_radii = stellar_radii
        self._edges = []

        self._angular_positions = np.random.rand(self._num_stars, 2) * np.pi
        self._angular_positions[:, 0] *= 2

    def write_texture(self, resolution, path):
        texture = np.empty((resolution[0], resolution[1], 3))
        texture[..., :] = self._background_colour

        image_positions = self._angular_positions / np.pi
        image_positions[:, 0] *= resolution[1] / 2 # x
        image_positions[:, 1] *= resolution[0] # y
        image_positions = image_positions.astype(int)

        for position in image_positions:
            cv2.circle(
                texture,
                tuple(position),
                self._stellar_radii,
                self._star_colour,
                -1,
            )

        for edge in self._edges:
            point_0 = image_positions[edge[0]]
            point_1 = image_positions[edge[1]]
            cv2.line(
                texture,
                tuple(point_0),
                tuple(point_1),
                self._star_colour,
                self._stellar_radii,
            )

        cv2.imwrite(path, texture)

    @property
    def angular_positions(self):
        """"""
        return self._angular_positions

    @property
    def edges(self):
        return self._edges

    def add_edges(self, new_edges):
        self._edges.extend(new_edges)

    def get_stars_within_angle(self, star_index, angle=0.5):
        """
        """
        indices = []
        for index, position in enumerate(self._angular_positions):
            if index == star_index:
                continue
            angular_distance = self._distance_between_angular_positions(
                position,
                self._angular_positions[star_index],
            )
            if angular_distance < angle:
                indices.append(index)

        return indices

    def get_angle_between_stars(self, index_0, index_1):
        difference = self._angular_positions[index_1] - self._angular_positions[index_0]
        return np.arctan2(difference[1], difference[0])

    @staticmethod
    def _distance_between_angular_positions(position_0, position_1):
        """
        """
        delta_lambda = position_1[0] - position_0[0]

        return np.arccos(
            np.sin(position_0[1])
            * np.sin(position_1[1])
            + np.cos(position_0[1])
            * np.cos(position_1[1])
            * np.cos(delta_lambda)
        )

    def get_distance_between_stars(self, star_index_0, star_index_1):
        """
        """
        position_0 = self._angular_positions[star_index_0]
        position_1 = self._angular_positions[star_index_1]

        return self._distance_between_angular_positions(position_0, position_1)

    def get_distance_to_nearest_star(self, angular_position):
        """
        """
        distances = [
            self._distance_between_angular_positions(position, angular_position)
            for position in self._angular_positions
        ]
        return np.argmin(distances), np.min(distances)


def create_star_map(request_data):
    num_stars = request_data.get("numStars")
    path = request_data.get("path")
    resolution = request_data.get("resolution")

    if not num_stars or not path or not resolution:
        return json.dumps({"success": False, "failureInfo": "Request data missing"}), 400

    star_map = StarMap(num_stars)

    star_map.add_edges([(0, 1), (1, 2), (2, 3), (3, 0)])

    star_map.write_texture(resolution, path)

    return json.dumps({"success": True})
