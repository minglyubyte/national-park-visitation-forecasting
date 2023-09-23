import pandas as pd
import json
import numpy as np
import os
from datetime import datetime

field_list = [
    "ParkName",
    "Year & Month Number",
    "ParkCode",
    "Year & Month Text",
    
    "Recreation Visits",
    "Non-Recreation Visits",
    "Total Visits",
    "Calendar YTD Visits",
    "Recreation Visitor Hours",
    "Non-Recreation Visitor Hours",
    "Total Visitor Hours",
    "Calendar YTD Visitor Hours",
    "Total Fiscal YTD Visitor Days Fiscal YTD",
    
    "Current Month Concessioner Lodging Recreation Overnight Stays",
    "Year-To-Date Concessioner Lodging Recreation Overnight Stays",
    
    "Current Month Concessioner Campgrounds Recreation Overnight Stays",
    "Year-To-Date Concessioner Campgrounds Recreation Overnight Stays",
    "NPS Campgrounds Tents",
    
    "Current Month NPS Campgrounds Recreation Overnight Stays",
    "Year-To-Date NPS Campgrounds Recreation Overnight Stays",
    "NPS Campgrounds RVs",
    
    "Current Month NPS Backcountry Recreation Overnight Stays",
    "Year-To-Date NPS Backcountry Recreation Overnight Stays",
    "NPS Campgrounds Total",
    
    "Current Month NPS Miscellaneous Recreation Overnight Stays",
    "Year-To-Date NPS Miscellaneous Recreation Overnight Stays",
    
    "Current Month Non-Recreation Overnight Stays Recreation Overnight Stays",
    "Year-To-Date Non-Recreation Overnight Stays Recreation Overnight Stays",
    
    "Current Month Total Overnight Stays Recreation Overnight Stays",
    "Year-To-Date Total Overnight Stays Recreation Overnight Stays",
    
    "This Month Total Rec",
    "Same Month Last Year Total Rec",
    "Percent Change Total Rec",
    "This Month Total Non-Rec",
    "Same Month Last Year Total Non-Rec",
    "Percent Change Total Non-Rec",
    "This Month Total Total Visits",
    "Same Month Last Year Total Visits",
    "Percent Change Total Visits",
    "This Month Total Total YTD",
    "Same Month Last Year Total YTD",
    "Percent Change Total YTD"]



def read_and_concatenate_dataframes(folder_path):
    """
    Interacts with a dropdown menu on a webpage.

    Args:
        folder_path (str): folder path to all the nps visitation data csv files
    """
    park_to_option_value = json.load(open("NPS_park_to_option_value.json","r"))
    park_info = json.load(open("national_park_code.json","r"))
    full_path = os.path.join(folder_path, "2_1_monthly_visit.csv")
    df = pd.read_csv(full_path)
    df = df.iloc[0:1,:]

    for key in park_info:
        print(key.strip())
        park_code = park_to_option_value[key.strip()]
        for i in range(1,120):
            if park_code == '2' and i == 1:
                continue
            current_path = os.path.join(folder_path, "{}_{}_monthly_visit.csv".format(park_code,i))
            df_temp = pd.read_csv(current_path).iloc[0:1,:]
            
            # combine current csv to cummulative csv
            df = pd.concat([df, df_temp], ignore_index=True)

    return df

def transform_date(date_string):
    """
    Transform date string into date format object. For example, "8/2023" -> "2023-08-01"

    Args:
        date_string (str): literal meaning, a date string
    """
    date_format = "%m/%Y"
    return datetime.strptime(date_string, date_format)

def df_transformation(df):
    """
    Transform the dataframe into the format we want including renaming column names and data type correction.

    Args:
        df (str): pandas dataframe
    """
    original_columns_list = list(df.columns)
    df.rename(columns = {original_columns_list[i]:field_list[i] for i in range(len(original_columns_list))}, 
            inplace = True)

    # Apply the transformation to the "Date" column
    df['Year & Month Number'] = df['Year & Month Number'].apply(transform_date)
    
    int_range_list = list(range(4,len(field_list)))
    percent_range_index = {41,38,35,32}
    for i in int_range_list:
        feature = field_list[i]
        if i in percent_range_index:
            df[feature] = df[feature].str.replace('%', '', regex=True).replace(',', '', regex=True).fillna(0).astype(float)
        else:
            df[feature] = df[feature].str.replace(',', '', regex=True).fillna(0).astype(float)
            
    df = df.sort_values(by = ['ParkName', 'Year & Month Number'])
    return df


if __name__ == "__main__":
    df = read_and_concatenate_dataframes("/Users/leo/Downloads")
    df = df_transformation(df)
    df.to_csv("national_park_monthly_visit_data.csv", index = False)
    






