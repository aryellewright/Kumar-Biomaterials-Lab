import pandas as pd

# Read the input CSV file
df = pd.read_csv("/Users/aryellewright/Documents/Kumar-Biomaterials-Lab/differential_scanning_fluorimetry/raw_data/20221217_Cas9_trial_AW_RK.csv")

# Select the desired wells
wells = ['B2','C2','D2','E2','F2','G2','B3','C3','D3','E3','F3','G3','D4','E4','F4','G4']

# Pivot the data to convert the rows to columns
pivoted = pd.pivot_table(df[df.SamplePos.isin(wells)], index=["Temp"], columns=["SamplePos"], values=["465-580"])

# Rename the columns to remove the top level
pivoted.columns = pivoted.columns.droplevel()

# Write the output to a new CSV file
pivoted.to_csv("output.csv", index_label="Temperature")

