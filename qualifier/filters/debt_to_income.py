# -*- coding: utf-8 -*-
"""Debt to Income Filter.

This script filters the bank list by the applicant's
maximum debt-to-income ratio.

"""


def filter_debt_to_income(monthly_debt_ratio, bank_list):
    """Filters the bank list by the maximum debt-to-income ratio allowed by the bank.

    Args:
        monthly_debt_ratio (float): The applicant's monthly debt ratio.
        bank_list (list of lists): The available bank loans.

    Returns:
        A list of qualifying bank loans.
    """

    # create an empty list
    debit_to_income_approval_list = []
    # go throught all the banks to find which banks meet the debt to income ratio requirements
    for bank in bank_list:
        # select the bank if the user's monthly debt to income ratio meets the bank's maximum debt to income ratio requirement 
        if monthly_debt_ratio <= float(bank[3]):
            debit_to_income_approval_list.append(bank)
    # return the list of qualifying banks
    return debit_to_income_approval_list
