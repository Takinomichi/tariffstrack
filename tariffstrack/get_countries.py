import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, MetaData, Table, ForeignKey
import csv
from sqlalchemy.orm import declarative_base

def match_country_codes(df):
    # read the list of countries paired with ISO codes and put into a dictionary
    dic = {}
    with open("wikipedia-iso-country-codes.csv") as f:
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

# read in the tariffs csv to obtain country names
filename = "./tariffs.csv"
df = pd.read_csv(filename)

countries = match_country_codes(df)

# Add headers and convert the countries dictionary to a DataFrame
countries_df = pd.DataFrame(countries.items(), columns=['country','code'])

# print(countries_df.to_string())

#Connect to the database
engine = create_engine('sqlite:///test.db')

# Base = declarative_base()

# # Create the countries table
# class Countries(Base):
#     __tablename__ = 'countries'
#     id = Column(Integer, primary_key=True)
#     country = Column(String)
#     code = Column(String, unique=True)

# Base.metadata.create_all(engine)

# Insert countries into the countries table
print("Inserting...")
countries_df.to_sql('countries', engine, if_exists='replace', index=False)