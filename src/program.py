# Standard Imports
import os
import time

# 3rd Party Imports
import matplotlib.pyplot as plt

# Local Imports
from citrus.webservices import create_star_map


def main():
    """
    """
    base_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)))

    # star_map = create_star_map({
    #     "numStars": 1000,
    #     "path": os.path.join(base_dir, os.pardir, "texture.png"),
    #     "resolutionX": 1000,
    #     "resolutionY": 2000,
    #     "edges": "[[0, 1], [1, 2], [2, 3], [3, 4], [4, 0]]",
    #     "vertices": "[[490, 437], [336, 134], [670, 270], [297, 294], [613, 116]]",
    # })
    # print(star_map)

    app_path = os.path.join(base_dir, "app/Citrus.exe")
    server_path = os.path.join(base_dir, "server.py")

    try:
        os.system(f"{app_path} & python3 {server_path}")

        while True:
            time.sleep(3)

    except KeyboardInterrupt as error:
        print(error)


if __name__ == "__main__":
    main()
