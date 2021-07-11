# -*- coding: utf-8 -*-
"""Loan Qualifier Application.

This is a command line application to match applicants with qualifying loans.

Example:
    $ python app.py
"""

# import all the relevant libraries/functionality
import sys
# import fire and questionary for user interaction
import fire
import questionary
# import pathlib to handle file Paths
from pathlib import Path

# import load and save csv functionality
from qualifier.utils.fileio import load_csv
from qualifier.utils.fileio import save_csv

# import calculators
from qualifier.utils.calculators import (
    calculate_monthly_debt_ratio,
    calculate_loan_to_value_ratio,
)

# import filters
from qualifier.filters.max_loan_size import filter_max_loan_size
from qualifier.filters.credit_score import filter_credit_score
from qualifier.filters.debt_to_income import filter_debt_to_income
from qualifier.filters.loan_to_value import filter_loan_to_value

# Global to control debug output
debug = False
# Global to control the maximum number of time to wait for a valid input
max_input_tries = 5

def check_csvpath_name(csvpath, try_attempt):
    """Checks the csv path for validity. Handles corner cases related to csvpath entries

    Input:
        csvpath - the path received from the user. This function validates the path.
        try_attempt - the attempt number. Tells if this is the 1st time, 2nd time the function 
                        is called for validating the path
    Returns:
        Returns true if the path is a valid path ending in .csv and is at least 5 characters long
        Otherwise returns false. If Ctrl+c or max input tries are detected then the application exists
    """

    # Check if Ctrl+C was entered
    if csvpath == None:
        sys.exit("Ctrl+C detected. Exiting")
    # check if the attempt was greater than or equal to max_input_tries     
    elif try_attempt >= max_input_tries - 1:
        sys.exit(f"Exiting because no valid input received in {max_input_tries} attempts")
    # check if the csv path is valied and end with a .csv and is atleast 5 characters long.
    elif csvpath and csvpath.lower().endswith(".csv") and len(csvpath) >= 5:
        return True
    # the csv path is invalid so display a message and return
    else:
        print(f"Incorrect or incomplete csv path '{csvpath}' entered - should end in .csv and should be greater than 4 characters")
        print("Press Ctrl+C to exit")
        return False


def load_bank_data(try_attempt = 0):
    """Ask for the file path to the latest banking data and load the CSV file.

    Input:
        try_attempt - is this the 1st time, 2nd time, etc. that this function was called
    Returns:
        The bank data from the data rate sheet CSV file.
    """
    ''' Sample Input
        .csv: data/daily_rate_sheet.csv
    '''

    # Ask for the .csv file from where to load the bank data
    csvpath = questionary.text("Enter a file path to a rate-sheet (.csv):").ask()
    # check if the csv file path name is valid
    if check_csvpath_name(csvpath, try_attempt):
        # the path name is valid, so check if the path exists. 
        csvpath = Path(csvpath)
        if not csvpath.exists():
            sys.exit(f"Oops! Can't find this path: {csvpath}")
        # the path exists, load the bank data from the csv file.
        return load_csv(csvpath)
    else:
        # the path name is invalid. Retry for a maximum of max_input_tries to obtain a valid path name
        return load_bank_data(try_attempt+1)

def get_user_applicant_info(query_text, info_type):
    """Prompt dialog to get the applicant's financial information.

    Input:
        query_text: the text that is prompted to the user
        info_type: int, float, etc. that describe the type of the expected query
    Returns:
        Returns the applicant's financial information only if it is valid as per type.
    """

    # Try for max specified attempts to obtain a valid query item 
    for input_try in range(max_input_tries):
        try:
            # Try to obtain the input
            info = questionary.text(f"What's your {query_text}?").ask()
            # bail out if ctrl+c was entered. Questionary handles ctrl+c by returning None
            if info == None:
                sys.exit("Ctrl+C detected. Exiting the program")
            # do a typecast of the data. 
            # If a character string is entered when digits are expected, the application will throw an exception
            info = info_type(info)
            # return the typecasted information
            return info
        except Exception as exception:
            # an invalid input/empty input was entered.
            # The invalid input could be characters when digits are expected.
            if input_try < max_input_tries - 1:
                # display message to try again unless it is the last attempt
                print(f"invalid {query_text}. Try again or Ctrl+C to exit.")
    # bail out of the application if no valid input is received in max specified attempts.
    sys.exit(f"Exiting because no valid input received in {max_input_tries} attempts")

def get_applicant_info():
    """Prompt dialog to get the applicant's financial information.

    Returns:
        Returns the applicant's financial information.
    """

    ''' Sample Applicant Input

        credit score: 600
        monthly debt: 10000
        monthly income: 30000
        desired loan: 100000
        home value: 200000
    '''

    # Use the get_user_applicant_info function to obtain valid input and 
    # to handle invalid input. This function will retry obtaining the input if it invalid for a max specified attempts
    # This function also takes care of typecasting the information. 
    credit_score = get_user_applicant_info("credit score", int)
    debt = get_user_applicant_info("current amount of monthly debt", float)
    income = get_user_applicant_info("total monthly income", float)
    loan_amount = get_user_applicant_info("desired loan amount", float)
    home_value = get_user_applicant_info("home value", float)

    # if debugging is enabled, display the information obtained
    if debug == True:
        print(f"Credit score : {credit_score}")
        print(f"Debt         : {debt}")
        print(f"Income       : {income}")
        print(f"Loan Amount  : {loan_amount}")
        print(f"Home Value   : {home_value}")

    # return the information obtained
    return credit_score, debt, income, loan_amount, home_value


