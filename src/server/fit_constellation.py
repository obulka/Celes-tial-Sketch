import math
import numpy as np
import matplotlib.pyplot as plt

def find_longest_edge(verts,edges):
    """ Returns the longest """
    max_edge_length = 0
    longest_edge = 0
    for index,edge in enumerate(edges):
        edge_length = get_edge_length(verts,edge)
        if edge_length > longest_edge:
            longest_edge = edge_length
            longest_edge = index
    return longest_edge

def get_edge_length(verts, edge):
    """ Returns the length of edge """
    edge_length = np.sqrt(
        (verts[edge[0]][0] - verts[edge[1]][0])**2
        + (verts[edge[0]][1]-verts[edge[1]][1])**2
    )
    return edge_length


def match(starmap, verts, edges):
    longest_edge = find_longest_edge(verts,edges)
    fixed_vert = verts[edges[longest_edge][0]]

    #The relative positions of each
    relative_array = np.array(verts) - np.array(fixed_vert)

    #Want to minimize the weighted value of "badness" of fit
    lowest_weight = np.Inf
    #The ordered list of star indicies that best match to the verticies
    best_match = []

    for first_star, pos in enumerate(starmap.angular_positions):
        nearby_stars = starmap.get_stars_within_angle(first_star)
        #print(nearby_stars)

        for second_star in nearby_stars:
            #The distance to which we will normalize the longest edge
            normalizing_distance = starmap.get_distance_between_stars(first_star, second_star)
            #print(normalizing_distance)
            longest_edge_length = get_edge_length(relative_array, edges[longest_edge])
            #print(longest_edge_length)
            scaled_relative_array = relative_array * normalizing_distance / longest_edge_length
            #print(scaled_relative_array) #(maybe make this signed somehow?)
            drawing_angle = np.arctan2(
                scaled_relative_array[edges[longest_edge][1]][1],
                scaled_relative_array[edges[longest_edge][1]][0],
            )

            #print(drawing_angle)
            star_angle = starmap.get_angle_between_stars(first_star, second_star)

            differential_angle =  star_angle-drawing_angle
            #print(differential_angle)
            c, s = np.cos(differential_angle), np.sin(differential_angle)
            R = np.array(((c, -s), (s, c)))

            rotated_verts = np.array([np.matmul(R, coord) for coord in scaled_relative_array])

            projected_verts = rotated_verts + np.array(pos)

            weight = 0
            match = list()
            for vert_index, vert in enumerate(projected_verts):
                #Two stars should align exactly with the longest edge
                if vert_index == edges[longest_edge][0]:
                    match.append(first_star)
                elif vert_index == edges[longest_edge][1]:
                        match.append(second_star)
                #The remaining stars should be fitted as well as possible
                else:
                    star_index, distance_weight = starmap.get_distance_to_nearest_star(vert)
                    #TODO figure out how to weight this
                    weight += distance_weight
                    match.append(star_index)

            if weight < lowest_weight and len(np.unique(match)) == len(match) :
                lowest_weight = weight
                best_match = match
                print(best_match)

    return best_match


def get_angle_between_edges(verts_array,edge_1,edge_2):
    vector_1 = vert_array[edge_1[1]] - vert_array[edge_1[0]]
    vector_2 = vert_array[edge_2[1]] - vert_array[edge_2[0]]
    return np.arccos(np.dot(vector_2,vector_1))


def match_1(star_map, vertices, edges):
    vertices = np.array(vertices)
    edges = np.array(edges)

    for star_index, star_position in enumerate(star_map.angular_positions):
        for next_star in star_map.angular_positions[star_index + 1:]:
            star_difference = next_star - star_position
            distance_between_stars = np.linalg.norm(star_difference)

            angle_between_stars = np.arctan2(
                star_difference[1],
                star_difference[0],
            )

            for vertex_index, vertex in enumerate(vertices):
                normalized_vertices = vertices - vertex

                for edge in edges:
                    if edge[0] == vertex_index:
                        next_vertex = normalized_vertices[edge[1]]
                    elif edge[1] == vertex_index:
                        next_vertex = normalized_vertices[edge[0]]
                    else:
                        continue

                    vertex_difference = next_vertex - vertex
                    distance_between_vertices = np.linalg.norm(vertex_difference)

                    scaled_vertices = (
                        distance_between_stars
                        * normalized_vertices
                        / distance_between_vertices
                    )

                    angle_between_vertices = np.arctan2(
                        vertex_difference[1],
                        vertex_difference[0],
                    )

                    differential_angle = angle_between_stars - angle_between_vertices

                    cos_, sin_ = np.cos(differential_angle), np.sin(differential_angle)
                    rotation_matrix = np.array([[cos_, -sin_], [sin_, cos_]])

                    rotated_verts = np.array([
                        np.matmul(R, vertex) for vertex in scaled_vertices
                    ])

                    projected_constellation = rotated_verts + star_position





def drawing_edges_to_star_edges(edges, star_match):
    star_edges = []
    for edge in edges:
        star_edges.append((star_match[edge[0]],star_match[edge[1]]))
    return star_edges
