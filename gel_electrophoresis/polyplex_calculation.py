
# Define a function to calculate the amount of polymer and pDNA needed to achieve a desired N/P ratio
def calculate_polymer_and_pDNA_amounts(NP_ratio, polymer_equivalence, polymer_weight_per_equivalence, polymer_volume):
    """Calculates the amount of polymer and pDNA needed to achieve the desired N/P ratio.
    Args:
    NP_ratio (float): The desired N/P ratio.
    polymer_equivalence (float): The amount of polymer needed per nucleotide of pDNA.
    polymer_weight_per_equivalence (float): The weight of polymer per equivalence.
    polymer_volume (float): The volume of polymer in microliters.
    Returns:
    tuple: The amount of polymer and pDNA needed in micrograms.
    """
    # Calculate the total number of equivalents of polymer needed based on the polymer volume and weight per equivalence
    total_equivalents = polymer_volume * polymer_weight_per_equivalence / polymer_equivalence
    
    # Calculate the amount of pDNA needed based on the N/P ratio and total equivalents of polymer
    pDNA_amount = total_equivalents / NP_ratio
    
    # Calculate the amount of polymer needed based on the polymer equivalence and amount of pDNA
    polymer_amount = pDNA_amount * polymer_equivalence
    
    # Return the amounts of polymer and pDNA in micrograms
    return (polymer_amount, pDNA_amount)

# Example usage of the function
# Calculate the amounts of p(DMAEMA) and pDNA needed for an N/P ratio of 2, with 140 equivalence of p(DMAEMA) per nucleotide of pDNA and 10 microliters of p(DMAEMA)
polymer_amount, pDNA_amount = calculate_polymer_and_pDNA_amounts(5, 140, 16.12, 10)
print(f"Add {polymer_amount} micrograms of p(DMAEMA) and {pDNA_amount} micrograms of pDNA for an N/P ratio of 2.")
