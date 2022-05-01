import os
import numpy as np
import pandas as pd
import psycopg2
import random

def csv_files():

    #get names of only csv files
    csv_files = []
    for file in os.listdir(os.getcwd()):
        if file.endswith(".csv"):
            csv_files.append(file)

    return csv_files


def configure_dataset_directory(csv_files, dataset_dir):
  
    #make dataset folder to process csv files
    try: 
      mkdir = 'mkdir {0}'.format(dataset_dir)
      os.system(mkdir)
    except:
      pass

    #move csv files to dataset folder
    for csv in csv_files:
      mv_file = "mv '{0}' {1}".format(csv, dataset_dir)
      os.system(mv_file)

    return


def create_df(dataset_dir, csv_files):
  
    data_path = os.getcwd()+'/'+dataset_dir+'/'

    #loop through the files and create the dataframe
    df = {}
    for file in csv_files:
        try:
            df[file] = pd.read_csv(data_path+file, low_memory=False)
        except UnicodeDecodeError:
            df[file] = pd.read_csv(data_path+file, low_memory=False, encoding="cp437", errors='ignore') #if utf-8 encoding error
        print(file)
    
    return df


def clean_tbl_name(filename):
  
    #rename csv, force lower case, no spaces, no dashes
    clean_tbl_name = filename.lower().replace(" - ","_").replace("=","").replace("user","tableuser").replace("`","").replace("]","_").replace("[","_").replace(" ", "").replace("-","").replace(r"/","_").replace("\\","_").replace("$","").replace("%","").replace("#","").replace("(","").replace(")","").replace("?","").replace(",","").replace("*","").replace(":","").replace("'","").replace("&","").replace(";","").replace("__", "_")
    
    tbl_name = '{0}'.format(clean_tbl_name.split('.')[0])

    return tbl_name



def clean_colname(dataframe):
  
    #force column names to be lower case, no spaces, no dashes
    dataframe.columns = [x.lower().replace(" ", "_").replace("=","").replace("if_other", "if_other"+str(round(random.random(),2))).replace("`","").replace("]","_").replace("1","one").replace("2","two").replace("3","three").replace("4","four").replace("5","five").replace("6","six").replace("7","seven").replace("8","eight").replace("9","nine").replace("0","zero").replace("[","_").replace("-","").replace(r"/","_").replace("\\","_").replace(".","_").replace("$","").replace("%","").replace("#","").replace("(","").replace(")","").replace("?","").replace(",","").replace("*","").replace(":","").replace("'","").replace("&","").replace(";","").replace("__", "_") for x in dataframe.columns]
    
    #Limiting duplicate column names due to long strings
    first_colstr = dataframe.columns.str[0:20]
    end_colstr = dataframe.columns.str[-43:]
    dataframe.columns = first_colstr+end_colstr
        
    #processing data
    replacements = {
        'timedelta64[ns]': 'varchar',
        'object': 'text',
        'float64': 'float',
        'int64': 'int',
        'datetime64': 'timestamp'
    }

    col_str = ", ".join("{} {}".format(n, d) for (n, d) in zip(dataframe.columns, dataframe.dtypes.replace(replacements)))
               
    return col_str, dataframe.columns



def upload_to_db(host, dbname, user, password, tbl_name, col_str, file, dataframe, dataframe_columns):

    conn_string = "host=%s dbname=%s user=%s password=%s" % (host, dbname, user, password)
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    print('opened database successfully')
    
    #drop table with same name
    cursor.execute("drop table if exists %s;" % (tbl_name))

    #create table
    cursor.execute("create table %s (%s);" % (tbl_name, col_str))
    print('{0} was created successfully'.format(tbl_name)) 
    
    #insert values to table

    #save df to csv
    dataframe.to_csv(file, header=dataframe_columns, index=False, encoding="cp437", errors='ignore')

    #open the csv file, save it as an object
    my_file = open(file)
    print('file opened in memory')
    
    #upload to db
    SQL_STATEMENT = """
    COPY %s FROM STDIN WITH
        CSV
        HEADER
        DELIMITER AS ','
    """

    cursor.copy_expert(sql=SQL_STATEMENT % tbl_name, file=my_file)
    print('file copied to db')
    
    cursor.execute("grant select on table %s to public" % tbl_name)
    conn.commit()
    cursor.close()
    print('table {0} imported to db completed'.format(tbl_name))

    return
