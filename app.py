import streamlit as st 
import pandas as pd
import math 

st.title("College Loan Payment Calculator")

st.write("### Input Data")
col1, col2 = st.columns(2)

loan_amount = col1.number_input("College Loan Amount", min_value=0, value=100000)
interest_rate = col1.number_input("Interest Rate (in %)", min_value=0.0, value=4.5)
loan_term = col2.number_input("Loan Term (in years)", min_value=1, value=10)

# Calculate the monthly interest rate and number of payments
monthly_interest_rate = (interest_rate / 100) / 12
number_of_payments = loan_term * 12

# Avoid division by zero by checking if interest rate is zero
if interest_rate > 0:
    monthly_payment = (
        loan_amount
        * (monthly_interest_rate * (1 + monthly_interest_rate) ** number_of_payments)
        / ((1 + monthly_interest_rate) ** number_of_payments - 1)
    )
else:
    monthly_payment = loan_amount / number_of_payments  # Simplified calculation for 0% interest

# Total payments and total interest
total_payments = monthly_payment * number_of_payments
total_interest = total_payments - loan_amount

st.write("### Repayments")
col1, col2, col3 = st.columns(3)
col1.metric(label="Monthly Repayments", value=f"${monthly_payment:,.2f}")
col2.metric(label="Total Repayments", value=f"${total_payments:,.0f}")
col3.metric(label="Total Interest", value=f"${total_interest:,.0f}")

# Create a data-frame with the payment schedule
schedule = []
remaining_balance = loan_amount

for i in range(1, int(number_of_payments) + 1):
    interest_payment = remaining_balance * monthly_interest_rate
    principal_payment = monthly_payment - interest_payment
    remaining_balance -= principal_payment
    year = math.ceil(i / 12)
    schedule.append(
        [
            i,
            monthly_payment,
            principal_payment,
            interest_payment,
            remaining_balance,
            year,
        ]
    )

df = pd.DataFrame(
    schedule,
    columns=["Month", "Payment", "Principal", "Interest", "Remaining Balance", "Year"],
)

# Display the data-frame as a chart
st.write("### Payment Schedule")
payments_df = df[["Year", "Remaining Balance"]].groupby("Year").min()
st.line_chart(payments_df)
