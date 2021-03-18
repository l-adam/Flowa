

import requests
import gmplot
import random
import os
#"started_at": "2021-02-01 04:22:18.202000+00:00", "ended_at": "2021-02-01 04:31:31.215000+00:00", 
# "duration": 553, 
# "start_station_id": "433", "start_station_name": "Ila", 
# "start_station_description": "langs Uelandsgt ved Colletts", 
# "start_station_latitude": 59.931828, "start_station_longitude": 10.748745, 
# "end_station_id": "443", "end_station_name": "Sj\u00f8siden ved trappen", 
# "end_station_description": "Oslo S", 
# "end_station_latitude": 59.910154466964954, "end_station_longitude": 10.751980909227372}



r = requests.get('https://data.urbansharing.com/oslobysykkel.no/trips/v1/2021/02.json')

result = r.json()



#***************************************************************************************
#Date stuff :
#***************************************************************************************
import datetime
from datetime import time

date1 = result[0]["started_at"]
date2 = result[0]["ended_at"]


def get_date_object(str_date):
    list_date = str_date.split("+")
    date_time_obj = datetime.datetime.strptime(list_date[0], '%Y-%m-%d %H:%M:%S.%f')
    #date_time_obj.date()
    #date_time_obj.time()
    return(date_time_obj)

"""
d1 = get_date_object(date1)
d2 = get_date_object(date2)
print(d1.date(), " ", d1.time())
print(d2.date(), " ", d2.time())
print(d1-d2)
"""

def morning(obj_date):
    #str_morning_start = "04:22:18"
    #morning_start = datetime.datetime(year = 1, month = 1, day = 1, hour = 6,minute = 0,second = 1)
    #morning_end = datetime.datetime(year = 1, month = 1, day = 1, hour = 9, minute = 0, second = 0)
    morning_start = datetime.time(5,3)
    morning_end = datetime.time(9)
    if obj_date.time()<morning_end and obj_date.time() > morning_start:
        return True
    return False

    """
    comparison1 = morning_end-obj_date
    str_comparison1 = str(comparison1)
    l_comparison1 = str_comparison1.split(" ")
    comparison1_days = int(l_comparison1[0])
    comparison2 = obj_date-morning_start
    str_comparison2 = str(comparison2)
    l_comparison2 = str_comparison2.split(" ")
    comparison2_days = int(l_comparison2[0])
    if comparison1_days >= 0 and comparison2_days>=0:
        return True
    return False
    """


"""
list_departures = []
for i in range(len(result)):
    dic_travel=result[i]
    list_departures.append((dic_travel['start_station_latitude'],dic_travel['start_station_longitude']))

list_arrivals = []
for j in range(len(result)):
    dic_travel2=result[j]
    list_arrivals.append((dic_travel2['end_station_latitude'],dic_travel2['end_station_longitude']))
"""

list_departures_morning = []
list_arrivals_morning = []
dic_station_number = {}
for i in range(len(result)):
    station_id = result[i]["start_station_id"]
    if station_id not in dic_station_number:
        dic_station_number[station_id] = 1
    else:
        dic_station_number[station_id] +=1

    dic_travel=result[i]
    started_str = dic_travel['started_at']
    ended_str = dic_travel['ended_at']

    #print(i, "started_str : " + started_str)
    if len(started_str) >27 and len(ended_str)> 27:

        started_obj = get_date_object(started_str)
        ended_obj = get_date_object(ended_str)

        if morning(started_obj)==True:

            list_departures_morning.append((dic_travel['start_station_latitude'],dic_travel['start_station_longitude']))
            list_arrivals_morning.append((dic_travel['end_station_latitude'],dic_travel['end_station_longitude']))

#print("dico : ", dic_station_number)

"""
i_travel=0
for travel in result :
    date_str = travel['started_at']
    date_obj = get_date_object(date_str)
    print("travel n°", i_travel, " morning : ", morning(date_obj))
    i_travel+=1
"""


