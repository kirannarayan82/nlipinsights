import streamlit as st
import pandas as pd
from datetime import datetime
import datetime as dt

# Sample format information
format_info = """
### Expected Excel Format
The Excel file should have the following columns:
- **Name**: Name of the participant
- **Program**: Either "Practitioners" or "Masters"
- **Date**: The date of the program in YYYY-MM-DD format
- **City**: The city where the program was conducted
"""

# Main function
def main():
    st.title("NLP Training Program Insights")

    # Display format information
    st.markdown(format_info)

    # File uploader
    uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])

    # Input prices for the programs
    practitioners_price = st.number_input("Enter the price for the Practitioners Program (in INR):", min_value=0, value=100000)
    masters_price = st.number_input("Enter the price for the Masters Program (in INR):", min_value=0, value=50000)

    if uploaded_file:
        df = pd.read_excel(uploaded_file)
        
        # Ensure the columns are as expected
        expected_columns = ['Name', 'Program', 'Date', 'City']
        if all(column in df.columns for column in expected_columns):
            # Convert Date column to datetime
            df['Date'] = pd.to_datetime(df['Date'])
            
            # Program prices
            prices = {'Practitioners': practitioners_price, 'Masters': masters_price}
            df['Revenue'] = df['Program'].map(prices)

            # Compute insights
            revenue_by_city = df.groupby('City')['Revenue'].sum().reset_index()
            revenue_by_program = df.groupby('Program')['Revenue'].sum().reset_index()

            # Plan future programs
            city_program_count = df.groupby(['City', 'Program']).size().reset_index(name='Count')
            future_dates = [dt.date.today() + dt.timedelta(days=30*i) for i in range(1, 4)]
            future_plan = []
            for city in df['City'].unique():
                for program in df['Program'].unique():
                    for date in future_dates:
                        future_plan.append({'City': city, 'Program': program, 'Date': date})
            future_plan_df = pd.DataFrame(future_plan)

            # Display dataframes
            st.header("Revenue by City")
            st.dataframe(revenue_by_city)

            st.header("Revenue by Program")
            st.dataframe(revenue_by_program)

            st.header("Future Training Program Plan")
            st.dataframe(future_plan_df)

            # Display current pricing
            st.header("Current Pricing")
            st.write(f"Practitioners Program: ₹{practitioners_price}")
            st.write(f"Masters Program: ₹{masters_price}")
        else:
            st.error("The uploaded Excel file does not have the expected columns. Please check the format information above.")
            
if __name__ == "__main__":
    main()
