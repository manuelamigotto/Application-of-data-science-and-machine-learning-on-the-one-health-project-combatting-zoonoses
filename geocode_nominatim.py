import pandas as pd
from geopy.geocoders import Nominatim
from geopy.exc import GeopyError
from file_sources import geocode_data_region
from geocode_utils import generate_error_file_name, set_notFound, open_addresses_dict_if_exist

geolocator = Nominatim(user_agent="geocodeApp")

#parmeters
#df_to_geocode: list of rows of dataframe for iterate
#df: dataframe we want to modify
def callNominatimGeocode(df, errFile, file_name):
    for row_id,row in df.iterrows():
        try:
            print(row["geocode_address"])
            location = geolocator.geocode(row["geocode_address"])
        except GeopyError as e:
            errFile.write("Error: geocode failed on input " + row["geocode_address"] + " with message " + str(e) + " for filename " + file_name)
            continue
        finally:
            if location:
                df.iloc[row_id,df.columns.get_loc('geocode_address')]= row["geocode_address"]
                df.iloc[row_id,df.columns.get_loc('latitude')] =location.point.latitude
                df.iloc[row_id,df.columns.get_loc('longitude')] =location.point.longitude
            else:
                df.iloc[row_id,df.columns.get_loc('latitude')]="NotFound" 
                df.iloc[row_id,df.columns.get_loc('longitude')]="NotFound"
    return df

#return dictionary of max and min latitude and longitude contained in parameter region
def get_geo_data_by_region(region):
    gdr = pd.read_csv(geocode_data_region,sep=';', encoding = 'utf8')
    geo_region = gdr.loc[gdr.regione == region]
    geo_data = {}
    if len(geo_region) >0:
        geo_data['lat_nord'] = float(geo_region.iloc[0]['lat_nord'])
        geo_data['lat_sud'] = float(geo_region.iloc[0]['lat_sud'])
        geo_data['long_ovest'] = float(geo_region.iloc[0]['long_ovest'])
        geo_data['long_est'] = float(geo_region.iloc[0]['long_est'])
    else:
        print("ATTENTION!Region " + region + " not found in " + geocode_data_region + "\n")
    return geo_data

#return dataset of notFound addresses
def get_notFound(in_file):#(in_file, out_file):
    df = pd.read_csv(in_file)
    not_foud_addresses = df.loc[df.latitude=='NotFound']
    
    if len(not_foud_addresses) >0:
        #not_foud_addresses.to_csv(out_file, index=False)
        return True
    else:
        #print("There are NO notFound addresses in " + in_file + "\n")
        return False
    
def save_notFound(in_file, out_file):
    df = pd.read_csv(in_file)
    not_foud_addresses = df.loc[df.latitude=='NotFound']
    
    if len(not_foud_addresses) >0:
        not_foud_addresses.to_csv(out_file, index=False)
        print("File" + out_file +" created with " + str(len(not_foud_addresses)) + "rows")
        return True
    else:
        #print("There are NO notFound addresses in " + in_file + "\n")
        return False
    

def massiveNominatimGeocode(region, file_input, file_output, addresses_dict_json, only_notFound=0):
    
    file_errors_name = generate_error_file_name("ErrorGeocodeNominatim", "geocodeNominatimErrors")
    errorsFile = open(file_errors_name, "a",encoding="utf-8")

    #file_name_prefix = "splitFiles/df_sigla_country" #"macelli_Italia_geocode"
    
    geo_data = get_geo_data_by_region(region)

    print("\nReading file " + file_input + " for NOMINATIM Geocode")
    df = pd.read_csv(file_input) #, sep=';', encoding = 'utf8') #parte commentata utile per la geocodifica dei macelli
    if 'latitude' not in df.columns:
        df['latitude']=""
    if 'longitude' not in df.columns:
        df['longitude']=""
    
    count_found_geo = 0
    count_not_found_geo = 0 
    already_geocoded_count = 0
    
    latitude_loc = df.columns.get_loc('latitude')
    longitude_loc = df.columns.get_loc('longitude')
    
    #open json and load addresses dictionary. This step is to avoid geocodings already done
    addr_dict = open_addresses_dict_if_exist(addresses_dict_json)    
                
    try:
        for row_id,row in df.iterrows():
            if only_notFound:
                if row['latitude']!='NotFound':
                    continue
            isRigth = True
                       
            if row["geocode_address"] not in addr_dict:
                try:
                    location = geolocator.geocode(row["geocode_address"])
                except GeopyError as e:
                    errorsFile.write("Error: geocode failed on input " + row["geocode_address"] + " with message " + str(e) + " for filename " + file_input)
                    continue
                finally:
                    if location:
                        #check wrong geocode 
                        if float(location.point.latitude)>geo_data['lat_nord'] or float(location.point.latitude)<geo_data['lat_sud']:
                            set_notFound(df, row_id)
                            isRigth = False
                        else:
                            if float(location.point.longitude)>geo_data['long_est'] or float(location.point.longitude)<geo_data['long_ovest']:
                                set_notFound(df, row_id)
                                isRigth = False
                        if isRigth:
                            df.iloc[row_id,latitude_loc] =location.point.latitude
                            df.iloc[row_id,longitude_loc] =location.point.longitude
                            count_found_geo +=1
                    else:
                        set_notFound(df, row_id)
                        count_not_found_geo +=1
            else:
                df.iloc[row_id,latitude_loc] = addr_dict[row["geocode_address"]].latitude
                df.iloc[row_id,longitude_loc] = addr_dict[row["geocode_address"]].longitude
                already_geocoded_count +=1          
    except Exception as e:
        errorsFile.write("Error : " + str(e) + " during reading of file : " + file_input )
    finally:
        print("\n----> NOMINATIM Geocode (file of "+ str(df.count()[0]) +" rows):")
        print("geocoded rows: " + str(count_found_geo))
        print("NOT geocoded rows: " + str(count_not_found_geo))
        print("Already geocoded rows (from json dictionary): " + str(already_geocoded_count))
        
        df.to_csv(file_output, index=False)
    errorsFile.close()   
