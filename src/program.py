# 3rd Party Imports
import matplotlib.pyplot as plt

# Local Imports
from server.webservices import create_star_map


def main():
    """
    """
    star_map = create_star_map({
        "num_stars": 1000,
        "path": "/home/ob1/software/qisk/citrus_hacks/tex.png",
        "resolution": (500, 1000),
    })
    print(star_map)


if __name__ == "__main__":
    main()
