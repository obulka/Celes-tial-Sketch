import math
import numpy as np


def find_longest_edge(verts, edges):
    max_edge_length = 0
    longest_edge = 0
    for index,edge in enumerate(edges):
        edge_length = get_edge_length(verts,edge)
        if edge_length > longest_edge:
            longest_edge = edge_length
            longest_edge = index
    return longest_edge


def get_edge_length(verts, edge):
    edge_length = np.sqrt(
        (verts[edge[0]][0] - verts[edge[1]][0])**2
        + (verts[edge[0]][1]-verts[edge[1]][1])**2
    )
    return edge_length


def match(starmap, verts, edges):
    longest_edge = find_longest_edge(verts, edges)
    fixed_vert = verts[longest_edge[0]]

    #The relative positions of each
    relative_array = np.array(verts) - np.array(verts[fixed_vert])

    lowest_weight = np.Inf
    best_match = list()

    for first_star, pos in enumerate(starmap.angular_positions):
        nearby_stars = starmap.get_stars_within_angle(first_star)

        for second_star in nearby_stars:
            #The distance to which we will normalize the longest edge
            normalizing_distance = abs(starmap.get_distance_between_stars(first_star, second_star))
            longest_edge_length = get_edge_length(relative_array,longest_edge)
            scaled_relative_array = relative_array * normalizing_distance / longest_edge_length

            drawing_angle = np.arctan2(
                scaled_relative_array[edges[longest_edge]][1],
                scaled_relative_array[edges[longest_edge]][0],
            )
            star_angle = starmap.get_angle_between_starts(first_star, second_star)

            differential_angle = drawing_angle - star_angle;

            c, s = np.cos(differential_angle), np.sin(differential_angle)
            R = np.array(((c, -s), (s, c)))
            #I think thisneeds to loop over each and then do matrix math
            rotated_verts = np.matmul(R, scaled_relative_array)
            projected_verts = rotated_verts + np.array(pos)

            weight = 0
            match = list()
            for vert_index, vert in enumerate(projected_verts):
                star_index, distance_weight = starmap.get_distance_to_nearest_star(vert)
                weight += distance_weight
                match.append((vert_index, star_index))

            if weight < lowest_weight:
                lowest_weight = weight
                best_match = match

    return best_match