#***************************************************************************************
#Map building :
#***************************************************************************************
# Create the map plotter:
apikey = '' # (your API key here)
gmap = gmplot.GoogleMapPlotter(59.9127300, 10.7460900, 14, apikey=apikey)

# Mark a hidden gem:
#gmap.marker(latitude, longitude, color='cornflowerblue')

#departure_lats, departure_lngs = zip(*list_departures)
departure_lats_morning, departure_lngs_morning = zip(*list_departures_morning)
#gmap.scatter(departure_lats, departure_lngs, color='cornflowerblue', size=40, marker=False)

"""
print("lengths : ", len(list_departures_morning), len(list_arrivals_morning))
for couple_ind in range(len(list_departures_morning)):
    #gmap.marker(couple[0], couple[1], color=random_color(),size=40, marker=True)
    pathlat = [list_departures_morning[couple_ind][0],list_arrivals_morning[couple_ind][0]]
    pathlon = [list_departures_morning[couple_ind][1],list_arrivals_morning[couple_ind][1]]
    #gmap.plot(pathlat,pathlon,'cornflowerblue', edge_width=1)
"""

#***************************************************************************************
# OpenRoutesService :
#***************************************************************************************
"""
#chemin = gmap.directions((departure_lats[0],departure_lngs[0]), (departure_lats[4],departure_lngs[4]), Travel_mode = "BIKING")
import openrouteservice

coords = ((list_departures_morning[0][0], list_departures_morning[0][1]),(list_arrivals_morning[0][0],list_arrivals_morning[0][1]))
print("coords[0]: ", coords[0])
print("coords[0]2: ", coords[1])
client = openrouteservice.Client(key = '5b3ce3597851110001cf624866ba0ebc646646da998734147e57cf8b')
routes = client.directions(coords)
print(routes)
"""

#***************************************************************************************
# Build geoJson file :
#***************************************************************************************
#if needed, to draw polygons, etc, check : https://github.com/jazzband/geojson
# "type" : "LineString", "coordinates" :[[],[],[]]

# UNUSED METHOD ITS USELESS
def create_geojson():
    station_0 = result[0]
    geojson = {
                "type" : "FeatureCollection",
                "features" : [

                ]
    }

    for station in range(len(result)):
        station_i = result[station]
        geojson["features"].append({
                    "type" : "Feature",
                        "geometry" : {
                            "type" : "Point",
                            "coordinates" : [
                                station_i["start_station_latitude"],station_i["start_station_longitude"]
                            ]
                        },
                        "properties" : {
                            "started_at" : station_i["started_at"],
                            "ended_at" : station_i["ended_at"],
                            "duration": station_i["duration"],
                            "start_station_id": station_i["start_station_id"],
                            "start_station_name": station_i["start_station_name"],
                            "start_station_description": station_i["start_station_description"],
                            "start_station_latitude": station_i["start_station_latitude"],
                            "start_station_longitude": station_i["start_station_longitude"],
                            "end_station_id": station_i["end_station_id"],
                            "end_station_name": station_i["end_station_name"],
                            "end_station_description": station_i["end_station_description"],
                            "end_station_latitude": station_i["end_station_latitude"],
                            "end_station_longitude": station_i["end_station_longitude"]
                        }
                    })
    with open('myfile2.geojson', 'w') as f:
        f.write(str(geojson))

#create_geojson()





