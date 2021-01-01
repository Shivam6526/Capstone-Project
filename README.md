#This project is done as part of the Capstone Project submission in the Udacity Data Engineering Nanodegree.

Capstone Project: Reporting US demographics integrated with Immigration data (City-Wise)

Introduction:
I have chosen the US immigration data (~ 3mn records) for my project which has the the information of the immigrants such as the mode of arrival, gender and their birth year, etc for each month and year. 
Along with that, I chose the US cities demographics data which has the information such as the male and female population and median age for each city within State. 

Use Case- To create a data model to ingest the City wise demographics data and create a data pipeline which will report the US demographics data along with the Immigration data. The data will ultimately help in reporting-
A.The change in the distribution of the population (City-wise) considering the Immigrants (assuming US cities demographics data to be static).
B.Reporting crucial data like the busiest mode of arrival of the immigrants & the busiest state to receive the migrants flow.

Execution steps:
A. Run the data_cleaning.py script to read and clean the immigration data and finally write into a csv file
B. Run create_tables.py to create the required tables as per the data model
C. Run etl_pipeline.py to load the data in tables.

Follow the Project_Report for more detailed view of the project.
