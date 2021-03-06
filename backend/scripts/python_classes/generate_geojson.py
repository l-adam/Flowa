import tools
import data_from_excel


import requests
import gmplot
import random
import os

import datetime
from datetime import time

import geojson	
from shapely.geometry import Polygon
from shapely.ops import cascaded_union

#use

class Generate_geojson():
    def __init__(self, title = None):

        # 'Bjerke':(59.940668, 10.808725)
        #'Gamle Oslo':(59.899237, 10.734767)
        self.string_month = ['2020-04.geojson', '2020-05.geojson', '2020-06.geojson', 
        '2020-07.geojson', '2020-08.geojson', '2020-09.geojson', '2020-10.geojson', 
        '2020-11.geojson', '2020-12.geojson', '2021-01.geojson', '2021-02.geojson', 
        '2021-03.geojson', '2021-04.geojson']

        self.places_coordinates = {'Gamle Oslo':(59.90500, 10.739767), 'Grunerlokka':(59.921875, 10.771906), 'Sagene':(59.937439, 10.760452), 
                        'St. Hanshaugen':(59.92795, 10.738958), 'Frogner':(59.917606, 10.710252), 'Ullern':(59.924469, 10.65988), 
                        'Vestre Aker':(59.9583, 10.670319), 'Nordre Aker':(59.953638, 10.756412), 'Bjerke':(59.943668, 10.808725), 
                        'Grorud':(59.961424, 10.880549), 'Stovner':(59.958595, 10.927285), 'Alna':(59.93092, 10.85403), 
                        'Ostensjo':(59.887563, 10.832748), 'Nordstrand':(59.859314, 10.801257), 'Sondre Nordstrand':(59.845535, 10.807981)}
        self.places_name = list(self.places_coordinates.keys())
        self.ids = {'Gamle Oslo':'gamle_oslo', 'Grunerlokka':'grunerlokka', 'Sagene':'sagene', 
                        'St. Hanshaugen':'hanshaugen', 'Frogner':'frogner', 'Ullern':'ullern' ,
                        'Vestre Aker':'vestre_aker', 'Nordre Aker':'nordre_aker', 'Bjerke':'bjerke', 
                        'Grorud':'grorud', 'Stovner':'stovner', 'Alna':'alna', 
                        'Ostensjo':'ostensjo', 'Nordstrand':'nordstrand', 'Sondre Nordstrand':'sondre_nordstrand'}

        self.alphabet = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
        self.months = ['Jan','Feb','March','April','May','June','July','Aug','Sept','Oct','Nov','Dec']

        # we instanciate the class Data_from_excel() and we generate the variables we need from it
        self.init_dfe = data_from_excel.Data_from_excel()
        self.global_station_hub = self.init_dfe.station_hub() # dico pour chaque id de station:[(lat, long), distance_closest_test_center, 'Name_closest_test_center']
        self.global_station_hub_keys = list(self.global_station_hub.keys())
        self.data_covid = self.init_dfe.test_station_amount_cases() #returns a dictionnary with test_center_name: amount of cases since march 2020 to march 2021 included
        self.ntl_dico = self.init_dfe.new_to_legacy_dico()
        self.ltn_dico = self.init_dfe.legacy_to_new_dico()

        # we instantiate the class Tools()
        self.init_tools = tools.Tools()

        self.compt = [0,0,0,0,0]
        self.compt_it = 0
        self.unefois=0
        self.dixfois = 0
    #indice_starting_month in [0:11]
    # filled with NEW ids
    def for_each_month_map(self):
        map_number = 0

        
        r = requests.get('https://data.urbansharing.com/oslobysykkel.no/trips/v1/2020/03.json')        
        result = r.json()
        
        amount_travels_bfore = self.init_tools.fill_departures_list2(result)
        

        index_month = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
        
        i_month = 3
        str_i_month = index_month[i_month]
        index_month_relevant=1
    
        amount_travels_month =[]
        
        for i in range(10):
       
            
            str_i_month = index_month[i_month]
            print("str:", str_i_month)
            r = requests.get('https://data.urbansharing.com/oslobysykkel.no/trips/v1/2020/' + str(str_i_month) + '.json')        
            result = r.json()
            
            amount_travels_dico = self.init_tools.fill_departures_list2(result)
            #print(amount_travels_dico)
            #print(amount_travels_bfore)

            #ici changer en create_matrix_square_station2()
            self.create_matrix_square_station(index_month_relevant, result, map_number, amount_travels_bfore, amount_travels_dico)
            print("compt ",self.compt_it, " : ", self.compt)
            self.compt = [0,0,0,0,0]
            self.compt_it +=1
            amount_travels_bfore = self.init_tools.fill_departures_list2(result)
            
            index_month_relevant += 1
            i_month +=1
            i_month = i_month%12
            print("imonth: ",i_month)
            
            map_number +=1
           
        for i in range(3):
            
            str_i_month = index_month[i_month]
            
            r = requests.get('https://data.urbansharing.com/oslobysykkel.no/trips/v1/2021/' + str(str_i_month) + '.json')        
            result = r.json()

            
            amount_travels_dico = self.init_tools.fill_departures_list2(result)
            self.create_matrix_square_station(index_month_relevant, result, map_number, amount_travels_bfore, amount_travels_dico)
            print("compt ",self.compt_it, " : ", self.compt)
            self.compt = [0,0,0,0,0]
            self.compt_it +=1
            amount_travels_bfore = self.init_tools.fill_departures_list2(result)
            
            index_month_relevant +=1
            i_month +=1
            i_month = i_month%12
            
            map_number +=1
        

    # generates a geojson file with the link between the different data sources
    def create_matrix_square_station(self, month_num, json_file, map_number, amount_travels_bfore, amount_travels_dico):
        #c_o = [10.635, 59.94] # = [longitude, latitude]
        c_o = [10.615, 59.975]
        print("start create_matrix_square_station() ")
        geojson = {
                    "type" : "FeatureCollection",
                    "features" : [
                        
                    ]
        }
        # c_o[0] + 10**(-4)*4.07696*lon_indice
        # c_o[1] - 10**(-4)*2.04425*lat_indice
        increment_long = 10**(-4)*4.07696*2
        increment_lat = 10**(-4)*2.04425*2
        #220, 200
        for lat_indice in range(400):#hauteur
            for lon_indice in range(390):#largeur
                if lon_indice<170 and lat_indice>200:
                    pass
                else:
                    # here it can be optimised:
                    gcbs_stat = self.get_closest_bike_station(self.init_tools.get_center_rectangle(c_o[1] - increment_lat*lat_indice, c_o[0] + increment_long*lon_indice, c_o[1] - increment_lat*(lat_indice+1), c_o[0] + increment_long*(lon_indice + 1))[0],self.init_tools.get_center_rectangle(c_o[1] - increment_lat*lat_indice, c_o[0] + increment_long*lon_indice, c_o[1] - increment_lat*(lat_indice+1), c_o[0] + increment_long*(lon_indice + 1))[1])[0]
                    ctb = self.compare_then_proba(month_num, self.legacy_to_new(gcbs_stat), json_file, amount_travels_bfore, amount_travels_dico)#month num, bike station id  compare_then_proba(month_num, bike_station_id, json_file):
                    geojson["features"].append({
                                                "type" : "Feature",
                                    "geometry" : {
                                        "type" : "Polygon",
                                        #bg, hg, hd, bd, bg
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
                                        #bg, bd, hg
                                        #"center" : get_center_rectangle(c_o[1] - increment_lat*lat_indice, c_o[0] + increment_long*lon_indice, c_o[1] - increment_lat*(lat_indice+1), c_o[0] + increment_long*(lon_indice + 1)),
                                        "closest_station_bike": gcbs_stat,
                                        "closest_test_station": self.global_station_hub[gcbs_stat][2],
                                        #"closest_test_center_coordinates": places_coordinates[global_station_hub[gcbs_stat][2]],
                                        "probability" : ctb
                                    }

                                })

        with open('bike_covid_' + self.string_month[map_number], 'w') as f:
            string_final1 = str(geojson)
            string_final2 = string_final1.replace("'",'"')
            f.write(string_final2)
            #print("end create_matrix_square_station() ")


