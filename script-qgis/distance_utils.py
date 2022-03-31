import pandas as pd

def get_not_found_distances(dist_folder, target_region_dict, region, disease, forceOutput=0):
    if forceOutput:
        return 1
    else:
        #read file with distances from water sources
        file_origin = dist_folder + "dist" + target_region_dict[region]+ "WaterTo" + disease + "Addr.csv"
        df_water = pd.read_csv(file_origin)
        #read file with all record of specific region and disease
        disease_file = "df_sigla_geocoded_" + region + "_"+ disease +"final.csv"
        df_origin = pd.read_csv(disease_file)
        #get hubName(correspond to row_id in disease file) with distances from water sources
        row_id_water = df_water["HubName"].drop_duplicates()
        #get rows without distances from water sources
        not_found_distances = df_origin[~df_origin['row_id'].isin(row_id_water)]
        
        #generate name for output file and save it
        file_out = dist_folder + disease_file[0:-4] #+ "_water_not_found.csv"
        not_found_distances.to_csv(file_out, index=False)
        
        #calculate percentage of rows with distances respect to rows without distances
        perc = len(row_id_water)/len(df_origin)
        
        print("---" + region + "-"+ disease + " statistics---\nNum of records with address without water:" + str(len(not_found_distances)) + 
                "\nWater distance file record:"+ str(len(df_water))+ "\nNum row_id with no distances:" + str(len(row_id_water)) + 
                "\nTot rows of file with geocode:" + str(len(df_origin)) + "\n perc: " + str(perc) + "\n")
        
        return len(not_found_distances)