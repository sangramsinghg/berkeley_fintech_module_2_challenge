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


def test_save_csv():
    qualifying_loans_path = "./data/output/qualifying_loans.csv"
    header = ["Lender", "Max Loan Amount", "Max LTV", "Max DTI", "Min Credit Score", "Interest Rate"]
    data = [["FHA Fredie Mac", 300000, 0.85, 0.45, 550, 4.35]]
    fileio.save_csv(qualifying_loans_path,
                    header,
                    data)
    assert Path(qualifying_loans_path).exists() == True

def test_calculate_monthly_debt_ratio():
    assert calculators.calculate_monthly_debt_ratio(1500, 4000) == 0.375

def test_calculate_loan_to_value_ratio():
    assert calculators.calculate_loan_to_value_ratio(210000, 250000) == 0.84

def test_filters():
    bank_data = fileio.load_csv(Path('./data/daily_rate_sheet.csv'))
    current_credit_score = 750
    debt = 1500
    income = 4000
    loan = 210000
    home_value = 250000

    monthly_debt_ratio = 0.375

    loan_to_value_ratio = 0.84

    header = ["Lender", "Max Loan Amount", "Max LTV", "Max DTI", "Min Credit Score", "Interest Rate"]

    loans_initial_path = './tests/output_validation/loans_initial.csv'
    fileio.save_csv(loans_initial_path, header, bank_data)

    bank_data_filtered = filter_max_loan_size(loan, bank_data)
    assert len(bank_data_filtered) == 18
    loans_max_loan_path = './tests/output_validation/loans_max_loan.csv'
    fileio.save_csv(loans_max_loan_path, header, bank_data_filtered)

    bank_data_filtered = filter_credit_score(current_credit_score, bank_data_filtered)
    assert len(bank_data_filtered) == 9
    loans_credit_score_path = './tests/output_validation/loans_credit_score.csv'
    fileio.save_csv(loans_credit_score_path, header, bank_data_filtered)

    bank_data_filtered = filter_debt_to_income(monthly_debt_ratio, bank_data_filtered)
    assert len(bank_data_filtered) == 8
    loans_debt_ratio_path = './tests/output_validation/loans_debt_ratio.csv'
    fileio.save_csv(loans_debt_ratio_path, header, bank_data_filtered)

    bank_data_filtered = filter_loan_to_value(loan_to_value_ratio, bank_data_filtered)
    assert len(bank_data_filtered) == 6

    # Test the save csv file functionality 
    qualifying_loans_path = './tests/output_validation/qualifying_loans_final.csv'
    fileio.save_csv(qualifying_loans_path, header, bank_data_filtered)
    assert Path(qualifying_loans_path).exists() == True
