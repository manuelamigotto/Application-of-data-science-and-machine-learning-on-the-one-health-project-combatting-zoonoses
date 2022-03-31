import processing
import qgis.analysis
import qgis.core
from qgis.core import QgsVectorFileWriter
from qgis.core import QgsVectorLayer
from qgis.core import QgsProject
import pandas as pd

#target_region = ["Basilicata","Umbria"]# "VDA","Liguria","Piemonte","Sicilia","Marche","Abruzzo","Toscana","Campania","Puglia","Veneto","Lombardia","EmiliaRomagna","TAA","Sardegna","Molise","Calabria","Lazio","FVG","Basilicata","Umbria"
lombardia_province = ["BG","BS","CO","CR","LC","LO","MI","MB","PV","SO","VA"]#"MN" # ci sono dei problemi su MN
veneto_province = ["BL","PD","RO","TV","VE","VR","VI"]

polygon_to_lines_folder = 'C:/Users/manue/Documents/Tesi/waterlayer/PolygonToLines/'
in_folder = 'C:/Users/manue/Documents/Tesi/qgis - estrazioni/'
'''
for region in target_region:
    #for disease in diseases:
    out_path_file = polygon_to_lines_folder + region +"_polygonToLine.gpkg" 
    parameters =  {
            'INPUT' : in_folder + region + 'WaterPolygon.gpkg|layername='+ region +'WaterPolygon', 
            'OUTPUT' : out_path_file, 
            }
    #print(parameters)
    processing.run("qgis:polygonstolines", parameters)

'''
for prov in lombardia_province:
    #for disease in diseases:
    out_path_file = polygon_to_lines_folder + prov +"_polygonToLine.gpkg" 
    parameters =  {
            'INPUT' : in_folder + prov + 'Polygon.gpkg|layername='+ prov +'Polygon', 
            'OUTPUT' : out_path_file, 
            }
    #print(parameters)
    processing.run("qgis:polygonstolines", parameters)
    
for prov in veneto_province:
    #for disease in diseases:
    out_path_file = polygon_to_lines_folder + prov +"_polygonToLine.gpkg" 
    parameters =  {
            'INPUT' : in_folder + prov + 'Polygon.gpkg|layername='+ prov +'Polygon', 
            'OUTPUT' : out_path_file, 
            }
    #print(parameters)
    processing.run("qgis:polygonstolines", parameters)
    