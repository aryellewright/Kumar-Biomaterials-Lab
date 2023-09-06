# Define the concentration of the polymer stock solution
polymer_stock_concentration = 1  # µg/µL

# Define the concentration of the pDNA stock solution
pDNA_stock_concentration = 5.37  # µg/µL

# Define the desired N/P ratio
desired_NP_ratio = 5

# Define the amount of pDNA stock solution to use
pDNA_volume = 100  # µL

# Calculate the amount of pDNA in micrograms
pDNA_amount = pDNA_volume * pDNA_stock_concentration

# Calculate the amount of polymer needed in micrograms
polymer_amount = desired_NP_ratio * pDNA_amount

# Calculate the volume of polymer stock solution needed in microliters
polymer_volume = polymer_amount / polymer_stock_concentration

print(f"Add {polymer_volume} µL of the polymer stock solution to {pDNA_volume} µL of pDNA stock solution for an N/P ratio of {desired_NP_ratio}.")