def find_qualifying_loans(bank_data, credit_score, debt, income, loan, home_value):
    """Determine which loans the user qualifies for.

    Loan qualification criteria is based on:
        - Credit Score
        - Loan Size
        - Debit to Income ratio (calculated)
        - Loan to Value ratio (calculated)

    Args:
        bank_data (list): A list of bank data.
        credit_score (int): The applicant's current credit score.
        debt (float): The applicant's total monthly debt payments.
        income (float): The applicant's total monthly income.
        loan (float): The total loan amount applied for.
        home_value (float): The estimated home value.

    Returns:
        A list of the banks willing to underwrite the loan.

    """

    # Calculate the monthly debt ratio
    monthly_debt_ratio = calculate_monthly_debt_ratio(debt, income)
    print(f"The monthly debt to income ratio is {monthly_debt_ratio:.02f}")

    # Calculate loan to value ratio
    loan_to_value_ratio = calculate_loan_to_value_ratio(loan, home_value)
    print(f"The loan to value ratio is {loan_to_value_ratio:.02f}.")

    # Run qualification filters

    # filter loans based on max loan size that the banks are willing to allow
    bank_data_filtered = filter_max_loan_size(loan, bank_data)
    if debug == True:
        print(f"Found {len(bank_data_filtered)} qualifying loans based on max loan size filter")

    # filter loans based on the minimum credit score requirements of the bank
    bank_data_filtered = filter_credit_score(credit_score, bank_data_filtered)
    if debug == True:
        print(f"Found {len(bank_data_filtered)} qualifying loans based on credit score filter")

    # filter loans based on debt to income ratio
    bank_data_filtered = filter_debt_to_income(monthly_debt_ratio, bank_data_filtered)
    if debug == True:
        print(f"Found {len(bank_data_filtered)} qualifying loans based on debt to income filter")

    # filter loans based on loan to home value ratio
    bank_data_filtered = filter_loan_to_value(loan_to_value_ratio, bank_data_filtered)
    if debug == True:
        print(f"Found {len(bank_data_filtered)} qualifying loans based on loan to value filter")

    # Inform the user how many loans they qualify for if they qualify for atleast 1 loan
    if len(bank_data_filtered) > 0:
        print(f"Found {len(bank_data_filtered)} qualifying loans")

    return bank_data_filtered


def save_qualifying_loans(qualifying_loans, header, prompt = True, try_attempt = 0):
    """Saves the qualifying loans to a CSV file.

    Args:
        qualifying_loans (list of lists): The qualifying bank loans.
        header: The header to be written to the csv file
        prompt: Do we want to prompt the user to save the loans output to a csv file
        try_attempt: is the 1st, 2nd, or nth time this function is called for saving qualifying loans
    """
    # prompt the user if they want to save the loans to a csv file. 
    # If prompt parameter is not set then assume that the user wants to save the file. 
    # This is used when an invalid file name is received. 
    # We retry to obtain a valid file name without prompting the user if they want to save to a csv file
    if prompt == True:
        save_the_csv = questionary.confirm("Do you want to save the loans output to a csv file?").ask()
    else:
        save_the_csv = True

    # if the user wants to save the qualifying loans to a csv file
    if save_the_csv == True:
        # obtain the csv file name
        csvpath = questionary.text("Please provide the csv path (ending in .csv) where you want to save the qualifying loans:").ask()
        # check if the csv file name is valid
        if check_csvpath_name(csvpath, try_attempt):
            if debug == True:
                print(header)
            # a valid csv file name was obtained. Save the qualifying loans to a csv file and inform the user
            save_csv(csvpath, header, qualifying_loans, debug)
            print(f"Saved the qualifying loans to '{csvpath}'")
        else:
            # if the csv file name was invalid and we have no tried for a max specified attempts,
            # retry obtaining a valid csv file name
            save_qualifying_loans(qualifying_loans, header, False, try_attempt+1)
    else:
        # inform the user that we are not saving the qualifying loans in a csv file
        print("As desired, we are not saving the qualifying loans in a csv file")



def run(verbose = False, help = False, v = False, h = False):
    """The main function for running the script."""

    # Print the application's command line options
    if help == True or h == True:
        print("python app.py --verbose : for debug mode")
        print("python app.py --v       : for debug mode")
        print("python app.py --help    : for help options")
        print("python app.py --h       : for help options")
        sys.exit()

    # Set the debugging mode based on the verbose or v option
    if verbose == True or v == True:
        global debug
        debug = True
        print(f"Verbose mode: setting debug to {debug}")

    # Load the latest Bank data
    header, bank_data = load_bank_data()

    # Get the applicant's information
    credit_score, debt, income, loan_amount, home_value = get_applicant_info()

    # Find qualifying loans
    qualifying_loans = find_qualifying_loans(
        bank_data, credit_score, debt, income, loan_amount, home_value
    )

    # if we didn't fine any qualifying loans. Inform the user and bail out because we don't need
    # to save anything to a csv file.
    if len(qualifying_loans) == 0:
        sys.exit("Sorry! you don't qualify for any loans")

    # Save qualifying loans to a csv file
    save_qualifying_loans(qualifying_loans, header)


if __name__ == "__main__":
    fire.Fire(run)
