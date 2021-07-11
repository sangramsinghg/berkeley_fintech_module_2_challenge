# -*- coding: utf-8 -*-
"""Loan Qualifier Application.

This is a command line application to match applicants with qualifying loans.

Example:
    $ python app.py
"""
import sys
import fire
import questionary
from pathlib import Path
import signal

from qualifier.utils.fileio import load_csv
from qualifier.utils.fileio import save_csv

from qualifier.utils.calculators import (
    calculate_monthly_debt_ratio,
    calculate_loan_to_value_ratio,
)

from qualifier.filters.max_loan_size import filter_max_loan_size
from qualifier.filters.credit_score import filter_credit_score
from qualifier.filters.debt_to_income import filter_debt_to_income
from qualifier.filters.loan_to_value import filter_loan_to_value

# Global to control debug output
debug = False

def check_csvpath(csvpath):
    if csvpath == None:
        sys.exit("Ctrl+C detected. Exiting")
    elif csvpath and csvpath.lower().endswith(".csv") and len(csvpath) >= 5:
        return True
    else:
        print(f"Incorrect or incomplete csv path '{csvpath}' entered - should end in .csv and should be greater than 4 characters")
        print("Press Ctrl+C to exit")
        return False


def load_bank_data():
    """Ask for the file path to the latest banking data and load the CSV file.

    Returns:
        The bank data from the data rate sheet CSV file.
    """
    ''' Sample Input

        .csv: data/daily_rate_sheet.csv
    '''

    csvpath = questionary.text("Enter a file path to a rate-sheet (.csv):").ask()
    if check_csvpath(csvpath):
        csvpath = Path(csvpath)
        if not csvpath.exists():
            sys.exit(f"Oops! Can't find this path: {csvpath}")
        return load_csv(csvpath)
    else:
        load_bank_data()

def get_user_applicant_info(query_text, info_type):
    """Prompt dialog to get the applicant's financial information.

    Input:
        query_text: the text that is prompted to the user
        info_type: int, float, etc. that describe the type of the expected query
    Returns:
        Returns the applicant's financial information only if it is valid as per type.
    """
    while True:
        try:
            info = questionary.text(f"What's your {query_text}?").ask()
            if info == None:
                sys.exit("Ctrl+C detected. Exiting the program")
            info = info_type(info)
            break
        except Exception as exception:
            print(f"invalid {query_text}. Try again or Ctrl+C to exit.")
    return info

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

    credit_score = get_user_applicant_info("credit score", int)
    debt = get_user_applicant_info("current amount of monthly debt", float)
    income = get_user_applicant_info("total monthly income", float)
    loan_amount = get_user_applicant_info("desired loan amount", float)
    home_value = get_user_applicant_info("home value", float)

    if debug == True:
        print(f"Credit score : {credit_score}")
        print(f"Debt         : {debt}")
        print(f"Income       : {income}")
        print(f"Loan Amount  : {loan_amount}")
        print(f"Home Value   : {home_value}")

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
    bank_data_filtered = filter_max_loan_size(loan, bank_data)
    if debug == True:
        print(f"Found {len(bank_data_filtered)} qualifying loans based on max loan size filter")

    bank_data_filtered = filter_credit_score(credit_score, bank_data_filtered)
    if debug == True:
        print(f"Found {len(bank_data_filtered)} qualifying loans based on credit score filter")

    bank_data_filtered = filter_debt_to_income(monthly_debt_ratio, bank_data_filtered)
    if debug == True:
        print(f"Found {len(bank_data_filtered)} qualifying loans based on debt to income filter")

    bank_data_filtered = filter_loan_to_value(loan_to_value_ratio, bank_data_filtered)
    if debug == True:
        print(f"Found {len(bank_data_filtered)} qualifying loans based on loan to value filter")

    print(f"Found {len(bank_data_filtered)} qualifying loans")

    return bank_data_filtered


def save_qualifying_loans(qualifying_loans, header, prompt = True):
    """Saves the qualifying loans to a CSV file.

    Args:
        qualifying_loans (list of lists): The qualifying bank loans.
        header: The header to be written to the csv file
        prompt: Do we want to prompt the user to save the loans output to a csv file
    """
    if prompt == True:
        save_the_csv = questionary.confirm("Do you want to save the loans output to a csv file?").ask()
    else:
        save_the_csv = True

    if save_the_csv == True:
        csvpath = questionary.text("Please provide the csv path (ending in .csv) where you want to save the qualifying loans:").ask()
        if check_csvpath(csvpath):
            if debug == True:
                print(header)
            save_csv(csvpath, header, qualifying_loans, debug)
            print(f"Saved the qualifying loans to '{csvpath}'")
        else:
            save_qualifying_loans(qualifying_loans, header, False)
    else:
        print("As desired, we are not saving the output in a csv file")



def run(verbose = False, help = False, v = False, h = False):
    """The main function for running the script."""

    # Print the help options
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

    # Save qualifying loans
    save_qualifying_loans(qualifying_loans, header)


if __name__ == "__main__":
    fire.Fire(run)
