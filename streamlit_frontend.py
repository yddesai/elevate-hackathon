import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


def load_data(file_path):
    try:
        data = pd.read_csv(file_path)
        return data
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

def main():
    st.title("Domestic Violence Data Retrieval and Analysis")
    
    # File upload
    uploaded_file = st.file_uploader("Upload CSV", type=["csv"])
    
    if uploaded_file is not None:
        # Load data
        docket_data = load_data(uploaded_file)
        
        if docket_data is not None:
            # Display paginated table
            st.write("Docket Table")
            docket_data.columns = ["Case Number", "Petitioner Representative", "Respondent Representative", "Restraining Order Issued"]
            page_size = st.sidebar.slider("Select number of rows per page", min_value=1, max_value=len(docket_data), value=10)
            page_number = st.sidebar.number_input("Go to page", min_value=1, max_value=len(docket_data)//page_size + 1, value=1)
            start_index = (page_number - 1) * page_size
            end_index = min(start_index + page_size, len(docket_data))
            st.table(docket_data[start_index:end_index].reset_index(drop=True))
            st.sidebar.write(f"Showing rows {start_index + 1} to {end_index} of {len(docket_data)}")

        # histogram 
        file_path = "cases.csv"  # Update with your file path
        cases = pd.read_csv(file_path)

        # Rename columns for convenience
        cases.columns = ["Case Number", "Petitioner Representative", "Respondent Representative", "Restraining Order Issued"]

        cases.columns = ["Case Number", "Petitioner Representative", "Respondent Representative", "Restraining Order Issued"]
            
        # Calculate percentages
        pet_rep_with_restraining_order = len(cases[(cases["Petitioner Representative"] == "Y") & (cases["Restraining Order Issued"] == "Y")])
        no_pet_rep_with_restraining_order = len(cases[(cases["Petitioner Representative"] == "N") & (cases["Restraining Order Issued"] == "Y")])
        total_cases_with_restraining_order = len(cases[cases["Restraining Order Issued"] == "Y"])

        # Calculate percentages
        perc_pet_rep_with_restraining_order = (pet_rep_with_restraining_order / total_cases_with_restraining_order) * 100
        perc_no_pet_rep_with_restraining_order = (no_pet_rep_with_restraining_order / total_cases_with_restraining_order) * 100

        # Plotting the histogram
        labels = ['Petitioner Representative', 'No Petitioner Representative']
        percentages = [perc_pet_rep_with_restraining_order, perc_no_pet_rep_with_restraining_order]

        # Display histogram
        st.bar_chart(percentages)
        
        # Display the percentage values
        st.write(f"Percentage of cases with a petitioner representative that got a restraining order: {perc_pet_rep_with_restraining_order:.2f}%")
        st.write(f"Percentage of cases without a petitioner representative that got a restraining order: {perc_no_pet_rep_with_restraining_order:.2f}%")
# Main function to run the app



if __name__ == "__main__":
    main()
