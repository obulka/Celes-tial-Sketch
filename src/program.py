# Standard Imports
import os

# 3rd Party Imports
import matplotlib.pyplot as plt


# Local Imports
from server.webservices import create_star_map
from server.fit_constellation import *
from server.webservices import StarMap

def main():
    """
    """
    base_dir = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        os.pardir,
    )
    star_map = create_star_map({
        "numStars": 1000,
        "path": os.path.join(base_dir, "texture.png"),
        "resolution": (500, 1000),
    })
    print(star_map)

    star_map = StarMap(100)
    # vertices = [(1,2),(4,5),(7,18)]
    # edges = [(0,1),(1,2),[2,0]]

    # print(match(star_map,vertices,edges))

if __name__ == "__main__":
    main()
