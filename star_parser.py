
import numpy as np

def parse_star_query(filename):
    #filename = "BrowseTargets.25333.1587902116"
    #Star data from https://heasarc.gsfc.nasa.gov/db-perl/W3Browse/w3query.pl

    f = open(filename,"r")

    got_names = False
    stars = list()
    for x in f:
        if x[0] == "|":
            if not got_names:
                got_names = True
            else:
                axial_string = x[20:31]
                azimuthal_string = x[32:43]

                hour = int(axial_string[0:2])
                min = int(axial_string[3:5])
                sec = int(axial_string[6:8])
                ms = int(axial_string[9:11])

                hour += min/60 +sec/(60*60) + ms/(60*60*10)
                axial_angle = hour/24*2*np.pi

                sign = 1
                if azimuthal_string[0] == "-":
                    sign = -1
                azimuthal_angle = int(azimuthal_string[1:3])
                azimuthal_angle += int(azimuthal_string[4:6])/100
                azimuthal_angle += int(azimuthal_string[7:9])/10000
                azimuthal_angle += int(azimuthal_string[10])
                azimuthal_angle = azimuthal_angle*sign
                azimuthal_angle += 90
                azimuthal_angle = azimuthal_angle*np.pi/180

                stars.append(axial_angle,azimuthal_angle)
    f.close()
    return stars
