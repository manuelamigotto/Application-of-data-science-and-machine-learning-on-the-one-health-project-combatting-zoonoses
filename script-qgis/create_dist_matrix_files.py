import processing
import qgis.analysis
import qgis.core
from qgis.core import QgsVectorFileWriter
from qgis.core import QgsVectorLayer
from qgis.core import QgsProject
import pandas as pd
import os

target_region = ["Sicilia","Marche","Abruzzo","Toscana","Campania","Puglia","TAA","Sardegna","Molise","Calabria","Lazio","FVG","Basilicata","Umbria"]# "VDA","Liguria", "Piemonte","Sicilia","Marche","Abruzzo","Toscana","Campania","Puglia","TAA","Sardegna","Molise","Calabria","Lazio","FVG","Basilicata","Umbria"
diseases = ["salmonella","epatite","leishmania","leptospira"] #"salmonella","epatite","leishmania","leptospira"
out_dist_folder = "C:/Develop/PhytonCode/tesi/Experiemnts/dist_matrix/"
geocode_file_prefix = 'dataframe_sigla_water_others' #'df_sigla_geocoded' #prefix for Piemonte, VDA, Liguria

for region in target_region:
    for disease in diseases:
        not_found_addresses_file = "C:/Develop/PhytonCode/tesi/Experiemnts/" + geocode_file_prefix + "_" + region + "_" + disease + "_dist_not_found.csv"
        found_addresses_file = "C:/Develop/PhytonCode/tesi/Experiemnts/" + geocode_file_prefix + "_" + region + "_" + disease + "_dist_found.csv"
        
        if os.path.exists(not_found_addresses_file) and os.path.exists(found_addresses_file):
            parameters =  {
                    'INPUT' : 'delimitedtext://file:///' + not_found_addresses_file + '?type=csv&maxFields=10000&detectTypes=yes&xField=longitude&yField=latitude&crs=EPSG:4326&spatialIndex=no&subsetIndex=no&watchFile=no', 
                    'INPUT_FIELD' : 'row_id',
                    'MATRIX_TYPE' : 1,
                    'NEAREST_POINTS' : 0,
                    'OUTPUT' : out_dist_folder + 'dist_matrix_'+ region +'_' + disease + '.csv', 
                    'TARGET' : 'delimitedtext://file:///' + found_addresses_file + '?type=csv&maxFields=10000&detectTypes=yes&xField=longitude&yField=latitude&crs=EPSG:4326&spatialIndex=no&subsetIndex=no&watchFile=no', 'TARGET_FIELD' : 'row_id' 
                    }
            #print(parameters)
            processing.run("qgis:distancematrix", parameters)