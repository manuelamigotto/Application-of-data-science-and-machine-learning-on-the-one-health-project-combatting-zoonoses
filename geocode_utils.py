import datetime
import os
import pyarrow.feather as feather
import pandas as pd
import jsonpickle

def generate_error_file_name(error_foldername, error_filename):
    now = datetime.datetime.now()
    year = now.strftime("%Y")
    month = now.strftime("%m")
    day = now.strftime("%d")
    time = now.strftime("%H%M%S")

    '''Check if directory exists, if not, create it'''
    CHECK_FOLDER = os.path.isdir(error_foldername)

    # If folder doesn't exist, then create it.
    if not CHECK_FOLDER:
        os.makedirs(error_foldername)

    file_errors_name = error_filename + year + month + day + time + ".txt"
    return error_foldername + '/' + file_errors_name

def set_lat_long(df, row_id, latitude, longitude):
    df.iloc[row_id,df.columns.get_loc('latitude')] = latitude
    df.iloc[row_id,df.columns.get_loc('longitude')] = longitude

def set_notFound(df, row_id):
    df.iloc[row_id,df.columns.get_loc('latitude')]="NotFound" 
    df.iloc[row_id,df.columns.get_loc('longitude')]="NotFound"

def add_complete_geocode_address(df1):
    #create column for complete address for geocoding 
    df1['geocode_address'] = df1['INDIRIZZO PRELIEVO'].fillna('-')
    df1['CAP PRELIEVO'] = df1['CAP PRELIEVO'].astype(str).str[:5]
    df1['geocode_address'] = df1['geocode_address'].astype(str) + ',' + \
        df1['CAP PRELIEVO'].astype(str) + ',' + df1['COMUNE PRELIEVO'] + ',' + df1['PROVINCIA PRELIEVO'] + ',' + 'Italia'
    df1['geocode_address'] = df1['geocode_address'].map(lambda x: x.lstrip(',-'))
    return df1 
         
def create_complete_address(file_in, file_out, file_type, printOn = True, saveOn = True):
    if file_type == 'feather':
        df1 = feather.read_feather(file_in) #'dataframe_sigla'
    if file_type == 'csv':
        df1 = pd.read_csv(file_in)

    df1 = add_complete_geocode_address(df1)
    
    if printOn:
        print("item with prov address: " + str(sum(pd.notnull(df1['INDIRIZZO ATTPROV CORRELATA']))))
        print("item with prel address: " + str(sum(pd.notnull(df1['INDIRIZZO ATTPREL CORRELATA']))))
        print("item with NO prel address: " + str(sum(pd.isnull(df1['INDIRIZZO ATTPREL CORRELATA']))))
        
    if saveOn:
        if file_type == 'csv':
            #save dataframe in csv file format
            df1.to_csv(file_out, index=False) #'df_sigla_country.csv'
        if file_type == 'feather':
            feather.write_feather(df1, file_out)
    else:
        return df1
    
def create_rag_soc_address(file_in, file_out, file_type):
    print("Adding geocode addresses...")
    if file_type == 'feather':
        df1 = feather.read_feather(file_in) #'dataframe_sigla'
    if file_type == 'csv':
        df1 = pd.read_csv(file_in)
    #create address geocoding column
    df1['geocode_address'] = df1['RAGSOCATTPROVCORR']
    df1['geocode_address'] = df1['geocode_address'].fillna(df1['RAGIONE SOCATTPRELCORR']) + ',' + \
        df1['CAP PRELIEVO'].astype(str).str[:5] + ',' + \
        df1['COMUNE PRELIEVO'] + ',' + df1['PROVINCIA PRELIEVO'] + ',' + 'Italia'
    
    #save dataframe in csv file format
    df1.to_csv(file_out, index=False)
    print("File with geocode addresses saved")
    
def create_centroid_address(file_in, file_out, file_type):
    print("Adding geocode addresses...")
    if file_type == 'feather':
        df1 = feather.read_feather(file_in) #'dataframe_sigla'
    if file_type == 'csv':
        df1 = pd.read_csv(file_in)

    #create address geocoding column
    df1['geocode_address'] = df1['CAP PRELIEVO'].astype(str).str[:5] + ',' + \
        df1['COMUNE PRELIEVO'] + ',' + df1['PROVINCIA PRELIEVO'] + ',' + 'Italia'
    df1['geocode_address'] = df1['geocode_address'].astype(str).map(lambda x: x.lstrip(',-')) 
    
    #save dataframe in csv file format
    df1.to_csv(file_out, index=False)
    print("File with geocode addresses saved")
    
def open_addresses_dict_if_exist(addresses_dict_json):
    addr_dict = {}
     #check if extists json file of address dictionary (key=string address value=DistanceFeature)
    file_exists = os.path.exists(addresses_dict_json)
    
    if file_exists:
        with open(addresses_dict_json, "r") as json_file:
            geo_dict_obj = jsonpickle.decode(json_file.read())            
            addr_dict = geo_dict_obj.features_dict
    return addr_dict