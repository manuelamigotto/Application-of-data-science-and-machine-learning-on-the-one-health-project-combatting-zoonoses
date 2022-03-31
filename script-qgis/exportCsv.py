from qgis.core import QgsVectorLayer
from qgis.core import QgsProject
from qgis.core import QgsVectorFileWriter
'''
this script load by region addresses points and water polygon 
'''
target_region = ["Valle d'Aosta"] #, "Liguria", "Piemonte"
target_region_dict = {"Valle d'Aosta": "VDA", "Liguria":"Liguria", "Piemonte":"Piemonte"}
diseases = ["epatite","leishmania","leptospira","salmonella"]
dist_folder = '/C:/Users/manue/Documents/Tesi/distanceLayer/'

for region in target_region:
    for disease in diseases:
        gpkg_name = "dist"+ target_region_dict[region] +"WaterTo"+disease+"Addr"
        addresses_file = dist_folder + gpkg_name + '.gpkg'

        uri = "file://"+ addresses_file +"?encoding=%s&delimiter=%s&xField=%s&yField=%s&crs=%s" % ("UTF-8",",", "longitude", "latitude","epsg:4326")

        layer = QgsVectorLayer(addresses_file, gpkg_name, "ogr")
        QgsVectorFileWriter.writeAsVectorFormat(layer,dist_folder + gpkg_name +".csv","utf-8",driverName = "CSV" , layerOptions = ['GEOMETRY=AS_XYZ'])