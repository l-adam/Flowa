import generate_geojson
import data_from_excel
import tools


if __name__=="__main__":
   
    gg_object = generate_geojson.Generate_geojson()
    gg_object.for_each_month_map()

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