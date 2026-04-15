# bike_tool/utils.py
import math
import pandas as pd
from .data import BIKES

def format_currency(x):
    """Return integer currency string with rupee symbol. Safe for numeric or string input."""
    try:
        return f"₹{int(round(float(x))):,}"
    except Exception:
        return x

def calculate_emi(principal, annual_rate_percent, months):
    """
    Standard EMI formula.
    principal: loan amount (float)
    annual_rate_percent: annual interest rate in percent (float)
    months: tenure in months (int)
    returns: monthly EMI as float
    """
    r = annual_rate_percent / 12.0 / 100.0
    if months <= 0:
        return 0.0
    if r == 0:
        return principal / months
    emi = principal * r * (1 + r) ** months / ((1 + r) ** months - 1)
    return emi

def build_comparison_df(selected_models):
    """
    selected_models: list of tuples (brand, model)
    returns: DataFrame with specs as rows and models as columns (numeric values)
    """
    specs = [
        "Ex-Showroom Price",
        "Engine Displacement cc",
        "Max Power bhp",
        "Max Torque Nm",
        "Fuel Tank Capacity L",
        "Mileage kmpl"
    ]
    data = {}
    for brand, model in selected_models:
        key = f"{brand} {model}"
        specs_dict = BIKES[brand][model]
        col = [specs_dict.get(s, None) for s in specs]
        data[key] = col
    df = pd.DataFrame(data, index=specs)
    return df

def emi_breakdown_for_model(brand, model, down_payment=0.0, annual_rate=10.0, tenures=None):
    """
    Returns a DataFrame with EMI breakdown for the given model.
    tenures default: [3,6,9,12,36,60]
    """
    if tenures is None:
        tenures = [3, 6, 9, 12, 36, 60]
    price = float(BIKES[brand][model]["Ex-Showroom Price"])
    loan_amount = max(0.0, price - float(down_payment))
    rows = []
    for months in tenures:
        emi = calculate_emi(loan_amount, annual_rate, months)
        total_payable = emi * months
        total_interest = total_payable - loan_amount
        rows.append({
            "Tenure Months": months,
            "Monthly EMI": format_currency(emi),
            "Total Interest": format_currency(total_interest),
            "Total Amount Payable": format_currency(total_payable),
            "Loan Amount": format_currency(loan_amount)
        })
    return pd.DataFrame(rows)
