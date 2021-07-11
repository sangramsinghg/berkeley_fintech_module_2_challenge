# -*- coding: utf-8 -*-
"""Helper functions to load and save CSV data.

This contains a helper function for loading and saving CSV files.

"""
import csv
import os
from pathlib import Path

def save_csv(csvpath, header, data, debug = False):
    """Writes header and data to the CSV file provided in the path.

    Args:
        csvpath: The csv file path.
        header: header of the csv file
        data: data to be written to the csv file
        debug: do you want to print any debug information to the console

    Returns:
        Nothing but save the header and data to the csvpath specified

    """

    # split the csv path to two components - the dir path and the file name
    dir_file = os.path.split(csvpath)
    dir = dir_file[0]
    file = dir_file[1]

    # inform the csvpath, dir path and filename to the user if so desired by the user
    if debug == True:
        print(f"writing to '{csvpath}' - dir: '{dir}', file: '{file}'")

    # if the dir does not exist, create the dir
    if not os.path.exists(dir):
        print(f"Dir '{dir}' does not exist - We will create it first")
        os.makedirs(dir, exist_ok = True)

    # open the csv file based on the path and write the header and data to the csv file specified
    # the csv file is opened in write mode and newline is not specified so that empty rows are not created.
    csvpath = Path(csvpath)
    with open(csvpath, "w", newline='') as csvfile:
        # initialized the writer to use comma as a separator of the data items.
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
        header of the csv file
        A list of lists that contains the rows of data from the CSV file.

    """

    # open the csv file in read only mode and read the csv header and data
    with open(csvpath, "r") as csvfile:
        data = []
        csvreader = csv.reader(csvfile, delimiter=",")

        # Detect the CSV header and return it to the caller
        header = next(csvreader)

        # Read the CSV data
        for row in csvreader:
            data.append(row)
    return header, data
