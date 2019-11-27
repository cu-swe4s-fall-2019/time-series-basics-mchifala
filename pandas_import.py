import pandas as pd
import numpy as np
import datetime as dt
import os
import argparse


def join_df(left_df, right_df):
    """
    This function performs a left join on a user-specified
    column and fills all result NaN values with 0's

    Parameters:
    - left_df(DataFrame): The left dataframe to join
    - right_df(DataFrame): The right dataframe to join

    Returns:
    - left_df(DataFrame): The joined dataframes

    """
    left_df = left_df.merge(right_df, how="left",
                            left_index=True, right_index=True)
    left_df.fillna(0, inplace=True)

    return left_df


def set_time_index(df, time_column):
    """
    This function converts a user-specified column into a
    datetime index.

    Parameters:
    - df(DataFrame): The dataframe to transform
    - time_column(str): The column to convert

    Returns:
    - df(DataFrame)

    """
    df.set_index(pd.to_datetime(df[time_column]), inplace=True)
    df.drop(columns=[time_column], inplace=True)

    return df


def rename_columns(df, file, col_to_rename):
    """
    This function renames a column to the name of the file
    and removes columns containing "Unnamed".

    Parameters:
    - df(DataFrame): The dataframe to transform
    - col_to_rename: The column to transform

    returns:
    - df(DataFrame)

    """
    df.rename({col_to_rename: file.split("/")[1].split("_")[0]},
              axis=1, inplace=True)
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

    return df


def import_df(file):
    """
    This function imports a data file of specific format
    and applies other useful utility functions to transform the data

    Parameters:
    - file(str): The file path to the .csv file

    Returns:
    - df(DataFrame): The dataframe containing the cleaned time series data
    """
    df = pd.read_csv(file, encoding="utf-8")

    df = set_time_index(df, "time")
    if df["value"].dtype == object:
        df = df[pd.to_numeric(df['value'], errors='coerce').notnull()]
    df["value"] = df["value"].astype("float64")
    df = rename_columns(df, file, "value")

    return df


def round_df(df, interval, cols_to_keep):
    """
    This function rounds an index of datatimes and
    filters out irrelevant columns.

    Parameters:
    - df(DataFrame): The dataframe to transform
    - interval(str): The time interval to round to
    - cols_to_keep(list): The columns to keep

    Returns:
    - df(DataFrame)

    """
    df.index = df.index.round(interval)
    df = df.loc[:, cols_to_keep]

    return df


def group_df(df, cols_to_sum, cols_to_avg):
    """
    This function groups a dataframe by its index,
    sums certain columns, and averages other columns.

    Parameters:
    - df(DataFrame): The dataframe to transform
    - cols_to_sum(list): A list of columns to apply sum()
    - cols_to_avg(list): A list of columns to apply avg()

    Returns:
    - df(DataFrame)

    """
    sum_df = (df
              .loc[:, cols_to_sum]
              .groupby(by=df.index)
              .sum())

    mean_df = (df
               .loc[:, cols_to_avg]
               .groupby(by=df.index)
               .mean())

    return sum_df.merge(mean_df,
                        left_index=True,
                        right_index=True)


def main(base_file, directory):
    """
    This main function joins files from a directory to a base file,
    rounds and groups by time stamp, and sums or averages the data
    columns. The results are printed to .csv files

    Parameters:
    - base_file(str): A command line argument for the base file path
    - directory(str): A command line argument for the file directory path.

    Returns:
    - None
    """
    df = import_df(directory+"/"+base_file)
    for file in os.listdir(directory):
        if ".csv" in file and base_file not in file:
            right_df = import_df(directory+"/"+file)
            df = join_df(df, right_df)

    df_5 = round_df(df, "5min", ["activity", "basal", "bolus",
                                 "cgm", "hr", "meal", "smbg"])
    df_15 = round_df(df, "15min", ["activity", "basal", "bolus",
                                   "cgm", "hr", "meal", "smbg"])

    df_5 = group_df(df_5, ["activity", "bolus", "meal"],
                    ["smbg", "hr", "cgm", "basal"])

    df_15 = group_df(df_15, ["activity", "bolus", "meal"],
                     ["smbg", "hr", "cgm", "basal"])

    df_5.to_csv("pandas_5.csv", index_label="time")
    df_15.to_csv("pandas_15.csv", index_label="time")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Time series input")

    parser.add_argument('base_file',
                        type=str,
                        help='Path of the file to join on')

    parser.add_argument('directory',
                        type=str,
                        help='Directory of files to join')

    args = parser.parse_args()
    main(args.base_file, args.directory)
