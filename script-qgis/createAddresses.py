from qgis.core import QgsVectorLayer
from qgis.core import QgsProject
from qgis.core import QgsVectorFileWriter
'''
this script load by region addresses points and water polygon 
'''
target_region = ["Sicilia"]# "VDA","Liguria","Piemonte","Sicilia","Marche","Abruzzo","Toscana","Campania","Puglia","Veneto","Lombardia","EmiliaRomagna","TAA","Sardegna","Molise","Calabria","Lazio","FVG","Basilicata","Umbria"
diseases = ["leishmania","salmonella"]# "leptospira", "epatite"
for region in target_region:
    for disease in diseases:
        addresses_file = "/C:/Develop/PhytonCode/tesi/Experiemnts/" + region + "/dataframe_sigla_water_others_" + region + "_" + disease + "output.csv"

        uri = "file://"+ addresses_file +"?encoding=%s&delimiter=%s&xField=%s&yField=%s&crs=%s" % ("UTF-8",",", "longitude", "latitude","epsg:4326")

        #Make a vector layer of addresses of case positive and negative
        sigla_addr_layer=QgsVectorLayer(uri,"siglaAddresses"+region + disease,"delimitedtext")

        #Check if layer is valid
        if not sigla_addr_layer.isValid():
            print ("Layer not loaded")

        #Add CSV data    
        QgsProject.instance().addMapLayer(sigla_addr_layer)
'''
target_water_layer = ["VDA", "Liguria", "Piemonte"]
for region in target_water_layer:
    path_to_gpkg = "C:/Users/manue/Documents/Tesi/waterlayer/" + region + "riverLakeUnion.gpkg"
    gpkg_water_layer = path_to_gpkg + "|layername=" + region + "riverLakeUnion"

    #Make a vector layer of addresses of case positive and negative
    vlayer=QgsVectorLayer(gpkg_water_layer,region+"Water","ogr")

    #Check if layer is valid
    if not vlayer.isValid():
        print ("Layer not loaded")

    #Add CSV data    
    QgsProject.instance().addMapLayer(vlayer)
'''
'''
#this lines doesn't work

#save addresses as shapefile
error = QgsVectorFileWriter.writeAsVectorFormat(sigla_addr_layer, "siglaAddresses_shapes.shp", 'utf-8', sigla_addr_layer.crs(), "ESRI Shapefile")
if error != QgsVectorFileWriter.NoError:
        # FIXME (DK): this branch isn't covered by test
        msg = ('Can not save data in temporary file.')
        raise IOError(msg)
'''