# generates a geojson file with the coordinates of all the test stations
    def create_test_stations(self, month):
        print("start create_test_stations() ")
        geojson = {
                    "type" : "FeatureCollection",
                    "features" : [
                        
                    ]
        }
        for name_station in self.places_name:
            number_cases = self.data_covid[name_station][month]
            number_cases = number_cases.replace(" ", "")
            geojson["features"].append({
                                        "type" : "Feature",
                            "geometry" : {
                                "type" : "Point",
                                "coordinates" : [self.places_coordinates[name_station][1], self.places_coordinates[name_station][0]]  
                                
                            },
                            "properties" : {
                                "id": self.ids[name_station],
                                "name_place": name_station,
                                "cases_this_month": int(number_cases)
                            }

                        })
        
        with open('test_stations_' + self.string_month[month], 'w') as f:
            string_final1 = str(geojson)
            string_final2 = string_final1.replace("'",'"')
            f.write(string_final2)
            print("end create_test_stations() ")
        
    # generates a geojson file with the coordinates of all the bike stations {legacy_id : [lat, long]}
    def create_bike_stations(self, month, jsf):
        #returns dictionnary with bike_station_new_id (string): amount of uses this month (int) (the month of the json_file)
        dsn = self.init_tools.fill_departures_list2(jsf)
        #print("start create_bike_stations() ")
        # legacy_id : coord
        dico_from_excel = self.init_dfe.bike_station_coord()
        geojson = {
                    "type" : "FeatureCollection",
                    "features" : [
                        
                    ]
        }
        #list(dico_from_excel.keys())
        for new_id in list(dsn.keys()):
            amount_travel = dsn[new_id]
            legacy_dico = self.init_dfe.new_to_legacy_dico()
            try:
                legacy = legacy_dico[new_id]
            except:
                legacy = legacy_dico['606']
            geojson["features"].append({
                                        "type" : "Feature",
                            "geometry" : {
                                "type" : "Point",
                                "coordinates" : [dico_from_excel[legacy][1], dico_from_excel[legacy][0]]  
                                
                            },
                            "properties" : {
                                "name_place": new_id,
                                "amount_travels": amount_travel
                            }

                        })

        with open('bike_stations' + self.string_month[month], 'w') as f:
            string_final1 = str(geojson)
            string_final2 = string_final1.replace("'",'"')
            f.write(string_final2)
            #print("end create_bike_stations() ")

    # month_num in [0:12], 0-> march 2020, 12-> march 2021
    # station_id : new
    # returns 1 when there is increase of bikes use -> increase of amount of cases, 
    # returns -1 when there is decrease of bikes use -> decrease of amount of cases, 
    # 2 if the increase of the use of bikes -> decrease of the amount of cases
    # -2 if the decrease of the use of bikes -> increase of the amount of cases
    # 0 else
    def compare_then_proba(self, month_num, bike_station_id, json_file, amount_travels_bfore, amount_travels_dico):
    #print("start compare_then_proba(", month_num, ", ", bike_station_id, ", json_file, ", "amount_travels_bfore", ")")
    # amount of travels this month:
        try:
            amount_travels = amount_travels_dico[bike_station_id]

            #covid:  global_station_hub = station_hub() # dico pour chaque id de station:[(lat, long), distance_closest_test_center, 'Name_closest_test_center']
            legacy_id = self.new_to_legacy(bike_station_id)
            linked_test_center = self.global_station_hub[legacy_id][2]
            #print("linked test center : ", linked_test_center)

            # data_covid : returns a dictionnary with test_center_name: amount of cases since march 2020 to march 2021 included
            data_covid_station = self.data_covid[linked_test_center]
            data_covid_station_month = int(data_covid_station[month_num])
            data_covid_station_month_bfore = int(data_covid_station[month_num-1])
            #print("covid : ", data_covid_station_month, data_covid_station_month_bfore)

            # >0 -> augmentation
            # <0 -> diminution
            #print("bikes : ", amount_travels, amount_travels_bfore[bike_station_id])
            comparison_bike = amount_travels-amount_travels_bfore[bike_station_id]
            comparison_test = data_covid_station_month-data_covid_station_month_bfore
            """
            if comparison_bike > 0 and comparison_test>0:
                print("1")
                return 1
            elif comparison_bike < 0 and comparison_test<0:
                print("-1)")
                return -1
            elif comparison_bike > 0 and comparison_test<0:
                print("2")
                return 2
            elif comparison_bike < 0 and comparison_test>0:
                print("-2")
                return -2
            else:
                print(comparison_bike, " ", comparison_test)
                return 0
            """
            
            if comparison_bike > 0 and comparison_test>0:
                #print("4")
                self.compt[4]+=1
                return 4
            elif comparison_bike < 0 and comparison_test<0:
                #print("-1)")
                self.compt[3]+=1
                return 3

            elif comparison_bike > 0 and comparison_test<0:
                #print("2")
                self.compt[0]+=1
                return 0
            elif comparison_bike < 0 and comparison_test>0:
                #print("-2")
                self.compt[2]+=1
                return 2
            else:
                #print(comparison_bike, " ", comparison_test)
                self.compt[2]+=1
                return 2
        except:
            #print("2")
            return 2
    
            
        #print("end compare_then_proba()")
        return 2

    #parameter = coordinates point from which we want the closest station
    #returns station_id, distance
    def get_closest_bike_station(self, lat, longi):
        closest_station = self.global_station_hub_keys[0]
        shortest_distance = self.init_tools.distance(self.global_station_hub[closest_station][0][0], self.global_station_hub[closest_station][0][1], lat, longi)
        for key in self.global_station_hub_keys:
            lat_key, long_key = self.global_station_hub[key][0][0], self.global_station_hub[key][0][1]
            if self.init_tools.distance(lat_key, long_key, lat, longi)<shortest_distance:
                shortest_distance = self.init_tools.distance(lat_key, long_key, lat, longi)
                closest_station = key
        return closest_station, shortest_distance

    # returns the legacy id of a new id
    def new_to_legacy(self, new_id):
        return self.ntl_dico[str(new_id)]
    
    # returns the new id from a legacy id
    # ltn_dico hasn't been generated because we don't need it for now
    # if you need it, generate ltn_dico the same way ntl_dico has been generated in new_to_legacy()
    def legacy_to_new(self, legacy_id):
        return self.ltn_dico[str(legacy_id)]

    # generates a geojson file with fake shit
    def fake(self, end_name):
        #print("start fake() ")
        #g??n??rer n points random dans la matrice
        c_o = [10.665, 59.97] # = [longitude, latitude]
        # 10.665 -> 10.828078399999999
        # entre 66500 et 82807 /10**5
        # 59.97 -> 60.059947
        # 59 970 000 -> 60 059 947 / 10**6
        # entre 5994 et 97000 /10**5
        random_points = []
        for i in range(3):
            random_long = 10 + random.randint(66500,82807)/10**5
            random_lat = random.randint(59970000, 60059947)/10**6
            random_points.append((random_long, random_lat))
        print("random_points: ",random_points)

        geojson = {
                    "type" : "FeatureCollection",
                    "features" : [
                        
                    ]
        }
        # c_o[0] + 10**(-4)*4.07696*lon_indice
        # c_o[1] - 10**(-4)*2.04425*lat_indice
        increment_long = 10**(-4)*4.07696*2
        increment_lat = 10**(-4)*2.04425*2
        """
        #44000 squares
        for lat_indice in range(220):
            for lon_indice in range(200):

        """
        #156000 squares - 170*200 = 122000
        for lat_indice in range(400):#hauteur
            for lon_indice in range(390):#largeur
                if lon_indice<170 and lat_indice>200:
                    pass
                else:
                    fake_value = self.get_fake_value(random_points, c_o[0] + 10**(-4)*4.07696*lon_indice,c_o[1] - 10**(-4)*2.04425*lat_indice)
                    geojson["features"].append({
                                                "type" : "Feature",
                                    "geometry" : {
                                        "type" : "Polygon",
                                        #bg, hg, hd, bd, bg
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
                                        #bg, bd, hg
                                        #"center" : get_center_rectangle(c_o[1] - increment_lat*lat_indice, c_o[0] + increment_long*lon_indice, c_o[1] - increment_lat*(lat_indice+1), c_o[0] + increment_long*(lon_indice + 1)),
                                        "value": fake_value
                                    }

                                })

        with open('fake_data_' + end_name , 'w') as f:
            string_final1 = str(geojson)
            string_final2 = string_final1.replace("'",'"')
            f.write(string_final2)
            #print("end fake() ")
    
    #returns a number depending on how far (longi, lati) is from the closest point of list_points
    def get_fake_value(self, list_points, longi, lati):
        #value ranging from 0 to 20
        # 0.07 -> 0.12
        value = 10
        biggest_value = 10

        for point in list_points:
            dist = self.init_tools.distance(lati, longi, point[1], point[0])

            #break?
            if dist<0.9:
                value = 0
            if dist < 0.8:
                value = 1
            if dist<0.7:
                value = 2
            if dist<0.6:
                value = 3
            if dist<0.5:
                value = 5
            if dist<0.4:
                value = 6
            if dist<0.3:
                value = 7
            if dist<0.2:
                value =  8        
            if dist<0.1:
                value = 9
            if dist<0.09:
                value = 11
            if dist < 0.08:
                value = 12
            if dist<0.07:
                value = 13
            if dist<0.06:
                value = 14
            if dist<0.05:
                value = 15
            if dist<0.04:
                value = 17
            if dist<0.03:
                value = 18
            if dist<0.02:
                value =  19        
            if dist<0.01:
                value = 20
            if value>biggest_value:
                biggest_value = value
        
        return biggest_value


    def get_dansleau(self):
        nom_ccnc ={}
        for place in self.places_coordinates:
            nom_ccnc[place] = self.places_coordinates[place][0]

        dic2=dict(sorted(nom_ccnc.items(),key= lambda x:x[1]))
        print(dic2)
        return nom_ccnc

    # reads the bike_covid geojson files and merge the polygons with the same value to make final files smaller
    # Before runnung this program you need to make sure the folder backend/export/sources contains all the files bike_covid_date.geojson 
    def read_zone(self):
        #https://stackoverflow.com/questions/34325030/merging-two-geojson-polygons-in-python
        indices_rz = [0,2,3,4]
        polys0 = []
        polys2 = []
        polys3 = []
        polys4 = []
        # working directory (here python_classes)
        wd = os.getcwd()
        os.chdir('../../export/sources') 
        geojsons_folder = os.getcwd()

        #for str_m in self.string_month:
        #    doc_name = 'bike_covid_' + str_m
        global_end=''
        for end_name in self.string_month:

            name_file = 'bike_covid_' + end_name
            global_end = end_name
            with open(geojsons_folder + '/' + name_file) as f:
                geojson_file = geojson.load(f)
                features = geojson_file['features']
                for dic in features :
                    comparison_number = dic['properties']['probability']
                    poly_coordinates = dic['geometry']['coordinates'] # [[[lat1, long1], [lat2, long2]]]
                    
                    list_poly_coordinates = poly_coordinates[0]
                    list_poly_coordinates_rw = []
                    for coord in list_poly_coordinates:
                        list_poly_coordinates_rw.append((coord[0], coord[1]))
                    #print(comparison_number)
                    #print(list_poly_coordinates_rw)

                    if comparison_number ==4:
                        polys4.append(Polygon(list_poly_coordinates_rw))

                    elif comparison_number ==3:
                        polys3.append(Polygon(list_poly_coordinates_rw))


                    elif comparison_number ==0:
                        polys0.append(Polygon(list_poly_coordinates_rw))

                    elif comparison_number ==2:
                        polys2.append(Polygon(list_poly_coordinates_rw))  
                f.close()        
            
            u0 = cascaded_union(polys0)
            u2 = cascaded_union(polys2)
            u3 = cascaded_union(polys3)
            u4 = cascaded_union(polys4)
            unions = [u0, u2, u3, u4]
            
            features = []
            for i in range(4):
                geojson_out = geojson.Feature(geometry=unions[i], properties={"probability": indices_rz[i]})
                features.append(geojson_out)

            feature_collection = geojson.FeatureCollection(features)
            with open('bike_covid2_' + global_end, 'w') as f2:
                string_final1 = str(feature_collection)
                string_final2 = string_final1.replace("'",'"')
                f2.write(string_final2)
                #print("end fake() ")
                f2.close()
            polys0 = []
            polys2 = []
            polys3 = []
            polys4 = []
    
    # same algorithm as above but for the fake source
    def read_zone_fake(self):
        #https://stackoverflow.com/questions/34325030/merging-two-geojson-polygons-in-python
        indices_rz = [0, 1, 2, 3, 5, 6, 7, 8, 9,10, 11, 12, 13, 14, 15, 17, 18, 19, 20]
        polys0 = []
        polys1 = []
        polys2 = []
        polys3 = []
        polys5 = []
        polys6 = []
        polys7 = []
        polys8 = []
        polys9 = []
        polys10 = []
        polys11 = []
        polys12 = []
        polys13 = []
        polys14 = []
        polys15 = []
        polys17 = []
        polys18 = []
        polys19 = []
        polys20 = []
        # working directory (here python_classes)
        wd = os.getcwd()
        os.chdir('../../export/sources') 
        geojsons_folder = os.getcwd()

        #for str_m in self.string_month:
        #    doc_name = 'bike_covid_' + str_m
        global_end=''
        for end_name in self.string_month:

            name_file = 'fake_data_' + end_name
            global_end = end_name
            with open(geojsons_folder + '/' + name_file) as f:
                geojson_file = geojson.load(f)
                features = geojson_file['features']

                # for every square of the matrix
                for dic in features :
                    #the value is
                    comparison_number = dic['properties']['value']
                    poly_coordinates = dic['geometry']['coordinates'] # [[[lat1, long1], [lat2, long2]]]
                    
                    #the list of the coordinates is
                    list_poly_coordinates = poly_coordinates[0]
                    #initialising the list of the coordinates within brackets:
                    list_poly_coordinates_rw = []
                    for coord in list_poly_coordinates:
                        list_poly_coordinates_rw.append((coord[0], coord[1]))

                    # pas de 4, 10, 16
                    if comparison_number ==0:
                        polys0.append(Polygon(list_poly_coordinates_rw))
                    elif comparison_number ==1:
                        polys1.append(Polygon(list_poly_coordinates_rw))
                    elif comparison_number ==2:
                        polys2.append(Polygon(list_poly_coordinates_rw))
                    elif comparison_number ==3:
                        polys3.append(Polygon(list_poly_coordinates_rw))  
                    elif comparison_number ==5:
                        polys5.append(Polygon(list_poly_coordinates_rw))  
                    elif comparison_number ==6:
                        polys6.append(Polygon(list_poly_coordinates_rw))  
                    elif comparison_number ==7:
                        polys7.append(Polygon(list_poly_coordinates_rw))  
                    elif comparison_number ==8:
                        polys8.append(Polygon(list_poly_coordinates_rw))  
                    elif comparison_number ==9:
                        polys9.append(Polygon(list_poly_coordinates_rw)) 
                    elif comparison_number ==10:
                        polys10.append(Polygon(list_poly_coordinates_rw))  
                    elif comparison_number ==11:
                        polys11.append(Polygon(list_poly_coordinates_rw))  
                    elif comparison_number ==12:
                        polys12.append(Polygon(list_poly_coordinates_rw))  
                    elif comparison_number ==13:
                        polys13.append(Polygon(list_poly_coordinates_rw))  
                    elif comparison_number ==14:
                        polys14.append(Polygon(list_poly_coordinates_rw))  
                    elif comparison_number ==15:
                        polys15.append(Polygon(list_poly_coordinates_rw))  
                    elif comparison_number ==17:
                        polys17.append(Polygon(list_poly_coordinates_rw))  
                    elif comparison_number ==18:
                        polys18.append(Polygon(list_poly_coordinates_rw))  
                    elif comparison_number ==19:
                        polys19.append(Polygon(list_poly_coordinates_rw))  
                    elif comparison_number ==20:
                        polys20.append(Polygon(list_poly_coordinates_rw))  
                f.close()        
            
            u0 = cascaded_union(polys0)
            u1 = cascaded_union(polys1)
            u2 = cascaded_union(polys2)
            u3 = cascaded_union(polys3)
            u5 = cascaded_union(polys5)
            u6 = cascaded_union(polys6)
            u7 = cascaded_union(polys7)
            u8 = cascaded_union(polys8)
            u9 = cascaded_union(polys9)
            u10 = cascaded_union(polys10)
            u11 = cascaded_union(polys11)
            u12 = cascaded_union(polys12)
            u13 = cascaded_union(polys13)
            u14 = cascaded_union(polys14)
            u15 = cascaded_union(polys15)
            u17 = cascaded_union(polys17)
            u18 = cascaded_union(polys18)
            u19 = cascaded_union(polys19)
            u20 = cascaded_union(polys20)
            unions = [u0, u1, u2, u3, u5, u6, u7, u8, u9, u10, u11, u12, u13, u14, u15, u17, u18, u19, u20]
            
            features = []
            for i in range(19):
                geojson_out = geojson.Feature(geometry=unions[i], properties={"value": indices_rz[i]})
                features.append(geojson_out)

            feature_collection = geojson.FeatureCollection(features)
            with open('fake_data2_' + global_end, 'w') as f2:
                string_final1 = str(feature_collection)
                string_final2 = string_final1.replace("'",'"')
                f2.write(string_final2)
                #print("end fake() ")
                f2.close()
            polys0 = []
            polys1 = []
            polys2 = []
            polys3 = []
            polys5 = []
            polys6 = []
            polys7 = []
            polys8 = []
            polys9 = []
            polys10 = []
            polys11 = []
            polys12 = []
            polys13 = []
            polys14 = []
            polys15 = []
            polys17 = []
            polys18 = []
            polys19 = []
            polys20 = []