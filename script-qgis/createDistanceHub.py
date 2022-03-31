import processing
import qgis.analysis
import qgis.core
from qgis.core import QgsVectorFileWriter
from qgis.core import QgsVectorLayer
from qgis.core import QgsProject
import pandas as pd

target_region = ["Abruzzo","Toscana","Campania","Puglia","EmiliaRomagna","TAA","Sardegna","Molise","Calabria","Lazio","FVG","Basilicata","Umbria"]# "VDA","Liguria","Piemonte","Sicilia","Marche","Abruzzo","Toscana","Campania","Puglia","Veneto","Lombardia","EmiliaRomagna","TAA","Sardegna","Molise","Calabria","Lazio","FVG","Basilicata","Umbria"
lombardia_province = ["BG","BS","CO","CR","LC","LO","MI","MB","PV","SO","VA"]#"MN" # ci sono dei problemi su MN
veneto_province = ["BL","PD","RO","TV","VE","VR","VI"]
diseases = ["salmonella","epatite","leishmania","leptospira"] #"salmonella","epatite","leishmania","leptospira"
water_folder = 'C:/Users/manue/Documents/Tesi/waterlayer/'
dist_folder = 'C:/Users/manue/Documents/Tesi/distanceLayer/'
out_dist_folder = "distanceFiles/"
file_prefix = "dataframe_sigla_water_others"

for region in target_region:
    for disease in diseases:
        file_check = "C:\\Develop\\PhytonCode\\tesi\\Experiemnts\\" + region + "\\" + file_prefix + "_" + region + "_" + disease + "_output.csv"
        df1 = pd.read_csv(file_check)
        if df1.count()[0] !=0:
            out_dist_file = dist_folder + "dist"+ region +"WaterTo"+disease+"Addr" 
            addresses_file = "C:/Develop/PhytonCode/tesi/Experiemnts/"+ region + "/" + file_prefix + "_" + region + "_" + disease + "_output.csv"
            parameters =  {
                    'FIELD' : 'id', 
                    'HUBS' : 'delimitedtext://file://' + '/' + addresses_file+ '?type=csv&maxFields=10000&detectTypes=yes&xField=longitude&yField=latitude&crs=EPSG:4326&spatialIndex=no&subsetIndex=no&watchFile=no', 
                    'INPUT' : water_folder + region + 'riverLakeUnion.gpkg|layername='+ region +'riverLakeUnion', 
                    'OUTPUT' : out_dist_file + '.csv', 
                    'UNIT' : 3
                    }
            #print(parameters)
            processing.run("qgis:distancetonearesthublinetohub", parameters)
