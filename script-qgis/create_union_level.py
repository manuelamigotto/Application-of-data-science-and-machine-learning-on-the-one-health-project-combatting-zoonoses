import processing
import qgis.analysis
import qgis.core
from qgis.core import QgsVectorFileWriter
from qgis.core import QgsVectorLayer
from qgis.core import QgsProject
import pandas as pd

target_region = ["Basilicata","Umbria"]# "VDA","Liguria","Piemonte","Sicilia","Marche","Abruzzo","Toscana","Campania","Puglia","Veneto","Lombardia","EmiliaRomagna","TAA","Sardegna","Molise","Calabria","Lazio","FVG","Basilicata","Umbria"
lombardia_province = ["BG","BS","CO","CR","LC","LO","MI","MB","PV","SO","VA"]#"MN" # ci sono dei problemi su MN
veneto_province = ["BL","PD","RO","TV","VE","VR","VI"]
water_folder = 'C:/Users/manue/Documents/Tesi/waterlayer/'
polygon_folder_name = 'PolygonToLines/'
out_folder = 'C:/Users/manue/Documents/Tesi/qgis - estrazioni/'
'''
for region in target_region:
    #for disease in diseases:
    out_path_file = water_folder + region +"_polygonToLine.gpkg" 
    parameters =  {
            'INPUT' : water_folder + polygon_folder_name + region + '_polygonToLine.gpkg', 
            'OUTPUT' : 'ogr:dbname=\'' + water_folder + region + 'riverLakeUnion.gpkg\' table=\"' + region + 'riverLakeUnion\" (geom)', 
            'OVERLAY' : out_folder + region + 'WaterLines.gpkg|layername=' + region + 'WaterLines', 
            'OVERLAY_FIELDS_PREFIX' : ''  
            }
    #print(parameters)
    processing.run("qgis:union", parameters)
'''
for prov in lombardia_province:
    #for disease in diseases:
    out_path_file = water_folder + prov +"_polygonToLine.gpkg" 
    parameters =  {
            'INPUT' : water_folder + polygon_folder_name + prov + '_polygonToLine.gpkg', 
            'OUTPUT' : 'ogr:dbname=\'' + water_folder + prov + 'riverLakeUnion.gpkg\' table=\"' + prov + 'riverLakeUnion\" (geom)', 
            'OVERLAY' : out_folder + prov + 'Lines.gpkg|layername=' + prov + 'Lines', 
            'OVERLAY_FIELDS_PREFIX' : ''  
            }
    #print(parameters)
    processing.run("qgis:union", parameters)

for prov in veneto_province:
    #for disease in diseases:
    out_path_file = water_folder + prov +"_polygonToLine.gpkg" 
    parameters =  {
            'INPUT' : water_folder + polygon_folder_name + prov + '_polygonToLine.gpkg', 
            'OUTPUT' : 'ogr:dbname=\'' + water_folder + prov + 'riverLakeUnion.gpkg\' table=\"' + prov + 'riverLakeUnion\" (geom)', 
            'OVERLAY' : out_folder + prov + 'Lines.gpkg|layername=' + prov + 'Lines', 
            'OVERLAY_FIELDS_PREFIX' : ''  
            }
    #print(parameters)
    processing.run("qgis:union", parameters)
