# DROP TABLES

demographics_immigration_table_drop = "DROP TABLE IF EXISTS demographics_immigration"
states_population_table_drop = "DROP TABLE IF EXISTS states_population"


# CREATE TABLES

demographics_immigration_table_create = ("""
  CREATE TABLE IF NOT EXISTS demographics_immigration (    
    state_code varchar PRIMARY KEY,
	year varchar NOT NULL,
    month varchar NOT NULL,    
    median_age decimal,
    male_population bigint, 
    female_population bigint, 
    total_population bigint);    
""")

states_population_table_create = ("""
  CREATE TABLE IF NOT EXISTS states_population (
    state_code text PRIMARY KEY,
    state_name varchar,
    city_name varchar,
    median_age decimal,
    male_population bigint, 
    female_population bigint, 
    total_population bigint);
""")

# INSERT RECORDS

demographics_immigration_table_insert = ("INSERT INTO demographics_immigration (state_code, year, month, median_age, male_population, female_population, total_population) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")

states_population_table_insert = ("INSERT INTO states_population (state_code, state_name, city_name, median_age, male_population, female_population, total_population) VALUES (%s, %s, %s, %s, %s, %s, %s)")



# QUERY LISTS

create_table_queries = [demographics_immigration_table_create, states_population_table_drop]
drop_table_queries = [demographics_immigration_table_drop, states_population_table_drop]