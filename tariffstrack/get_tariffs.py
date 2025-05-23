import pandas as pd
import csv
from sqlalchemy import create_engine, Column, Integer, String, Float, MetaData, Table
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
import django
django.setup()

from tariffstrack.models import Tariff


# from sqlalchemy.orm import declarative_base

# Define a converter function to strip '%' and convert to float
def pct_to_float(x):
    return float(x.strip('%')) / 100

def clean_tariff_data(df):
     # Delete unused columns
    df.pop('Unnamed: 10')
    df.pop('Unnamed: 9')
    df.pop('Unnamed: 8')
    df.pop('Sources')
    df.pop("Legal authority")

    # Delete rows where 'Rate' is not determined
    df = df[df['Rate'] != 'TBD']
    df = df[df['Rate'].isnull() == False]

    # Convert 'Rate' from percent string to float
    df['Rate'] = df['Rate'].apply(pct_to_float)

    return df

def get_tariff_data():
    # url = "https://docs.google.com/spreadsheets/d/1s046O7ulAQ7d15TT-9-qtqemgGbEAGo5jF5ETEvyeXg/export?format=csv&id=1s046O7ulAQ7d15TT-9-qtqemgGbEAGo5jF5ETEvyeXg&gid=107324639"
    filename = "./tariffs.csv"
    # df = pd.read_csv(url)
    df = pd.read_csv(filename)
    return clean_tariff_data(df)
    #df.to_csv("tariffs.csv", index=False)

def match_country_codes(df):
    # read the list of countries paired with ISO codes and put into a dictionary
    dic = {}
    with open("wikipedia-iso-country-codes.csv", encoding='windows-1252', errors='replace') as f:
        file= csv.DictReader(f, delimiter=',')
        for line in file:
            dic[line['English short name lower case']] = line['Alpha-2 code']

    # Extract the country names from the tariff dataframe
    country_list = df["Geography"].unique()

    # Match the tariff countries to their ISO codes and return a dictionary of the countries and their codes
    countries = {}
    for country in country_list:
        if country in dic:
            countries[country] = dic[country]
        else:
            print(country + " not in list.")
    return countries

# replace all the country names in tariff dataframe to country codes
def replace_country_names(df, countries):
    for country in df['Geography']:
        if country not in countries:
            print(country + " not in list.")
        else:
            # print(country + " = " + countries[country])
            df.loc[df['Geography'] == country, 'Geography'] = countries[country]
    
    return df
 
# Connect to the database
# engine = create_engine('sqlite:///../db.sqlite3', echo=True)

# Base = declarative_base()

# Create the tariff table
# class Tariffs(Base):
#     __tablename__ = 'tariffs'
#     id = Column(Integer, primary_key=True)
#     target_type = Column(String)
#     geography = Column(String)
#     target = Column(String)
#     first_announced = Column(String)
#     date_in_effect = Column(String)
#     rate = Column(Float)
# Base.metadata.create_all(engine)


df = get_tariff_data() # Grab the tariff data from CSV
countries = match_country_codes(df) # Match the country codes to country names and return a dictionary
final_df = replace_country_names(df, countries) # Replace the country names in the tariff dataframe with the country codes

print(final_df.to_string())

confirmation = input("Do you want to clear the tariff database in preparation for update? (y/n): ")
if confirmation == 'y':
    print("Clearing the tariffs database...")
    Tariff.objects.all().delete()

    confirmation = input("Do you want to insert this data into the database? (y/n): ")
    if confirmation == 'y':
        # Iterate through the Tariff DataForm to create a Tariff object for each row and add to the database
        for index, row in final_df.iterrows():
            # Create a new Tariff object for each row
            tariff = Tariff(
                country_id=row['Geography'],
                target_type=row['Target type'],
                target=row['Target'],
                first_announced=row['First announced'],
                date_in_effect=row['Date in effect'],
                rate=row['Rate']
            )
            print(f"Inserting {row['Geography']}-{row['Rate']} tariff into database...")
            # Save the Tariff object to the database
            tariff.save()

# confirmation = input("Do you want to insert this data into the database? (y/n): ")
# if confirmation == 'y':
    # # Insert tariff dataframe into the database
    # print("Inserting...")
    # final_df.to_sql('tariffstrack_tariff', engine, if_exists='replace', index=False)