c_o = [10.68695068359375, 59.954838366826024] # = [longitude, latitude]
# Builds the file without returning back to beginning of the line, it works but it doesn't look clean
def create_geojson2():
    geojson = {
                "type" : "FeatureCollection",
                "features" : [
                    
                ]
    }
    # c_o[0] + 10**(-4)*4.07696*lon_indice
    # c_o[1] - 10**(-4)*2.04425*lat_indice
    increment_long = 10**(-4)*4.07696*2
    increment_lat = 10**(-4)*2.04425*2
    for lat_indice in range(130):
        for lon_indice in range(150):
            geojson["features"].append({
                                        "type" : "Feature",
                            "geometry" : {
                                "type" : "Polygon",
                                "coordinates" : [[
                                    
                                    [
                                    c_o[0] + increment_long*lon_indice,
                                    c_o[1] - increment_lat*lat_indice
                                    ],
                                    [
                                    c_o[0] + increment_long*(lon_indice + 1),
                                    c_o[1] - increment_lat*lat_indice
                                    ],
                                    [
                                    c_o[0] + increment_long*(lon_indice+1),
                                    c_o[1] - increment_lat*(lat_indice+1) 
                                    ],
                                    [
                                    c_o[0] + increment_long*lon_indice,
                                    c_o[1] - increment_lat*(lat_indice+1) 
                                    ],
                                    [
                                    c_o[0] + increment_long*lon_indice,
                                    c_o[1] - increment_lat*lat_indice
                                    ]
                                    
                                ]]
                            },
                            "properties" : {
                                "probability" : random.randint(0,255)
                            }

                        })

    with open('myfile2.geojson', 'w') as f:
        string_final1 = str(geojson)
        string_final2 = string_final1.replace("'",'"')
        f.write(string_final2)

create_geojson2()





# Builds the file returning back to beginning of the line, it works but it takes too much time to build the file (~116 minutes)
# how to make this more efficient?
def create_geojson3():
    geojson = "{\n  \"type\" : \"FeatureCollection\",\n  \"features\" : [  \n    ]\n}"
    index_add = 0
    for lat_indice in range(1000):
        for lon_indice in range(1000):
            index_add +=1
            new_el_str = ("    {\n      \"type\" : \"Feature\",\n      \"geometry\" : {\n        \"type\" : \"Polygon\",\n        \"coordinates\" : [\n          [\n            [\n              " 
            + str(c_o[1]+ 10**(-1)*lon_indice) + ",\n              " 
            + str(c_o[0]+ 10**(-1)*lat_indice) 
            + "\n            ],\n            [\n              " 
            + str(c_o[1]+ 10**(-1)*lon_indice +10**(-1)) 
            + ",\n              " 
            + str(c_o[0]+ 10**(-1)*lat_indice) 
            + "\n            ],            [\n              " 
            + str(c_o[1]+ 10**(-1)*lon_indice) 
            + ",\n              " 
            + str(c_o[0]+ 10**(-1)*lat_indice +10**(-1)) 
            + "\n            ],\n            [\n              " 
            + str(c_o[1]+ 10**(-1)*lon_indice +10**(-1)) 
            + ",\n              " 
            + str(c_o[0]+ 10**(-1)*lat_indice +10**(-1)) 
            + "\n            ]\n          ]\n        ]\n      },\n      \"properties\" : {\n        \"probability\" : random.randint(0,255)\n      }\n    }")
            if lat_indice!=999 and lon_indice != 999:
                new_el_str += ","
            insert_index = 57+index_add*len(new_el_str)
            geojson = geojson[:insert_index] + new_el_str + geojson[insert_index:]
            print(index_add)
    with open('myfile2.geojson', 'w') as f:
        f.write(str(geojson))

#create_geojson3()


# Draw the map to an HTML file:
#gmap.draw('map.html')

#***************************************************************************************

                                        
#color methods :
#***************************************************************************************

"""
# Outline the Golden Gate Park:
golden_gate_park = zip(*[
    (37.766227, -122.460213),
    (37.764028, -122.510347)
])
gmap.polygon(*golden_gate_park, color='cornflowerblue', edge_width=10)
"""

def random_color():
    colors = ['green', 'white', 'red', 'purple', 'yellow', 'pink', 'orange', 'cyan']
    return colors[random.randint(0,7)]

def random_color_hexa():
    letter = ['a','b','c','d','e','f']
    number = ['0','1','2','3','4','5','6','7','8','9']
    res = '#'
    while(len(res)<7):
        l_or_n = random.randint(0,1)
        if l_or_n == 0:
            new_el = random.randint(0,5)
        else:
            new_el = random.randint(0,9)
        res += str(new_el)
    return res