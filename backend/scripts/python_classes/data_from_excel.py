from csv import reader

class Data_from_excel():
    def __init__(self,data_dir="C:\\Users\\virgi\\Desktop\\cours_imt\\A2\\S4 norway\\Project 6\\python_part", excel_filename='table_cases_oslo.xlsx'):
        self.data_dir = data_dir
        self.excel_filename = excel_filename
        self.station_hub_result = {}


        self.places_coordinates = {'Gamle Oslo':(59.899237, 10.734767), 'Grünerløkka':(59.921875, 10.771906), 'Sagene':(59.937439, 10.760452), 
                        'St. Hanshaugen':(59.92795, 10.738958), 'Frogner':(59.917606, 10.710252), 'Ullern':(59.924469, 10.65988), 
                        'Vestre Aker':(59.9583, 10.670319), 'Nordre Aker':(59.953638, 10.756412), 'Bjerke':(59.940668, 10.808725), 
                        'Grorud':(59.961424, 10.880549), 'Stovner':(59.958595, 10.927285), 'Alna':(59.93092, 10.85403), 
                        'Østensjø':(59.887563, 10.832748), 'Nordstrand':(59.859314, 10.801257), 'Søndre Nordstrand':(59.845535, 10.807981)}

        self.places_names = list(self.places_coordinates.keys())

    # returns a dictionnary with test_center_name: amount of cases since march 2020 to march 2021 included
    def test_station_amount_cases(self):
        print("start test_station_amount_cases()")
        dic_station_month_amount = {}
        start_line5=0
        excel_title = "../tables_covid/table_cases_oslo.csv"
        with open(excel_title, 'r') as read_obj:
            # pass the file object to reader() to get the reader object
            csv_reader = reader(read_obj)
            for line in read_obj:
                if start_line5>3 and start_line5<19:
                    #print(line)
                    list1 = list(line.split(";")) 
                    
                    for i in range(1,4):
                        list1.pop(-1)

                    name_test_center = list1[0] 
                    if start_line5==5:
                        #name_test_center="Grünerløkka"
                        name_test_center="Grunerlokka"
                    if start_line5==16:
                        #name_test_center="Østensjø"
                        name_test_center="Ostensjo"
                    if start_line5==18:
                        #name_test_center="Søndre Nordstrand"
                        name_test_center="Sondre Nordstrand"

                    list1.pop(0)      
                
                    dic_station_month_amount[name_test_center] = list1

                start_line5 +=1 
        print("\ntest_station_amount_cases done")
        return dic_station_month_amount

    # generates the dictionnary which links the old id (legacy id) of a given bike station with the new id of a given bike station
    # {"legacy_id" : "new_id"}
    def new_to_legacy_dico(self):
        dico={}
        print("start new_to_legacy_dico()")
        excel_title = '../tables_covid/legacy_new_station_id_mapping.csv'
        # open file in read mode
        with open(excel_title, 'r') as read_obj:
            # pass the file object to reader() to get the reader object
            csv_reader = reader(read_obj)
            for line in csv_reader:
                dico[line[0]]=line[1]
            del dico['new_id']
            print("end new_to_legacy_dico()")
            return dico

    #returns string
    def legacy_to_new_dico(self):
        dico={}
        print("start legacy_to_new_dico()")
        excel_title = '../tables_covid/legacy_new_station_id_mapping.csv'
        # open file in read mode
        with open(excel_title, 'r') as read_obj:
            # pass the file object to reader() to get the reader object
            csv_reader = reader(read_obj)
            for line in csv_reader:
                dico[line[1]]=line[0]
            del dico['legacy_id']
            print("end legacy_to_new_dico()")
            return dico



    from csv import reader
    # for each bike station, which hub? (returns a dictionnary)
    # returns 'Name_station' : [(lat, long), distance_clothest_test_center, 'Name_clothest_test_center']
    # CARREFULL : currently using legacy names, can easely use the latest ones with 'legacy_new_station_id_mapping.csv' but useless
    def station_hub(self):
        print("start station_hub()")
        dic_station_hub = {}
        excel_title = '../tables_covid/legacy_coord.csv'
        # open file in read mode
        with open(excel_title, 'r') as read_obj:
            # pass the file object to reader() to get the reader object
            csv_reader = reader(read_obj)
            print(type(csv_reader).__name__)

            # Iterate over each row in the csv using reader object
            dont_want_1st_line=0
            for station in csv_reader:
                if dont_want_1st_line>0:

                    station_lat, station_long = float(station[1]), float(station[2])
                    
                    clothest_place = self.places_names[0]
                    distance_min = ((self.places_coordinates[clothest_place][0]-station_lat)**2 
                    + (self.places_coordinates[clothest_place][1] - station_long)**2)**(1/2)
                    for place_name in self.places_names:
                        distance = ((self.places_coordinates[place_name][0]-station_lat)**2 
                    + (self.places_coordinates[place_name][1] - station_long)**2)**(1/2)
                        if distance<distance_min:
                            distance_min = distance
                            clothest_place = place_name
                    
                    dic_station_hub[station[0]]= [(float(station[1]), float(station[2])), distance_min, clothest_place]
                dont_want_1st_line+=1
                # station variable is a list that represents a row in csv
        print("end station_hub()")
        return dic_station_hub
