import generate_geojson
import data_from_excel
import tools

import requests


if __name__=="__main__":
   
    gg_object = generate_geojson.Generate_geojson()
    #gg_object.for_each_month_map()
    m=0
    da = ["2020/01", "2020/02", "2020/03", "2020/04", "2020/05", "2020/06", "2020/07","2020/08","2020/09","2020/10","2020/11","2020/12","2021/01", "2021/02", "2021/03", "2021/04"]
    for d in da:
        r = requests.get('https://data.urbansharing.com/oslobysykkel.no/trips/v1/'+ d + '.json')
        result = r.json() 
        gg_object.create_bike_stations(m, result)
        m +=1
    #ROAD MAP:
    # Parse Oslo Bysikkel site to get the bikes-related data
    # Generate a geojson file filled with a matrix

    # read the pdf
    # extract an xlsx file from the pdf

    ### with the csv containing stations id + pos:
    # link each bike station with a test center from the first xlsx file
    
    # make the matrix bigger, then :
    # for this matrix, generate a value for each square in order for each square to be linked to a station (test center?)
    # add a property that is a value depending on:
    # compare cases from "table_cases_oslo.xlsx" and osloBysikkel for related/notrelated/other thing?