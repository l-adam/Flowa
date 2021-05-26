import generate_geojson
import data_from_excel

import requests
import gmplot
import random
import os

import datetime
from datetime import time
import requests

"""
import tarfile
import lzma
"""
import zipfile
import bz2

class Tools():
    def __init__(self):
        self.newId_usesMonth = {}


    def get_date_object(self, str_date):
        list_date = str_date.split("+")
        date_time_obj = datetime.datetime.strptime(list_date[0], '%Y-%m-%d %H:%M:%S.%f')
        #date_time_obj.date()
        #date_time_obj.time()
        return(date_time_obj)


    # Returns True if obj_date is in [5AM : 9AM]
    #   False otherwise
    def morning(self, obj_date):
        #str_morning_start = "04:22:18"
        #morning_start = datetime.datetime(year = 1, month = 1, day = 1, hour = 6,minute = 0,second = 1)
        #morning_end = datetime.datetime(year = 1, month = 1, day = 1, hour = 9, minute = 0, second = 0)
        morning_start = datetime.time(5,3)
        morning_end = datetime.time(9)
        if obj_date.time()<morning_end and obj_date.time() > morning_start:
            return True
        return False

    def afternoon(self, obj_date):
        #str_morning_start = "04:22:18"
        #morning_start = datetime.datetime(year = 1, month = 1, day = 1, hour = 6,minute = 0,second = 1)
        #morning_end = datetime.datetime(year = 1, month = 1, day = 1, hour = 9, minute = 0, second = 0)
        afternoon_start = datetime.time(16,3)
        afternoon_end = datetime.time(20,15)
        if obj_date.time()<afternoon_end and obj_date.time() > afternoon_start:
            return True
        return False


    #bg, bd, hg,  1,2, 3, 6
    def get_center_rectangle(self, lat_bg, long_bg, lat_bd, long_hg):
        result_lat, result_long = (lat_bg + lat_bd)/2, (long_bg + long_hg)/2
        return result_lat, result_long



    def distance(self, latA, longA, latB, longB):
        return float((latB-latA)**2 + (longB-longA)**2)**(1/2)


    # returns dictionnary with bike_station_new_id (string): amount of uses this month (int) (the month of the json_file)
    # new or legacy? I guess new
    def fill_departures_list2(self, json_file):
        # global_station_hub = dico pour chaque id de station de vélo:[(lat, long), distance_closest_test_center, 'Name_closest_test_center']
        
        amount_travel_morning = 0

        amount_travel_afternoon =0
        dic_station_number = {}
        #result = fichier json
        #pour chaque station
        for i in range(len(json_file)):
            start_station_id = json_file[i]["start_station_id"]
            end_station_id = json_file[i]["end_station_id"]
            
            #si c'est la première fois qu'on voit cette station on l'instancie à 1 sinon on lui rajoute 1.
            if start_station_id not in dic_station_number:
                dic_station_number[start_station_id] = 0
            if end_station_id not in dic_station_number:
                dic_station_number[end_station_id] = 0

            
            # infos relatives à la station i = dic_travel
            dic_travel=json_file[i]
            # heures de départ et d'arrivée
            started_str = dic_travel['started_at']
            ended_str = dic_travel['ended_at']

            #print(i, "started_str : " + started_str)

            #nécessaire car des fois la date n'a pas toujours le même format, donc là ça enlève quelques cas mais pas beaucoup (à vérifier)
            if len(started_str) >27 and len(ended_str)> 27:
                started_obj = self.get_date_object(started_str)
                ended_obj = self.get_date_object(ended_str)
                #si le vélo est bien partit le matin on ajoute sa latitude, longitude du départ dans la 1ère liste et même chose pour la 2ème liste
                if self.morning(started_obj)==True:
                    #print(started_obj, " : True")
                    amount_travel_morning+=1
                    dic_station_number[end_station_id] +=1

                else:
                    if self.afternoon(started_obj)==True:
                        amount_travel_afternoon +=1
                        dic_station_number[start_station_id] +=1
        self.newId_usesMonth = dic_station_number
        return dic_station_number


    def fill_departures_list3(self, json_file):
        dfeo = data_from_excel.Data_from_excel()
        new_to_test_center = dfeo.station_hub()
        
        amount_travel = 0

        test_center_amount = {}
        #result = fichier json
        #pour chaque station
        for i in range(len(json_file)):
            start_station_id = json_file[i]["start_station_id"]
            end_station_id = json_file[i]["end_station_id"]
            
            #si c'est la première fois qu'on voit cette station on l'instancie à 1 sinon on lui rajoute 1.
            if new_to_test_center[start_station_id] not in test_center_amount:
                test_center_amount[new_to_test_center[start_station_id]] = 0
            if new_to_test_center[end_station_id] not in test_center_amount:
                test_center_amount[new_to_test_center[end_station_id]] = 0

            
            # infos relatives à la station i = dic_travel
            dic_travel=json_file[i]
            amount_travel+=1
            test_center_amount[new_to_test_center[start_station_id]] +=1
            test_center_amount[new_to_test_center[end_station_id]] +=1

        self.newId_usesMonth = test_center_amount
        return test_center_amount

    
    def compress(self):
        #python_classes
        #curr_dir = os.getcwd()
        os.chdir("../") 
        curr_dir = os.path.normpath(os.getcwd() + os.sep + os.pardir)#backend
        curr_dir = os.path.normpath(curr_dir + "/export/sources/")
        list_files = os.listdir(curr_dir)
        list_files = list_files[0:13]

        print(curr_dir)
        geojson_zip = zipfile.ZipFile(curr_dir + 'geojson_archived.zip', 'w')


        for folder, subfolders, files in os.walk(curr_dir):
 
            for file in files:
                #if file.startswith('bike'):
                geojson_zip.write(os.path.join(folder, file), os.path.relpath(os.path.join(folder,file), curr_dir), 
                compress_type = zipfile.ZIP_BZIP2, compresslevel=9)
        
        geojson_zip.close()

        return(curr_dir, list_files)
