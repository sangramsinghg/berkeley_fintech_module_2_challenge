# -*- coding: utf-8 -*-
"""Max Loan Size Filter.

This script filters the bank list by comparing the user's loan value
against the bank's maximum loan size.

"""


def filter_max_loan_size(loan_amount, bank_list):
    """Filters the bank list by the maximum allowed loan amount.

    Args:
        loan_amount (int): The requested loan amount.
        bank_list (list of lists): The available bank loans.

    Returns:
        A list of qualifying bank loans.
    """

    # create an empty list
    loan_size_approval_list = []

    # go throught all the banks to find which banks meet the loan size requirements
    for bank in bank_list:
        # select the bank if the user's loan request meets the bank's maximum loan requirement
        if loan_amount <= int(bank[1]):
            loan_size_approval_list.append(bank)
    # return the list of qualifying banks
    return loan_size_approval_list
