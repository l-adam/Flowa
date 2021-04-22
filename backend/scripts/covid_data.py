import requests
import gmplot
import random
import os

#bg, hg, hd, bd:
limits_random = [
    [
        10.673389434814453,
        59.903573850545634
    ],
    [
        10.673389434814453,
        59.95638539185255
    ],
    [
        10.83749771118164,
        59.95638539185255
    ],
    [
        10.83749771118164,
        59.903573850545634
    ]]

# Builds the file without returning back to beginning of the line, it works but it doesn't look clean
# Returns a geojson file with random points to create an artificial dataset
def create_geojson_covid():
    geojson = {
                "type" : "FeatureCollection",
                "features" : [
                    
                ]
    }


    for lat_indice in range(10):
        for lon_indice in range(50):
            geojson["features"].append({
                                        "type" : "Feature",
                            "geometry" : {
                                "type" : "Point",
                                "coordinates" : 
                                    [
                                    limits_random[0][0] + (limits_random[3][0]-limits_random[0][0])*random.random(),
                                    limits_random[0][1] + (limits_random[1][1]-limits_random[0][1])*random.random()
                                    ],
                            },
                            "properties" : {
                                "probability" : "None"
                            }

                        })

    with open('oslo_covid_cases.geojson', 'w') as f:
        string_final1 = str(geojson)
        string_final2 = string_final1.replace("'",'"')
        f.write(string_final2)

create_geojson_covid()