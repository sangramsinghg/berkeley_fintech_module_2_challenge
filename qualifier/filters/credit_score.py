# -*- coding: utf-8 -*-
"""Credit Score Filter.

This script filters a bank list by the user's minimum credit score.

"""


def filter_credit_score(credit_score, bank_list):
    """Filters the bank list by the mininim allowed credit score set by the bank.

    Args:
        credit_score (int): The applicant's credit score.
        bank_list (list of lists): The available bank loans.

    Returns:
        A list of qualifying bank loans.
    """

    # create an empty list
    credit_score_approval_list = []
    # go throught all the banks to find which banks meet the credit score requirements
    for bank in bank_list:
        # select the bank if the user's credit score meets the bank's minimum credit score requirement 
        if credit_score >= int(bank[4]):
            credit_score_approval_list.append(bank)
    # return the list of qualifying banks
    return credit_score_approval_list
