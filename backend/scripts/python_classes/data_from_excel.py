from csv import reader

import os
import PyPDF2
import tabula

class Data_from_excel():
    def __init__(self):
        
        # working directory (here python_classes)
        wd = os.getcwd()
        os.chdir('../tables_covid') 
        self.data_dir = os.getcwd()

        #self.station_hub_result = self.station_hub()
        self.station_hub_result = {}
        self.ltn = self.legacy_to_new_dico()

        self.places_coordinates = {'Gamle Oslo':(59.899237, 10.734767), 'Grunerlokka':(59.921875, 10.771906), 'Sagene':(59.937439, 10.760452), 
                        'St. Hanshaugen':(59.92795, 10.738958), 'Frogner':(59.917606, 10.710252), 'Ullern':(59.924469, 10.65988), 
                        'Vestre Aker':(59.9583, 10.670319), 'Nordre Aker':(59.953638, 10.756412), 'Bjerke':(59.940668, 10.808725), 
                        'Grorud':(59.961424, 10.880549), 'Stovner':(59.958595, 10.927285), 'Alna':(59.93092, 10.85403), 
                        'Ostensjo':(59.887563, 10.832748), 'Nordstrand':(59.859314, 10.801257), 'Sondre Nordstrand':(59.845535, 10.807981)}

        self.places_name = list(self.places_coordinates.keys())

        self.string_month = ['2020-04', '2020-05', '2020-06', '2020-07', '2020-08', '2020-09', '2020-10', '2020-11', '2020-12', '2021-01', 
        '2021-02', '2021-03', '2021-04']

    # Reads the pdf file "pdf_name" and generates "table_cases_oslo.csv" which contains the amount of cases per month per station
    def read_pdf_download_csv(self):
        pdf_name = "Statusrapport koronastatistikk 13. april 2021.pdf" #page 6
        print("********** read_pdf_download_csv('" + pdf_name + "') **********")
        # creating a pdf file object (on ouvre le fichier en code binaire)
        pdfFileObj = open(self.data_dir + "/" + pdf_name, 'rb') 

        # creating a pdf reader object  (Here, we create an object of PdfFileReader class of PyPDF2 module and  pass the pdf file object & get a pdf reader object)
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj) 
        nbPages = pdfReader.numPages

        tables = tabula.read_pdf(pdf_name, pages = 6)
        page_id_titre = "table_cases_oslo3.xlsx"
        
        # Conversion des tableaux en excel
        tables[0].to_excel(os.path.join(self.data_dir, page_id_titre), index=False)
        print("\nread_pdf_download(" + pdf_name + ") done")

    # returns a dictionnary with test_center_name: amount of cases since march 2020 to march 2021 included
    def test_station_amount_cases(self):
        #print("start test_station_amount_cases()")
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
                        #name_test_center="Gr??nerl??kka"
                        name_test_center="Grunerlokka"
                    if start_line5==16:
                        #name_test_center="??stensj??"
                        name_test_center="Ostensjo"
                    if start_line5==18:
                        #name_test_center="S??ndre Nordstrand"
                        name_test_center="Sondre Nordstrand"

                    list1.pop(0)      
                
                    dic_station_month_amount[name_test_center] = list1

                start_line5 +=1 
        #print("\ntest_station_amount_cases done")
        return dic_station_month_amount

    # generates the dictionnary which links the new id of a given bike station with its legacy id
    # {"new_id" : "legacy_id"}
    def new_to_legacy_dico(self):
        dico={}
        #print("start new_to_legacy_dico()")
        excel_title = '../tables_covid/legacy_new_station_id_mapping.csv'
        # open file in read mode
        with open(excel_title, 'r') as read_obj:
            # pass the file object to reader() to get the reader object
            csv_reader = reader(read_obj)
            for line in csv_reader:
                dico[line[0]]=line[1]
            del dico['new_id']
            #print("end new_to_legacy_dico()")
            return dico

    # generates the dictionnary which links the legacy id of a given bike station with its new id
    # {"legacy_id" : "new_id"}
    def legacy_to_new_dico(self):
        dico={}
        #print("start legacy_to_new_dico()")
        excel_title = '../tables_covid/legacy_new_station_id_mapping.csv'
        # open file in read mode
        with open(excel_title, 'r') as read_obj:
            # pass the file object to reader() to get the reader object
            csv_reader = reader(read_obj)
            for line in csv_reader:
                dico[line[1]]=line[0]
            del dico['legacy_id']
            #print("end legacy_to_new_dico()")
            return dico



    from csv import reader
    # for each bike station, which hub? (returns a dictionnary)
    # returns 'Name_station' : [(lat, long), distance_closest_test_center, 'Name_closest_test_center']
    # CARREFULL : currently using legacy names, can easely use the latest ones with 'legacy_new_station_id_mapping.csv' but useless
    # if you change lines 144, 146 and 147 to use new names it will screw up the generation of the maps.
    def station_hub(self):
        #print("start station_hub()")
        dic_station_hub = {}
        excel_title = '../tables_covid/legacy_coord.csv'
        # open file in read mode
        with open(excel_title, 'r') as read_obj:
            # pass the file object to reader() to get the reader object
            csv_reader = reader(read_obj)
            #print(type(csv_reader).__name__)

            # Iterate over each row in the csv using reader object
            dont_want_1st_line=0
            for station in csv_reader:
                if dont_want_1st_line>0:

                    station_lat, station_long = float(station[1]), float(station[2])
                    
                    clothest_place = self.places_name[0]
                    distance_min = ((self.places_coordinates[clothest_place][0]-station_lat)**2 
                    + (self.places_coordinates[clothest_place][1] - station_long)**2)**(1/2)
                    for place_name in self.places_name:
                        distance = ((self.places_coordinates[place_name][0]-station_lat)**2 
                    + (self.places_coordinates[place_name][1] - station_long)**2)**(1/2)
                        if distance<distance_min:
                            distance_min = distance
                            closest_place = place_name
                    #ltn = self.legacy_to_new_dico()
                    try:
                        #new_name = ltn[station[0]]
                        dic_station_hub[station[0]]= [(float(station[1]), float(station[2])), distance_min, closest_place]
                    except:
                        pass
                dont_want_1st_line+=1
                # station variable is a list that represents a row in csv
        #print("end station_hub()")
        return dic_station_hub

    # {legacy_id:coords}
    def bike_station_coord(self):
        #print("start bike_station_coord()")
        dic_bs_coord = {}
        excel_title = '../tables_covid/legacy_coord.csv'
        # open file in read mode
        with open(excel_title, 'r') as read_obj:
            # pass the file object to reader() to get the reader object
            csv_reader = reader(read_obj)
            #print(type(csv_reader).__name__)

            # Iterate over each row in the csv using reader object
            dont_want_1st_line=0
            for station in csv_reader:
                if dont_want_1st_line>0:

                    station_lat, station_long = float(station[1]), float(station[2])
                    dic_bs_coord[station[0]]= [station_lat, station_long]
                dont_want_1st_line+=1
                # station variable is a list that represents a row in csv
        #print("end bike_station_coord()")
        return dic_bs_coord

    def hub_station(self):
        dct = self.station_hub().copy()
        print(dct)
        dct = {v: k for k, v in dct.items()}
        print("\n",dct)
        return dct
    
    # returns a dictionnary with test_center_name: amount of cases since march 2020 to march 2021 included
    def dico_stats(self):
        
        dic_stats = {}
        deaths = []
        start_line24=0
        excel_title = "../tables_covid/table_cases_oslo2.csv"
        with open(excel_title, 'r') as read_obj:
            # pass the file object to reader() to get the reader object
            csv_reader = reader(read_obj)
            for line in read_obj:
                if start_line24>21 and start_line24<37:
                    list1 = list(line.split(";")) 
                    """
                    for i in range(1,4):
                        list1.pop(-1)
                    """
                    list1.pop(-1)
                    name_test_center = list1[0] 

                    if start_line24==23:
                        #name_test_center="Gr??nerl??kka"
                        name_test_center="Grunerlokka"
                    if start_line24==34:
                        #name_test_center="??stensj??"
                        name_test_center="Ostensjo"
                    if start_line24==36:
                        #name_test_center="S??ndre Nordstrand"
                        name_test_center="Sondre Nordstrand"
      
                    
                    dic_stats[name_test_center] = list1[-1]
                if start_line24==37:
                    list1 = list(line.split(";")) 
                    list1.pop(0)
                    list1.pop(-1)
                    list1.pop(-1)
                    deaths = list1

                start_line24 +=1 
        return dic_stats, deaths
    
    # creates a json file with the statistics of death and cases from/of covid-19
    def json_stats(self):
        dico_stats, deaths = self.dico_stats()
        dico_stats_keys = list(dico_stats.keys())
        json = {

	"totalCases": {
		"header": "Total Cases",
		"description": "total amount of cases since the beginning of march 2020",
		"items": [
		]
	}
        }

        for key in dico_stats_keys:
            json["totalCases"]["items"].append({"name_station": key, "amount":dico_stats[key]})

        json["totalDeaths"] = {
        		"header": "Total Deaths",
		"description": "total amount of deaths since the beginning of march 2020",
		"items": [

		]
        }

        for month in range(13):
            json["totalDeaths"]["items"].append({"month": self.string_month[month], "amount": deaths[month]})

        with open('statistics.json', 'w') as f:
            string_final1 = str(json)
            string_final2 = string_final1.replace("'",'"')
            f.write(string_final2)
        
