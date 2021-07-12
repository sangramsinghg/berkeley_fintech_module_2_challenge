# -*- coding: utf-8 -*-
"""Loan to Value Filter.

This script filters the bank list by the applicant's maximum home loan
to home value ratio.

"""


def filter_loan_to_value(loan_to_value_ratio, bank_list):
    """Filters the bank list by the maximum loan to value ratio.

    Args:
        loan_to_value_ratio (float): The applicant's loan to value ratio.
        bank_list (list of lists): The available bank loans.

    Returns:
        A list of qualifying bank loans.
    """

    # create an empty list
    loan_to_value_approval_list = []
    # go throught all the banks to find which banks meet the loan to home value ratio requirements
    for bank in bank_list:
        # select the bank if the user's loan to home value ratio meets the bank's maximum loan to home value ratio requirement
        if loan_to_value_ratio <= float(bank[2]):
            loan_to_value_approval_list.append(bank)
    # return the list of qualifying banks
    return loan_to_value_approval_list
