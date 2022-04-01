import pandas as pd
from geopy.geocoders import GoogleV3
from geocode_nominatim import get_geo_data_by_region
from geocode_utils import generate_error_file_name, set_lat_long, set_notFound, open_addresses_dict_if_exist
from google_api_params import AUTH_KEY_SC
from geopy.exc import GeopyError

#---------BEGIN 1ST STEP: create files with geocode obtained by Google-------------
def massiveGoogleGeocode(region, file_input, file_output, addresses_dict_json, all_record=0):

    geolocator = GoogleV3(api_key=AUTH_KEY_SC)

    file_errors_name = generate_error_file_name("ErrorGeocodeGoogle", "geocodeErrors")
    errorsFile = open(file_errors_name, "w", encoding="utf-8")
    tot_googleGeocode=0
    #file_name_prefix = "splitFiles/df_sigla_country" #"macelli_Italia_geocode"

    geo_data = get_geo_data_by_region(region)

    #dictionary for already geocoded addresses (geocoding during this step) 
    geocode_dict={}
    
    tot_geocode = 0
    count_call_api_google = 0
    n_geocode = 0
    count = 0
    geocode_from_json = 0 

    print("Reading file " + file_input + " for Google geocode")
    # read files of exams
    df = pd.read_csv(file_input)
    
    #open json and load addresses dictionary. This step is to avoid geocodings already done
    addr_dict = open_addresses_dict_if_exist(addresses_dict_json)  
     
    try:
        for row_id,row in df.iterrows():
            isRigth = True 
            if row["geocode_address"] not in addr_dict:
                if row['latitude']=='NotFound' or all_record:
                    count +=1
                    try:
                        if row["geocode_address"] not in geocode_dict:
                            location = geolocator.geocode(row["geocode_address"])
                            count_call_api_google +=1
                        #print(str(tuple(location.point)))
                    except GeopyError as e:
                        print(row["geocode_address"])
                        errorsFile.write("Error: geocode failed on input row " + str(id) + " for address " + row["geocode_address"] + " with message " + str(e) + " for filename " + file_input)
                        continue
                    finally:
                        if row["geocode_address"] in geocode_dict:
                            set_lat_long(df, row_id, geocode_dict[row["geocode_address"]][0], geocode_dict[row["geocode_address"]][1])
                            n_geocode += 1    
                        else:
                            if location:
                                if float(location.point.latitude)>geo_data['lat_nord'] or float(location.point.latitude)<geo_data['lat_sud']:
                                    set_notFound(df, row_id)
                                    isRigth = False
                                else:
                                    if float(location.point.longitude)>geo_data['long_est'] or float(location.point.longitude)<geo_data['long_ovest']:
                                        set_notFound(df, row_id)
                                        isRigth = False
                                if isRigth:
                                    set_lat_long(df, row_id, location.point.latitude, location.point.longitude)
                                    n_geocode += 1
                                    geocode_dict[row["geocode_address"]] = [location.point.latitude,location.point.longitude]    
                            else:
                                set_notFound(df, row_id)
            else:
                set_lat_long(df, row_id, addr_dict[row["geocode_address"]].latitude, addr_dict[row["geocode_address"]].longitude)
                n_geocode +=1
                geocode_from_json += 1
        print("Effettuate " + str(count_call_api_google) + " geocodifiche con Google su un totale di " + str(n_geocode))
        tot_googleGeocode +=count_call_api_google
        tot_geocode += n_geocode
    except Exception as e :
        print('Eccezione: ' + str(e))
        errorsFile.close()
    finally:
        df.to_csv(file_output, index=False)
        print("Totale geocodifiche fatte con Google: " + str(tot_googleGeocode))
        print("Totale indirizzi con geocodifica: " + str(tot_geocode))
        print("Geocode from addresses dictionary saved in json: " + str(geocode_from_json))
        print("Tot righe file: " + str(len(df)) + "\n")
    errorsFile.close()

    #Array for define end geocoding: if there are some addresses not geocoded is necessary to retrive geocode using other assumption
    return [tot_geocode, count] 
#---------BEGIN 1ST STEP-------------


#---------BEGIN 2ND STEP: Create unique file with addresses not found for manual search-------------

def merge_not_found_addresses():
    #start reading from index file 
    start_idx=1
    #end reading to index file 'end_idx'
    end_idx = 219

    file_errors_name = generate_error_file_name()
    errorsFile = open(file_errors_name, "w", encoding="utf-8")
    file_addr_not_found_name = "NotFoundAddresses.txt"
    notFoundAddrFile = open(file_addr_not_found_name, "w", encoding="utf-8")
    notFoundAddr=0
    file_name_prefix = "splitFiles/df_sigla_country" #"macelli_Italia_geocode"

    notFoundAddrFile.write( "id,filename,geocode_address\n")
    for i in range(start_idx, end_idx+1):
        file_name = file_name_prefix + str(i) + "_latlong_complete.csv"
        print("Reading file" + file_name)
        # read splitted file of exams
        df = pd.read_csv(file_name) 
        try:
            for id,row in df.iterrows():
                if row['latitude']=='NotFound' or row['longitude']=='NotFound' or row['latitude'] is None or row['longitude'] is None:
                    notFoundAddr +=1
                    notFoundAddrFile.write("\"" + str(row['id']) + "\",\"" + file_name + "\",\"" + str(row['geocode_address']) + "\"\n")
        except Exception as e :
            print('Eccezione: ' + str(e))
            errorsFile.write('Eccezione: ' + str(e) + "for filename: " + file_name + "\n")

    print("Total addresses not found: " + str(notFoundAddr))
#---------END 2ND STEP-------------

def geocodeTest(address):
    geolocator = GoogleV3(api_key=AUTH_KEY_MM)
    location = geolocator.geocode(address)
    if location is not None:
        print("latitude " + str(location.point.latitude) + " longitude " + str(location.point.longitude))
    else:
        print("Location returned is None")