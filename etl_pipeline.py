import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *
import numpy as np
import datetime
from psycopg2.extensions import register_adapter, AsIs
psycopg2.extensions.register_adapter(np.int64, psycopg2._psycopg.AsIs)
import configparser

def load_states_population_data(cur, conn):
    """
    Summary: This function will load the required colunms after reading the cities-demographics data to the states population table                  
    Params: cursor to the redshift database connection, redshift connection
    Returns: None
    """
    # open states demographics file
    df = pd.read_csv('us-cities-demographics.csv', delimiter = ';')
    no_of_rows_in_source = len(df.index)
    
    # Unit test to check if the data was read successfully
    if (no_of_rows_in_source > 0):
        print ('Cities demographics data read successfully')
    else:
        raise ValueError('Zero rows found after reading Cities demographics data')
    
    # insert states demographics record
    states_data = (df.loc[0,['State Code','State','City','Median Age','Male Population','Female Population','Total Population']]).values.tolist()   
    cur.execute(states_population_table_insert, states_data)
    
    rows_inserted = cur.execute('SELECT COUNT(*) FROM states_population')
    
    #Unit test to check if the insert is successful
    if rows_inserted > 0:
        print ("Data inserted successfully in states_population table")
    else:
        raise ValueError('Zero rows inserted in states_population table')
    
    # Data Completeness Check
    if (no_of_rows_in_source != rows_inserted):
        raise ValueError('Count mismatch: records {} not matching with source {}'.format(rows_inserted,no_of_rows_in_source))
    
def process_immigration_demographics_data(cur, conn):
    """
    Summary: This function will load the cleaned immigration data and will calculate the values required for demographics based on grouping on the state_code
    Params: cursor to the redshift database connection, redshift connection
    Returns: None    
    """
    df = pd.read_csv('immigration-cleaned-data.csv', low_memory=False)
    fetched_rows = len(df.index)
    
    # Unit test to check if the data was read successfully
    if (fetched_rows > 0):
        print ('Immigration demographics data read successfully')
    else:
        raise ValueError('Zero rows found after reading Immigration demographics data')
        
    # calculate the number of records in source
    no_of_unique_rows_source = df['i94addr'].nunique()
    
    immigration_required_data = pd.DataFrame(columns = ['state_code', 'year', 'month', 'median_age', 'male_population', 'female_population', 'total_population'])
    immigration_required_data['state_code'] = df['i94addr'].unique()
    immigration_required_data['year'] = df['year']
    immigration_required_data['month'] = df['month_name']
    immigration_required_data['median_age'] = df.groupby('i94addr', as_index=False)['immigrant_age'].median()
    immigration_required_data['male_population'] = df.groupby('i94addr', as_index=False).filter(df.gender == 'M').value_counts()
    immigration_required_data['female_population'] = df.groupby('i94addr', as_index=False).filter(df.gender == 'F').value_counts()
    immigration_required_data['total_population'] = df.groupby('i94addr', as_index=False)['gender'].value_counts()
    
    immigration_demographics_data = (immigration_required_data.loc[0, ['state_code', 'year', 'month', 'median_age', 'male_population', 'female_population', 'total_population']]).values.tolist()
    cur.execute(demographics_immigration_table_insert, immigration_demographics_data)
    
    # count the number of records in demographics_immigration table
    rows_inserted = cur.execute('SELECT COUNT(*) FROM demographics_immigration')
    
    #Unit test to check if the insert is successful
    if rows_inserted > 0:
        print ("Data inserted successfully in demographics_immigration table")
    else:
        raise ValueError('Zero rows inserted in demographics_immigration table')
    
    # Data Completeness Check
    if (no_of_unique_rows_source != rows_inserted):
        raise ValueError('Count mismatch: records {} not matching with source {}'.format(rows_inserted,no_of_unique_rows_source))
    
def main():
    """
    Summary: main function 
    Param: None
    Returns: None
    """
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()

    load_states_population_data(cur, conn)
    process_immigration_demographics_data(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()