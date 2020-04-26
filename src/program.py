# Standard Imports
import os
import time

# 3rd Party Imports
import matplotlib.pyplot as plt

# Local Imports
from citrus.webservices import create_star_map, StarMap


def main():
    """
    """
    base_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)))
    app_path = os.path.join(base_dir, "app/Citrus.exe")
    server_path = os.path.join(base_dir, "server.py")

    try:
        os.system(f"{app_path} & python3 {server_path}")

        while True:
            time.sleep(3)

    except KeyboardInterrupt as error:
        print(error)

    # star_map = create_star_map({
    #     "numStars": 200,
    #     "path": os.path.join(base_dir, "texture.png"),
    #     "resolution": (500, 1000),
    #     "edges": [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0)],#[(0,1),(1,2),(2,3),(3,0)],
    #     "vertices": [[490, 437], [336, 134], [670, 270], [297, 294], [613, 116]], #[(1,1),(2,1),(2,2),(1,2)],
    # })


if __name__ == "__main__":
    main()
