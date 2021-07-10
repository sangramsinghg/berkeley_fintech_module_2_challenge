# -*- coding: utf-8 -*-
"""Helper functions to load and save CSV data.

This contains a helper function for loading and saving CSV files.

"""
import csv
import os

def save_csv(csvpath, header, data):
    """Reads the CSV file from path provided.

    Args:
        csvpath (Path): The csv file path.

    Returns:
        A list of lists that contains the rows of data from the CSV file.

    """
    dir_file = os.path.split(csvpath)
    dir = dir_file[0]
    file = dir_file[1]
    print(f"writing to '{csvpath}' - dir: '{dir}', file: '{file}'")

    # if the dir does not exist, create the dir
    if not os.path.exists(dir):
        print(f"Dir '{dir}' does not exist - We will create it first")
        os.makedirs(dir, mode, exist_ok =True)

    with open(csvpath, "w", newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=",")

        # Write the CSV Header
        csvwriter.writerow(header)

        # Write the CSV data
        for row in data:
            csvwriter.writerow(row)

def load_csv(csvpath):
    """Reads the CSV file from path provided.

    Args:
        csvpath (Path): The csv file path.

    Returns:
        A list of lists that contains the rows of data from the CSV file.

    """
    with open(csvpath, "r") as csvfile:
        data = []
        csvreader = csv.reader(csvfile, delimiter=",")

        # Skip the CSV Header
        next(csvreader)

        # Read the CSV data
        for row in csvreader:
            data.append(row)
    return data
