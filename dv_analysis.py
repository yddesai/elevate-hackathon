import pandas as pd

# Load data
file_path = "cases.csv"  # Update with your file path
cases = pd.read_csv(file_path)

# Rename columns for convenience
cases.columns = ["Case Number", "Petitioner Representative", "Respondent Representative", "Restraining Order Issued"]

pet_rep_cases = cases[(cases["Restraining Order Issued"] == "Y") & (cases["Petitioner Representative"] == "Y")]

total_rest_cases = cases[cases["Restraining Order Issued"] == "Y"] 

perc_pet_rep_cases = len(pet_rep_cases) / len(total_rest_cases) * 100

print(f"Percentage of cases with a petitioner representative and a restraining order issued: {perc_pet_rep_cases}%")

pet_rep_cases = cases[(cases["Restraining Order Issued"] == "Y") & (cases["Petitioner Representative"] == "N")]

perc_no_rest_cases = len(pet_rep_cases) / len(total_rest_cases) * 100

print(f"Percentage of cases with no petitioner representative and restraining order issued: {perc_no_rest_cases}%")