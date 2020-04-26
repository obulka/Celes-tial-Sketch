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

        self._angular_positions = np.random.rand(self._num_stars, 2) * np.pi
        self._angular_positions[:, 0] *= 2

    def write_texture(self, resolution, path):
        texture = np.empty((resolution[0], resolution[1], 3))
        texture[..., :] = self._background_colour

        image_positions = self._angular_positions / np.pi
        image_positions[:, 0] *= resolution[1] / 2 # x
        image_positions[:, 1] *= resolution[0] # y

        for position in image_positions.astype(int):
            cv2.circle(
                texture,
                tuple(position),
                self._stellar_radii,
                self._star_colour,
                -1,
            )
        cv2.imwrite(path, texture)

    @property
    def angular_positions(self):
        """"""
        return self._angular_positions

    def get_stars_in_radius(self, star_index, radius=0.5):
        """
        """
        pass

    def get_distance_between_stars(self, star_index_0, star_index_1):
        """
        """
        position_0 = self._angular_positions[star_index_0]
        position_1 = self._angular_positions[star_index_1]

        return np.arccos(np.dot(position_0, position_1))


    def get_distance_to_nearest_star(self, angular_position):
        """
        """
        index = 0
        distance = 0
        return index, distance


def create_star_map(request_data):
    num_stars = request_data.get("num_stars")
    path = request_data.get("path")
    resolution = request_data.get("resolution")

    if not num_stars or not path or not resolution:
        return json.dumps({"success": False, "failureInfo": "Request data missing"}), 400

    star_map = StarMap(num_stars)

    star_map.write_texture(resolution, path)

    return json.dumps({"success": True})
