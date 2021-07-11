# Import pathlib
from pathlib import Path

#Import fileio
from qualifier.utils import fileio

# Import Calculators
from qualifier.utils import calculators

# Import Filters
from qualifier.filters.max_loan_size import filter_max_loan_size
from qualifier.filters.credit_score import filter_credit_score
from qualifier.filters.debt_to_income import filter_debt_to_income
from qualifier.filters.loan_to_value import filter_loan_to_value

# The input loan data that we reference to validate the filtering of loans
loan_data = [
    ["Bank of Big - Premier Option", '300000', '0.85', '0.47', '740', '3.6'],
    ["West Central Credit Union - Premier Option", '400000', '0.9', '0.35', '760', '2.7'],
    ["FHA Fredie Mac - Premier Option", '600000', '0.9', '0.43', '790',	'3.6'],
    ["FHA Fannie Mae - Premier Option", '500000', '0.9', '0.47', '780', '3.6'],
    ["General MBS Partners - Premier Option", '400000', '0.95',	'0.35', '790', '3.0'],
    ["Bank of Fintech - Premier Option", '300000', '0.9', '0.47', '740', '3.15'],
    ["iBank - Premier Option", '500000', '0.85', '0.46', '780',	'3.15'],
    ["Goldman MBS - Premier Option", '500000', '0.8', '0.4', '770', '3.6'],
    ["Citi MBS - Premier Option", '400000', '0.9', '0.47', '780', '3.6'],
    ["Prosper MBS - Premier Option", '400000', '0.85', '0.42', '750', '3.45'],
    ["Developers Credit Union - Premier Option", '300000', '0.85', '0.47', '770', '3.45'],
    ["Bank of Stodge & Stiff - Premier Option", '500000', '0.9', '0.41', '790', '3.15'],
    ["Bank of Big - Starter Plus", '300000', '0.85', '0.39', '700', '4.35'],
    ["West Central Credit Union - Starter Plus", '300000', '0.8', '0.44', '650', '3.9'],
    ["FHA Fredie Mac - Starter Plus", '300000', '0.85', '0.45', '550', '4.35'],
    ["FHA Fannie Mae - Starter Plus", '200000', '0.9', '0.37', '630', '4.2'],
    ["General MBS Partners - Starter Plus", '300000', '0.85', '0.36', '670', '4.05'],
    ["Bank of Fintech - Starter Plus", '100000', '0.85', '0.47', '610', '4.5'],
    ["iBank - Starter Plus", '300000', '0.9', '0.4', '620', '3.9'],
    ["Goldman MBS - Starter Plus", '100000', '0.8',	'0.43', '600', '4.35'],
    ["Citi MBS - Starter Plus", '300000', '0.8', '0.39', '740', '4.05'],
    ["Prosper MBS - Starter Plus", '100000', '0.9',	'0.38', '640', '3.75'],
    ["Developers Credit Union - Starter Plus", '200000', '0.85', '0.46', '640',	'4.2'],
    ["Bank of Stodge & Stiff - Starter Plus", '100000', '0.8', '0.35', '680', '4.35']
]

def save_to_csv_and_validate_bank_loan_data(csvpath, header, bank_loan_data, loan_index_list):
    """Saves the header and bank loan data to csv path and validates it by reading from 
        the csv file and cross checking with the original data based on the loan index list

    Input:
        csvpath - the csv file where the bank data will be saved.
        header - header to be written to the csv file
        bank_loan_data - bank loan data to be written to the csv file
        loan_index_list - list to be used to access the original loan data for cross
                            checking purpose
    Returns:
        Nothing. Writes data to the csv file and Validates the loan data saved to the csv file
    """

    # save header and data to the csv file
    fileio.save_csv(csvpath, header, bank_loan_data)
    # ensure that the file was created
    assert Path(csvpath).exists() == True
    # read from the csv file
    header_from_saved_file, data_from_saved_file = fileio.load_csv(Path(csvpath))
    # ensure that the header matches the header that was supposed to have been written
    assert header == header_from_saved_file
    
    # go through all the rows of the csv file and cross check using the loan index list
    loan_index = 0
    for row in data_from_saved_file:
        assert loan_data[loan_index_list[loan_index]] == row
        loan_index += 1

def test_save_csv():
    """Saves the cooked header and data to a csv file and validate that the data was written properly

    """
    # cook the file name, header and data
    qualifying_loans_path = "./data/output/qualifying_loans.csv"
    header = ["Lender", "Max Loan Amount", "Max LTV", "Max DTI", "Min Credit Score", "Interest Rate"]
    data = [["FHA Fredie Mac", '300000', '0.85', '0.45', '550', '4.35']]
    # write the header and data to the csv file
    fileio.save_csv(qualifying_loans_path,
                    header,
                    data)
    # validate that the file was created 
    assert Path(qualifying_loans_path).exists() == True
    # load the header and data from the newly created file
    header_from_saved_file, data_from_saved_file = fileio.load_csv(Path(qualifying_loans_path))
    # validate that the header saved in the file is the same as the header we tried to save
    assert header == header_from_saved_file
    # validate that the non-header data saved in the file is the same as the non-header data we tried to save
    assert data == data_from_saved_file

def test_calculate_monthly_debt_ratio():
    """Validate that the monthly debt ratio is calculated without any issues

    """
    assert calculators.calculate_monthly_debt_ratio(1500, 4000) == 0.375

