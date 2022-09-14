import pandas as pd
import numpy as np
import os, sys
from sklearn.preprocessing import MinMaxScaler, Normalizer, StandardScaler, LabelEncoder
from datetime import datetime

sys.path.insert(0, '../scripts/')
sys.path.insert(0, '../logs/')
sys.path.append(os.path.abspath(os.path.join('..')))
from logger import App_Logger

app_logger = App_Logger("logs/data_preProcessing.log").get_app_logger()


class dataProcessor:

    def __init__(self, df: pd.DataFrame) -> None:
        self.df = df
        self.logger = App_Logger(
            "logs/data_preProcessing.log").get_app_logger()


### DATA_CLEANER ###

    def drop_duplicates(self) -> pd.DataFrame:
        droped = self.df[self.df.duplicated()].index
        return self.df.drop(index=droped, inplace=True)

    def convert_to_numbers(self) -> pd.DataFrame:
        self.df = self.df.apply(pd.to_numeric, errors='coerce')
        return self.df

    def convertByteMB(self, coll) -> pd.DataFrame:
        for col in coll:
            self.df[col] = (self.df[col]) / 1*10e+5
            self.df.rename(
                columns={col: f'{col[:-7]}(MegaBytes)'}, inplace=True)
        print('Byte to MB change error')
        return self.df
    

###DATA_INFO_COLLECTION_FUNTIONS###

    def show_datatypes(self) -> pd.DataFrame:
        return self.df.dtypes

    def show_data_description(self) -> pd.DataFrame:
        return self.df.describe()

    def show_data_information(self) -> pd.DataFrame:
        return self.df.info()

    def show_statistical_info(self) -> pd.DataFrame:
        return self.df.agg(['mean'])

    def show_correlation(self) -> pd.DataFrame:
        return self.df.corr()

    def collective_grouped_mean(self, colomnName: str) -> pd.DataFrame:
        groupby_colomnName = self.df.groupby(colomnName)
        return groupby_colomnName.mean()

    def list_coloumn_names(self) -> pd.DataFrame:
        return self.df.columns
    
