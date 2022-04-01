import pandas as pd
import os
import math
import pyarrow.feather as feather

def split_by_zoonoses(file_prefix, target_region):
    #zoonoses exams codes
    cod_salmonella =['AASE', 'ABSAL', 'ABSAN', 'ABSEN', 'ABSEV', 'CARSALM', 'ELFSACA', 'ELFSALG', 'ELFSALM', 'ELFSALT', 'ELFSANA', 'ELFSATA', 'ELFSATN', 'ELFSGNA', 'ELFSTNA', 'ELSAL', 'FTIPS', 'FTPS2', 'LMPCR', 'PCDSAL', 'PCRSAL', 'PFGESAL', 'PFSALCR', 'RCSALQL', 'RCSALQN', 'SAFSISC', 'SALDIS', 'SALFSIS', 'SALG2NA', 'SALGUNA', 'SALGUS2', 'SALGUSC', 'SALI2GN', 'SALI2TN', 'SALICA', 'SALICAC', 'SALICN', 'SALICNC', 'SALIS2N', 'SALISC2', 'SALISCN', 'SALISG2', 'SALISGN', 'SALISO', 'SALISO2', 'SALISOC', 'SALISOD', 'SALISOG', 'SALISON', 'SALISOT', 'SALIST2', 'SALISTA', 'SALISTC', 'SALISTN', 'SALITCN', 'SALITN', 'SALM', 'SALM2', 'SALM2NA', 'SALMCON', 'SALMEL', 'SALMNA', 'SALMPCR', 'SALMTA', 'SALPCA', 'SALPCCA', 'SALPCNA', 'SALPCNN', 'SALPCR', 'SALPCR2', 'SALPCRA', 'SALPCRG', 'SALPCRT', 'SALPCTA', 'SALPCTN', 'SALPGNA', 'SALPTNA', 'SALRAP', 'SALSA', 'SALSEL', 'SALSP', 'SALSPAN', 'SALSPAR', 'SALSPCR', 'SALSPNA', 'SALSPR', 'SALSPRR', 'SALT2NA', 'SALTUNA', 'SALTUO', 'SALTUO2', 'SALVPCR', 'SAMELNA', 'SARAPNA', 'SARSPUL', 'TIPSAL2', 'TIPSALM', 'TIPSALP', 'TIPSCR', 'TIPSCR2', 'TIPSISS']
    cod_epatite =['ELHA', 'ELHB', 'ELHC', 'ELHE', 'ELHE1', 'ELHEM', 'HACONCR', 'HASCRCR', 'HAVALCR', 'HAVCPCR', 'HAVPCR', 'HAVSPCN', 'HAVSPCR', 'HEVPCR', 'HEVPCR2', 'PCRHAV', 'PCRHAV1', 'PCRHCV', 'PCRHEV', 'PCRHEV1', 'PCRHEVP', 'PEGEPCR', 'RRTHACR', 'RRTHAV', 'RRTHAV2', 'RRTHAV3', 'RRTHAVE', 'RRTHAVN', 'RRTHEV', 'RRTNV', 'RRTNV2', 'SEQHBVP', 'SEQHEV']
    cod_leishmania=['IFILEI', 'IFILEIS', 'IFILENA', 'QPCRLEI']
    cod_leptospira=['LPAG', 'LPBOC', 'LPCS', 'LPEQ', 'LPEX', 'LPFE', 'LPSEL', 'PCRLPT']

    for region in target_region:
        file_origin = region + '/' + file_prefix + "_" + region + ".csv"
        df = pd.read_csv(file_origin)
        
        df_salmonella = df[df['ESAME'].isin(cod_salmonella)]
        df_epatite = df[df['ESAME'].isin(cod_epatite)]
        df_leishmania = df[df['ESAME'].isin(cod_leishmania)]
        df_leptospira = df[df['ESAME'].isin(cod_leptospira)]
        
        #Check if directory exists, if not, create it
        CHECK_FOLDER = os.path.isdir(region)
        if not CHECK_FOLDER:
            os.makedirs(region)
        
        df_salmonella.to_csv(region + "/" + file_prefix + "_" + region + "_salmonella.csv", index=False)
        df_epatite.to_csv(region + "/" + file_prefix + "_" + region + "_epatite.csv", index=False)
        df_leishmania.to_csv(region + "/" + file_prefix + "_" + region + "_leishmania.csv", index=False)
        df_leptospira.to_csv(region + "/" + file_prefix + "_" + region + "_leptospira.csv", index=False)

def split_in_multiple_csv(in_csv, infolder, outfolder, rows_num):
    # read DataFrame
    if infolder is not None:
        read_path = infolder + '/' + in_csv
    data = pd.read_csv(read_path)

    # number of csv files with rows_num rows
    k = math.ceil(len(data)/rows_num)

    for i in range(k):
        df = data[rows_num*i:rows_num*(i+1)]
        out_file_prefix = in_csv[:-4] 
        out_path = outfolder + '/' + out_file_prefix + str(i+1) +'.csv'
        df.to_csv(out_path, index=False)
    return k
        
def split_by_region_to_csv(geocode_file,region,file_format="csv"):
    if file_format == "csv":
        df = pd.read_csv(geocode_file)
    if file_format == "feather":
        df = feather.read_feather(geocode_file)
         
    prov = pd.read_csv('province.CSV',sep=';', encoding = 'utf8')
    selected_prov = prov.loc[prov['REGIONE'] == region, 'SIGLA']
    prov_list = []
    
    for p in selected_prov:
        #print(p)
        prov_list.append(p)
        
    prov_region = df[df['PROVINCIA PRELIEVO'].isin(prov_list)]
    sub_name = geocode_file.replace('.csv', '')
    
    #Check if directory exists, if not, create it
    CHECK_FOLDER = os.path.isdir(region)
    if not CHECK_FOLDER:
        os.makedirs(region)
                            
    prov_region.to_csv(f'{region}/{sub_name}_{region}.csv', index=False)
    
    print("Region " + region +" file created with " + str(len(prov_region)) + " rows")
    