def test_calculate_loan_to_value_ratio():
    """Validate that the loan to value ratio is calculated without any issues

    """
    assert calculators.calculate_loan_to_value_ratio(210000, 250000) == 0.84

def test_filters():
    """Validate that the qualifying loans are filtered without any issues.
        This test does not validate by comparing the actual data in the csv file to the expected data.
        It validates it by ensuring that the number of entries matches the expected number of entries
    """
    # load the header and bank loan data from the csv file
    header, bank_data = fileio.load_csv(Path('./data/daily_rate_sheet.csv'))

    # create a user profile with credit score, debt, income, loan and home value
    current_credit_score = 750
    debt = 1500
    income = 4000
    loan = 210000
    home_value = 250000

    # create the monthly debt ratio and loan to value ratio
    monthly_debt_ratio = 0.375
    loan_to_value_ratio = 0.84

    # filter loans based on max loan size and validate the result by checking the number of entries
    # against expected number of entries
    bank_data_filtered = filter_max_loan_size(loan, bank_data)
    assert len(bank_data_filtered) == 18

    # filter loans based on the credit score and validate the result by checking the number of entries
    # against expected number of entries
    bank_data_filtered = filter_credit_score(current_credit_score, bank_data_filtered)
    assert len(bank_data_filtered) == 9

    # filter loans based on the debt to income ratio and validate the result by checking the number of entries
    # against expected number of entries
    bank_data_filtered = filter_debt_to_income(monthly_debt_ratio, bank_data_filtered)
    assert len(bank_data_filtered) == 8

    # filter loans based on the loan to home value ratio and validate the result by checking the number of entries
    # against expected number of entries
    bank_data_filtered = filter_loan_to_value(loan_to_value_ratio, bank_data_filtered)
    assert len(bank_data_filtered) == 6

    # Test the save csv file functionality by writting the qualified loans to a csv file
    qualifying_loans_path = './tests/output_validation/qualifying_loans_final.csv'
    # save to a csv file 
    fileio.save_csv(qualifying_loans_path, header, bank_data_filtered)
    # ensure that file was created
    assert Path(qualifying_loans_path).exists() == True
    # load header and data from newly created csv file
    header_from_saved_file, data_from_saved_file = fileio.load_csv(Path(qualifying_loans_path))
    # count the rows in the csv file and validate that the expected amount of rows were written to the csv file
    row_count = 0
    for row in data_from_saved_file:
        row_count += 1
    assert row_count == 6

def test_filters_elaborate():
    """Validate that the qualifying loans are filtered without any issues.
        This test validates by comparing the actual data in the csv file to the expected data.
    """
    # load the header and bank loan data from the csv file
    header, bank_data = fileio.load_csv(Path('./data/daily_rate_sheet.csv'))

    # create a user profile with credit score, debt, income, loan and home value
    current_credit_score = 750
    debt = 1500
    income = 4000
    loan = 210000
    home_value = 250000

    # create the monthly debt ratio and loan to value ratio
    monthly_debt_ratio = 0.375
    loan_to_value_ratio = 0.84

    # Create a csv file based on the original data and compare the two files to test the save functionality
    loans_initial_path = './tests/output_elaborate_validation/loans_initial.csv'
    loan_index_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
    save_to_csv_and_validate_bank_loan_data(loans_initial_path, header, bank_data, loan_index_list)

    # filter loans based on max loan size and validate the result by checking the actual data written to csv file
    # against expected data. This also creates a csv file with the results of the filtering
    bank_data_filtered = filter_max_loan_size(loan, bank_data)
    loans_max_loan_path = './tests/output_elaborate_validation/loans_max_loan.csv'
    loan_index_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 16, 18, 20]
    save_to_csv_and_validate_bank_loan_data(loans_max_loan_path, header, bank_data_filtered, loan_index_list)

    # filter loans based on credit score and validate the result by checking the actual data written to csv file
    # against expected data. This also creates a csv file with the results of the filtering
    bank_data_filtered = filter_credit_score(current_credit_score, bank_data_filtered)
    loans_credit_score_path = './tests/output_elaborate_validation/loans_credit_score.csv'
    loan_index_list = [0, 5, 9, 12, 13, 14, 16, 18, 20]
    save_to_csv_and_validate_bank_loan_data(loans_credit_score_path, header, bank_data_filtered, loan_index_list)

    # filter loans based on debt to income ratio and validate the result by checking the actual data written to csv file
    # against expected data. This also creates a csv file with the results of the filtering
    bank_data_filtered = filter_debt_to_income(monthly_debt_ratio, bank_data_filtered)
    loans_debt_ratio_path = './tests/output_elaborate_validation/loans_debt_ratio.csv'
    loan_index_list = [0, 5, 9, 12, 13, 14, 18, 20]
    save_to_csv_and_validate_bank_loan_data(loans_debt_ratio_path, header, bank_data_filtered, loan_index_list)

    # filter loans based on loan to home value ratio and validate the result by checking the actual data written to csv file
    # against expected data. This also creates a csv file with the results of the filtering
    bank_data_filtered = filter_loan_to_value(loan_to_value_ratio, bank_data_filtered)
    # Test the save csv file functionality 
    qualifying_loans_path = './tests/output_elaborate_validation/qualifying_loans_final.csv'
    loan_index_list = [0, 5, 9, 12, 14, 18]
    save_to_csv_and_validate_bank_loan_data(qualifying_loans_path, header, bank_data_filtered, loan_index_list)
