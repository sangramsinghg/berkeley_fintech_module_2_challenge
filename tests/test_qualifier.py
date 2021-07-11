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


def test_save_csv():
    qualifying_loans_path = "./data/output/qualifying_loans.csv"
    header = ["Lender", "Max Loan Amount", "Max LTV", "Max DTI", "Min Credit Score", "Interest Rate"]
    data = [["FHA Fredie Mac", '300000', '0.85', '0.45', '550', '4.35']]
    fileio.save_csv(qualifying_loans_path,
                    header,
                    data)
    assert Path(qualifying_loans_path).exists() == True
    header_from_saved_file, data_from_saved_file = fileio.load_csv(Path(qualifying_loans_path))
    # validate that the header saved in the file is the same as the header we tried to save
    assert header == header_from_saved_file
    # validate that the non-header data saved in the file is the same as the non-header data we tried to save
    assert data == data_from_saved_file

def test_calculate_monthly_debt_ratio():
    assert calculators.calculate_monthly_debt_ratio(1500, 4000) == 0.375

def test_calculate_loan_to_value_ratio():
    assert calculators.calculate_loan_to_value_ratio(210000, 250000) == 0.84

def test_filters():
    header, bank_data = fileio.load_csv(Path('./data/daily_rate_sheet.csv'))
    current_credit_score = 750
    debt = 1500
    income = 4000
    loan = 210000
    home_value = 250000

    monthly_debt_ratio = 0.375

    loan_to_value_ratio = 0.84

    bank_data_filtered = filter_max_loan_size(loan, bank_data)
    assert len(bank_data_filtered) == 18

    bank_data_filtered = filter_credit_score(current_credit_score, bank_data_filtered)
    assert len(bank_data_filtered) == 9

    bank_data_filtered = filter_debt_to_income(monthly_debt_ratio, bank_data_filtered)
    assert len(bank_data_filtered) == 8

    bank_data_filtered = filter_loan_to_value(loan_to_value_ratio, bank_data_filtered)
    assert len(bank_data_filtered) == 6

    # Test the save csv file functionality 
    qualifying_loans_path = './tests/output_validation/qualifying_loans_final.csv'
    fileio.save_csv(qualifying_loans_path, header, bank_data_filtered)
    assert Path(qualifying_loans_path).exists() == True
    header_from_saved_file, data_from_saved_file = fileio.load_csv(Path(qualifying_loans_path))
    row_count = 0
    for row in data_from_saved_file:
        row_count += 1
    assert row_count == 6

def test_filters_elaborate():
    header, bank_data = fileio.load_csv(Path('./data/daily_rate_sheet.csv'))
    current_credit_score = 750
    debt = 1500
    income = 4000
    loan = 210000
    home_value = 250000

    monthly_debt_ratio = 0.375

    loan_to_value_ratio = 0.84

    loans_initial_path = './tests/output_elaborate_validation/loans_initial.csv'
    fileio.save_csv(loans_initial_path, header, bank_data)
    header_from_saved_file, data_from_saved_file = fileio.load_csv(Path(loans_initial_path))
    assert header == header_from_saved_file
    loan_index = 0
    for row in data_from_saved_file:
        assert loan_data[loan_index] == row
        loan_index += 1

    bank_data_filtered = filter_max_loan_size(loan, bank_data)
    loans_max_loan_path = './tests/output_elaborate_validation/loans_max_loan.csv'
    fileio.save_csv(loans_max_loan_path, header, bank_data_filtered)
    header_from_saved_file, data_from_saved_file = fileio.load_csv(Path(loans_max_loan_path))
    assert header == header_from_saved_file
    loan_index = 0
    loan_index_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 16, 18, 20]
    for row in data_from_saved_file:
        assert loan_data[loan_index_list[loan_index]] == row
        loan_index += 1

    bank_data_filtered = filter_credit_score(current_credit_score, bank_data_filtered)
    loans_credit_score_path = './tests/output_elaborate_validation/loans_credit_score.csv'
    fileio.save_csv(loans_credit_score_path, header, bank_data_filtered)
    header_from_saved_file, data_from_saved_file = fileio.load_csv(Path(loans_credit_score_path))
    assert header == header_from_saved_file
    loan_index = 0
    loan_index_list = [0, 5, 9, 12, 13, 14, 16, 18, 20]
    for row in data_from_saved_file:
        assert loan_data[loan_index_list[loan_index]] == row
        loan_index += 1

    bank_data_filtered = filter_debt_to_income(monthly_debt_ratio, bank_data_filtered)
    loans_debt_ratio_path = './tests/output_elaborate_validation/loans_debt_ratio.csv'
    fileio.save_csv(loans_debt_ratio_path, header, bank_data_filtered)
    header_from_saved_file, data_from_saved_file = fileio.load_csv(Path(loans_debt_ratio_path))
    assert header == header_from_saved_file
    loan_index = 0
    loan_index_list = [0, 5, 9, 12, 13, 14, 18, 20]
    for row in data_from_saved_file:
        assert loan_data[loan_index_list[loan_index]] == row
        loan_index += 1

    bank_data_filtered = filter_loan_to_value(loan_to_value_ratio, bank_data_filtered)

    # Test the save csv file functionality 
    qualifying_loans_path = './tests/output_elaborate_validation/qualifying_loans_final.csv'
    fileio.save_csv(qualifying_loans_path, header, bank_data_filtered)
    assert Path(qualifying_loans_path).exists() == True

    header_from_saved_file, data_from_saved_file = fileio.load_csv(Path(qualifying_loans_path))
    assert header == header_from_saved_file
    loan_index = 0
    loan_index_list = [0, 5, 9, 12, 14, 18]
    for row in data_from_saved_file:
        assert loan_data[loan_index_list[loan_index]] == row
        loan_index += 1
