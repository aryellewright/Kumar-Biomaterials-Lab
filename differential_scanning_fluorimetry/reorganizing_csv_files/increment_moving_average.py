import csv
import numpy as np
import pandas as pd


def temp_bucket(temp):
    return round(temp * 2) / 2

# Averages the data points into half increment buckets
def process_csv(file_path):
    df = pd.read_csv(file_path)
    df['Temp Bucket'] = df['Temp'].apply(lambda x: temp_bucket(x))

    result = df.groupby(['SamplePos', 'Temp Bucket'])[
        '465-580'].mean().reset_index()

    final_result = {}
    for sample_pos, temp_bucket_df in result.groupby('SamplePos'):
        temp_buckets = temp_bucket_df['Temp Bucket'].to_dict()
        avg_flors = temp_bucket_df['465-580'].to_dict()
        final_result[sample_pos] = dict(
            zip(temp_buckets.values(), avg_flors.values()))

    return final_result

# moves data to a moving average
def moving_average(data, range_length):
    # Initialize an empty dictionary to store the moving average results
    moving_avgs = {}
    # Loop over each sample position and its associated temperature buckets and flor values
    for sample_pos, temp_bucket_data in data.items():
        # Get the sorted temperature buckets
        temp_bucket_values = sorted(temp_bucket_data.keys())
        # Get the flor values for each temperature bucket
        flor_values = [temp_bucket_data[val] for val in temp_bucket_values]
        # Compute the moving average using the NumPy `convolve` function
        moving_avg_values = np.convolve(flor_values, np.ones(
            range_length)/range_length, mode='valid')
        # Store the moving average results for this sample position in the `moving_avgs` dictionary
        moving_avgs[sample_pos] = dict(
            zip(temp_bucket_values[range_length-1:], moving_avg_values))

    # Return the moving average results
    return moving_avgs


def write_result_to_csv(result, file_path):
    # Get a list of all the sample positions
    sample_positions = list(result.keys())
    # Get a list of all the temperature buckets
    temp_buckets = set()
    for sample_pos_data in result.values():
        temp_buckets.update(sample_pos_data.keys())
    temp_buckets = sorted(list(temp_buckets))

    # Open the output file
    with open(file_path, 'w', newline='') as f:
        # Create a CSV writer object
        writer = csv.writer(f)
        # Write the header row
        header = [''] + \
            [i for i in sample_positions]
        writer.writerow(header)
        # Loop over each temperature bucket
        for temp_bucket in temp_buckets:
            # Create a list to store the flor values for this temperature bucket
            flor_values = [temp_bucket]
            # Loop over each sample position
            for sample_pos in sample_positions:
                # If this temperature bucket has a flor value for this sample position, add it to the list
                if temp_bucket in result[sample_pos]:
                    flor_values.append(result[sample_pos][temp_bucket])
                # If this temperature bucket doesn't have a flor value for this sample position, add NaN
                else:
                    flor_values.append(np.nan)
            # Write the row for this temperature bucket
            writer.writerow(flor_values)


filename = "20221217_Cas9_AW_RK__new.csv"
i = process_csv(filename)

write_result_to_csv(i, './test_output.csv')
