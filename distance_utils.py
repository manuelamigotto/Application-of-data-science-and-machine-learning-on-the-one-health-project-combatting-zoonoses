import pandas as pd
import jsonpickle
from shapely import wkb
    
def get_not_found_distances(distance_to_water_file, disease_addresses_file, no_dist_file_output, dist_file_output):
    #read file with distances from water sources
    df_water = pd.read_csv(distance_to_water_file, encoding = "ISO-8859-1")
    #read file with all record of specific region and disease
    df_origin = pd.read_csv(disease_addresses_file)
    #get hubName(correspond to row_id in disease file) with distances from water sources
    row_id_water = df_water["HubName"].drop_duplicates()
    #get rows without distances from water sources
    not_found_distances = df_origin[~df_origin['id'].isin(row_id_water)]
    found_distances = df_origin[df_origin['id'].isin(row_id_water)]
    
    #generate name for output file and save it
    not_found_distances.to_csv(no_dist_file_output, index=False)
    found_distances.to_csv(dist_file_output, index=False)
    
    #calculate percentage of rows with distances respect to rows without distances
    perc = len(row_id_water)/len(df_origin)
    
    print("---" + disease_addresses_file + " statistics---\nNum of records with address without water:" + str(len(not_found_distances)) + 
            "\nWater distance file record:"+ str(len(df_water))+ "\nNum row_id with no distances:" + str(len(row_id_water)) + 
            "\nTot rows of file with geocode:" + str(len(df_origin)) + "\n perc: " + str(perc) + "\n")
    
    return len(not_found_distances)

class DictDistFeatures:    
    def __init__(self, dict):        
        self.features_dict = dict  
           
class DictGeoInfo:    
    def __init__(self, dict):        
        self.geo_dict = dict                

# class of geographic information
class GeoInfo:
    def __init__(self, lat, long, dist_dict):
        self.latitude = lat
        self.longitude = long
        self.distances_dict = dist_dict
    def show(self):
        print("Latitude: ", self.latitude)
        print("Longitude: ", self.longitude)
        print("Distance List: ", self.distances_dict)
    #def to_json(obj):
        #return json.dumps(obj, default=lambda obj: obj.__dict__) 

# class of water source
class WaterSourceDistance:
    def __init__(self, o_id, n, o_id_2, n2, dist):
        self.osm_id = o_id
        self.name = n
        self.osm_id_2 = o_id_2
        self.name2 = n2
        self.distance_value = dist
    def __eq__(self, other):
        if (isinstance(other, WaterSourceDistance)):
            return self.distance_value == other.distance_value
    def __lt__(self, other):
        return (self.distance_value < other.distance_value)
    def __cmp__(self, other):
        return cmp(self.distance_value, other.distance_value)
    def show(self):
        print("Osm_id: ", self.osm_id)
        print("Name: ", self.name)
        print("Osm_is_2: ", self.osm_id_2)
        print("Name2: ", self.name2)
        print("Distance in km: ", self.distance_value)

class DistanceFeature:
    def __init__(self, o_id, n, o_id_2, n2, latitude, longitude, dist, count):
        self.osm_id = o_id
        self.name = n
        self.osm_id_2 = o_id_2
        self.name2 = n2
        self.latitude = latitude
        self.longitude = longitude
        self.min_dist = dist
        self.water_count = count
    def __eq__(self, other):
        if (isinstance(other, DistanceFeature)):
            return self.min_dist == other.min_dist
    def __lt__(self, other):
        return (self.min_dist < other.min_dist)
    def __cmp__(self, other):
        return cmp(self.min_dist, other.min_dist)
    def show(self):
        print("Osm_id: ", self.osm_id)
        print("Name: ", self.name)
        print("Osm_is_2: ", self.osm_id_2)
        print("Latitude: ", self.latitude)
        print("Longitude: ", self.longitude)
        print("Name2: ", self.name2)
        print("Minimum distance to water source in meters: ", self.min_dist)
        print("Number of water source in bounding box: ", self.water_count)

def save_json_distances(json_output_filename, dist_folder, target_region, diseases):    
    import os.path
    
    addr_dict = {}
    
    file_exists = os.path.exists(json_output_filename)
    if file_exists:
        with open(json_output_filename, "r") as json_file:
            geo_dict_obj = jsonpickle.decode(json_file.read())            
            addr_dict = geo_dict_obj.geo_dict                             
    
    for region in target_region:
        for disease in diseases:
            distance_to_water_file = dist_folder + "dist" + region + "WaterTo" + disease + "Addr_complete"                     
            df_water = pd.read_csv(distance_to_water_file + ".csv", encoding = "ISO-8859-1")
            addresses_file = "df_sigla_geocoded" + "_" + region + "_" + disease + "final"
            df_addresses = pd.read_csv(addresses_file + ".csv")
             
            df_addresses['geocode_address'] = df_addresses['INDIRIZZO PRELIEVO'].fillna('-')
            df_addresses['CAP PRELIEVO'] = df_addresses['CAP PRELIEVO'].astype(str).str[:5]
            df_addresses['geocode_address'] = df_addresses['geocode_address'].astype(str) + ',' + \
            df_addresses['CAP PRELIEVO'].astype(str) + ',' + df_addresses['COMUNE PRELIEVO'] + ',' + df_addresses['PROVINCIA PRELIEVO'] + ',' + 'Italia'
            df_addresses['geocode_address'] = df_addresses['geocode_address'].map(lambda x: x.lstrip(',-'))  
            
            for index, row in df_water.iterrows():
                address_row = df_addresses.loc[df_addresses.row_id == row['HubName']]
                address = address_row['geocode_address'].values[0]
                latitude = address_row['latitude'].values[0]
                longitude = address_row['longitude'].values[0]
                water_obj = WaterSourceDistance(row['osm_id'], row['name'], row['osm_id_2'], row['name_2'], row['HubDist'])
                waterKey = str(water_obj.osm_id)+str(water_obj.name)+str(water_obj.osm_id_2)+str(water_obj.name2)
                if address in addr_dict:
                    if waterKey not in addr_dict[address].distances_dict:
                        addr_dict[address].distances_dict[waterKey] = water_obj
                else:                    
                    water_list = {waterKey : water_obj}    
                    addr_dict[address] = GeoInfo(latitude, longitude, water_list)
    out_dict = DictGeoInfo(addr_dict)
    with open(json_output_filename, 'w') as file:
        out_dict_jason = jsonpickle.encode(out_dict)
        file.write(out_dict_jason)

def create_feature_dict(addr_dict, df_closest):                          
            
    for index, row in df_closest.iterrows():
        address = row['geocode_address']
        latitude = wkb.loads(row['point']).y
        longitude = wkb.loads(row['point']).x
        min_dist = row['meters_dist']
        count_water_source = row['counts']
        osm_id = row['osm_id']
        osm_id2 = row['osm_id_2']
        name = row['name']
        name2 = row['name_2']
        if address not in addr_dict:
            addr_dict[address] = DistanceFeature(osm_id, name, osm_id2, name2, latitude, longitude, min_dist, count_water_source)
    
    return addr_dict
    