###MISSING_DATA_MANIPULATORS###

    def columns_WithMissingValue(self):
        miss = []
        dff = self.df.isnull().any()
        sum = 0 
        for col in dff:
            if col == True:
                miss.append(dff.index[sum])
            sum += 1 
        return miss
    
    def c_missing_percentage(self):  ###column based###
        c_null = self.df.isnull().sum()
        total_entries = self.df.shape[0]
        missing_percentage = []
        for missing_entries in c_null:
            value = str(
                round(((missing_entries/total_entries)*100),2)
            ) + " %"
            missing_percentage.append(value)
            
        missing_df = pd.DataFrame(c_null, columns=['total_missing_values'])
        missing_df['missing_percentage'] = missing_percentage
        return missing_df
    
    
    ## To add other features from existing features
    
    def add_week_day(self, day_of_week_col: str) -> pd.DataFrame:
        try:
            date_index = self.df.columns.get_loc(day_of_week_col)
            self.df.insert(date_index + 1, 'WeekDay',
                           self.df[day_of_week_col].apply(lambda x: 1 if x <= 5 else 0))

            self.logger.info("Successfully Added WeekDay Column to the DataFrame")

        except Exception as e:
            self.logger.exception("Failed to Add WeekDay Column")
            
            
    def add_number_of_days_to_holiday(self, state_holiday_col: str):
        try:
            date_index = self.df.columns.get_loc(state_holiday_col)

            modified_index = self.modify_holiday_list(
                self.df[state_holiday_col].values.tolist())
            days_to_holiday_index = []
            i = 0
            last_holiday_index = 0
            for index, value in enumerate(modified_index):
                if(index == len(modified_index) - 1):
                    for j in range(last_holiday_index+1, len(modified_index)):
                        days_to_holiday_index.append(0)
                elif(value == 'neither' or value == 'after' or value == 'before'):
                    i += 1
                elif(value == 'during' and i != 0):
                    last_holiday_index = index
                    for j in range(i):
                        days_to_holiday_index.append(i)
                        i = i-1
                    days_to_holiday_index.append(0)
                    i = 0
                elif(value == 'during' and i == 0):
                    days_to_holiday_index.append(i)
                    last_holiday_index = index
                    continue

            self.df.insert(date_index + 1, 'DaysToHoliday',
                           days_to_holiday_index)

            self.logger.info("Successfully Added DaysToHoliday Column")

        except Exception as e:
            self.logger.exception("Failed to Add DaysToHoliday Column")


    def add_number_of_days_after_holiday(self, state_holiday_col: str):
        try:
            date_index = self.df.columns.get_loc(state_holiday_col)

            modified_index = self.modify_holiday_list(
                self.df[state_holiday_col].values.tolist())

            days_to_after_holiday_index = [0] * len(modified_index)
            i = 0
            last_holiday_index = modified_index.index('during')

            for index, value in enumerate(modified_index):
                if(value == 'before'):
                    if(index > last_holiday_index):
                        i += 1
                        days_to_after_holiday_index[index] = i
                    continue
                elif(value == 'after'):
                    i += 1
                    days_to_after_holiday_index[index] = i
                elif(value == 'during'):
                    last_holiday_index = index
                    i = 0
                    continue

            days_to_after_holiday_index.insert(0, 0)

            self.df.insert(date_index + 1, 'DaysAfterHoliday',
                           days_to_after_holiday_index[:-1])

            self.logger.info("Successfully Added DaysAfterHoliday Column")

        except Exception as e:
            self.logger.exception("Failed to Add DaysAfterHoliday Column")
            
            
    def add_month_timing(self, day_col: str) -> pd.DataFrame:
        try:
            date_index = self.df.columns.get_loc(day_col)
            self.df.insert(date_index + 1, 'MonthTiming',
                           self.df[day_col].apply(self.return_day_status_in_month))

            self.logger.info("Successfully Added MonthTiming Column")

        except Exception as e:
            self.logger.exception("Failed to Add MonthTiming Column")

    

    def get_season(self, month: int):
        if(month <= 2 or month == 12):
            return 'Winter'
        elif(month > 2 and month <= 5):
            return 'Spring'
        elif(month > 5 and month <= 8):
            return 'Summer'
        else:
            return 'Autumn'

    def add_season(self, month_col: str) -> pd.DataFrame:
        try:
            date_index = self.df.columns.get_loc(month_col)
            self.df.insert(date_index + 1, 'Season',
                           self.df[month_col].apply(self.get_season))

            self.logger.info("Successfully Added Season Column")

        except Exception as e:
            self.logger.exception("Failed to Add Season Column")


    def label_columns(self, columns: list) -> dict:
        labelers = {}
        try:
            for col in columns:
                le = LabelEncoder()
                le_fitted = le.fit(self.df[col].values)
                self.df[col] = le_fitted.transform(self.df[col].values)
                labelers[col] = le_fitted

            return labelers

        except Exception as e:
            print("Failed to Label Encode columns")
            
            
    def standardize_column(self, column: str) -> pd.DataFrame:
        """
            Returns the objects DataFrames column normalized using Normalizer
            Parameters
            ----------
            column:
                Type: str
            length:
                Type: int

            Returns
            -------
            pd.DataFrame
        """
        try:
            std_column_df = pd.DataFrame(self.df[column])
            std_column_values = std_column_df.values
            standardizer = StandardScaler()
            normalized_data = standardizer.fit_transform(std_column_values)
            self.df[column] = normalized_data

            return self.df
        except:
            print("Failed to standardize the column")
            
            
    def standardize_columns(self, columns: list) -> pd.DataFrame:
        try:
            for col in columns:
                self.df = self.standardize_column(col)

            return self.df
        except:
            print(f"Failed to standardize {col} column")