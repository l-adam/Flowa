import tools
import data_from_excel


import requests
import gmplot
import random
import os

import datetime
from datetime import time

#use

class Generate_geojson():
    def __init__(self, title = None):

        self.places_coordinates = {'Gamle Oslo':(59.899237, 10.734767), 'Grunerlokka':(59.921875, 10.771906), 'Sagene':(59.937439, 10.760452), 
                        'St. Hanshaugen':(59.92795, 10.738958), 'Frogner':(59.917606, 10.710252), 'Ullern':(59.924469, 10.65988), 
                        'Vestre Aker':(59.9583, 10.670319), 'Nordre Aker':(59.953638, 10.756412), 'Bjerke':(59.940668, 10.808725), 
                        'Grorud':(59.961424, 10.880549), 'Stovner':(59.958595, 10.927285), 'Alna':(59.93092, 10.85403), 
                        'Ostensjo':(59.887563, 10.832748), 'Nordstrand':(59.859314, 10.801257), 'Sondre Nordstrand':(59.845535, 10.807981)}
        self.places_name = list(self.places_coordinates.keys())
        self.ids = {'Gamle Oslo':'gamle_oslo', 'Grunerlokka':'grunerlokka', 'Sagene':'sagene', 
                        'St. Hanshaugen':'hanshaugen', 'Frogner':'frogner', 'Ullern':'ullern' ,
                        'Vestre Aker':'vestre_aker', 'Nordre Aker':'nordre_aker', 'Bjerke':'bjerke', 
                        'Grorud':'grorud', 'Stovner':'stovner', 'Alna':'alna', 
                        'Ostensjo':'ostensjo', 'Nordstrand':'nordstrand', 'Sondre Nordstrand':'sondre_nordstrand'}

        # working directory
        self.data_dir = "C:\\Users\\virgi\\Desktop\\cours_imt\\A2\\S4 norway\\Project 6\\python_part"

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
            r = requests.get('https://data.urbansharing.com/oslobysykkel.no/trips/v1/2020/' + str(str_i_month) + '.json')        
            result = r.json()

            amount_travels_dico = self.init_tools.fill_departures_list2(result)
            #print(amount_travels_dico)
            #print(amount_travels_bfore)
            self.create_matrix_square_station(index_month_relevant, result, map_number, amount_travels_bfore, amount_travels_dico)
            print("compt ",self.compt_it, " : ", self.compt)
            self.compt = [0,0,0,0,0]
            self.compt_it +=1
            amount_travels_bfore = self.init_tools.fill_departures_list2(result)
            index_month_relevant += 1
            i_month +=1
            i_month = i_month%12
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
        c_o = [10.665, 59.97] # = [longitude, latitude]
        #print("start create_matrix_square_station() ")
        geojson = {
                    "type" : "FeatureCollection",
                    "features" : [
                        
                    ]
        }
        # c_o[0] + 10**(-4)*4.07696*lon_indice
        # c_o[1] - 10**(-4)*2.04425*lat_indice
        increment_long = 10**(-4)*4.07696*2
        increment_lat = 10**(-4)*2.04425*2
        for lat_indice in range(220):
            for lon_indice in range(200):
                # here it can be optimised:
                gcbs_stat = self.get_closest_bike_station(self.init_tools.get_center_rectangle(c_o[1] - increment_lat*lat_indice, c_o[0] + increment_long*lon_indice, c_o[1] - increment_lat*(lat_indice+1), c_o[0] + increment_long*(lon_indice + 1))[0],self.init_tools.get_center_rectangle(c_o[1] - increment_lat*lat_indice, c_o[0] + increment_long*lon_indice, c_o[1] - increment_lat*(lat_indice+1), c_o[0] + increment_long*(lon_indice + 1))[1])[0]
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
                                    "probability" : self.compare_then_proba(month_num, self.legacy_to_new(gcbs_stat), json_file, amount_travels_bfore, amount_travels_dico)#month num, bike station id  compare_then_proba(month_num, bike_station_id, json_file):
                                }

                            })

        with open('try_map_number' + str(map_number) +'.geojson', 'w') as f:
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
        
        with open('test_stations'+ str(month)+ '.geojson', 'w') as f:
            string_final1 = str(geojson)
            string_final2 = string_final1.replace("'",'"')
            f.write(string_final2)
            print("end create_test_stations() ")
        
    # generates a geojson file with the coordinates of all the bike stations {legacy_id : [lat, long]}
    def create_bike_stations(self):
        #print("start create_bike_stations() ")
        dico_from_excel = self.init_dfe.bike_station_coord()
        geojson = {
                    "type" : "FeatureCollection",
                    "features" : [
                        
                    ]
        }
        for name_station in list(dico_from_excel.keys()):
            geojson["features"].append({
                                        "type" : "Feature",
                            "geometry" : {
                                "type" : "Point",
                                "coordinates" : [dico_from_excel[name_station][1], dico_from_excel[name_station][0]]  
                                
                            },
                            "properties" : {
                                "Name_place": name_station,
                            }

                        })

        with open('bike_stations.geojson', 'w') as f:
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
            
            if comparison_bike > 0 and comparison_test>0:
                #print("1")
                self.compt[0]+=1
                return 1
            elif comparison_bike < 0 and comparison_test<0:
                #print("-1)")
                self.compt[1]+=1
                return -1

            elif comparison_bike > 0 and comparison_test<0:
                #print("2")
                self.compt[2]+=1
                return 2
            elif comparison_bike < 0 and comparison_test>0:
                #print("-2")
                self.compt[3]+=1
                return -2
            else:
                #print(comparison_bike, " ", comparison_test)
                self.compt[4]+=1
                return 0
            
            """
            if comparison_bike > 0 and comparison_test>0:
                print("5")
                return 5
            elif comparison_bike < 0 and comparison_test<0:
                print("-5")
                return -1

            elif comparison_bike > 0 and comparison_test<0:
                print("1")
                return 1
            elif comparison_bike < 0 and comparison_test>0:
                print("9")
                return 9
            else:
                print(comparison_bike, " ", comparison_test)
                return 0
            """
        except:
            #print("0")
            self.compt[4]+=1
            return 0
            
        #print("end compare_then_proba()")
        return 0

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