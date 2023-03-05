import pandas
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit 
import seaborn as sns
import scipy.signal as signal

# function that reads the csv file, aggregates the data, creates two plots: melting curve and derivative plot
def create_dsf_graphs(filename):

    # reading the csv and saving as a variable
    df = pandas.read_csv(filename)
    
    # grouping the data by three columns: 
    # 1. Sample Position to track which well, then the 2. temperature and 3. fluroescence of each well
    new_df = df.groupby('SamplePos')['Temp', '465-580'].agg(list)

    # using a dictionary to create the x-axis for our melting curve
    melting_curve_data = {'Temperature Celsius': new_df.iloc[0, 0]}

    # looping through the rows of the data frame 
    for index, row in new_df.iterrows():

        # ensuring that the length of the fluorescence column is the same as the length of our temperature column
        if len(row['465-580']) == len(row['Temp']):
            melting_curve_data[row.name] = row['465-580']

    # making the melting curve x-axis a dataframe
    melting_curve_df = pandas.DataFrame(melting_curve_data)

    # creating a variable that selects position [0,0] in our dataframe as temp
    temp = new_df.iloc[0, 0]
    
    # copying the aggregated data
    melting_curve_df_scaled = melting_curve_df.copy()

    # apply normalization techniques
    for column in melting_curve_df_scaled.iloc[:,2:]:
        melting_curve_df_scaled[column] = melting_curve_df_scaled[column]  / melting_curve_df_scaled[column].abs().max()


    # going through each row one by one, saving as a variable
    all_wells = list(melting_curve_df.columns)[1::]

    #dRdt = np.gradient(melting_curve_df, temp)

    # using a dictionary to create the x-axis for our derivative plot
    derivative_data = {'Temperature Celsius': new_df.iloc[0, 0][1::]}

    # looping through all the wells
    for i in all_wells[1::]:

        # creating an emtpy derivative list that'll have derivative values appended to it later
        derivative = []

        # looping through the enumerated melting curve dataframe to calculate the derivative 
        for j, val in enumerate(melting_curve_df[i][1::]):

            # ensure that infinity doesn't occur
            if (temp[j+1] - temp[j]) != 0:
                
                # as long as the current temp minus the previous temp isn't zero, calculate and add the derivative 
                derivative.append((val - melting_curve_df[i][j]) / (temp[j+1] - temp[j]))
            
            # if there's a 0 during subtraction
            else:

                # the derivative is the 
                derivative.append(derivative[j-1])

        # setting the derivative data equal to our derivative list 
        derivative_data[i] = derivative


    # creating a derivative dataframe 
    derivative_df = pandas.DataFrame(derivative_data)

    # apply normalization techniques
    for column in derivative_df.iloc[:,2:]:
        derivative_df[column] = derivative_df[column]  / derivative_df[column].abs().max()

    

    # plotting our melting curve
    melting_curve_plot = melting_curve_df_scaled.plot(x='Temperature Celsius',
                                  y=['B2','D2','E2'],
                                  kind='line',
                                  legend=True,
                                  label=['20µL Cas9','18µL Cas9','16µL Cas9'],
                                  linewidth=1)
    melting_curve_plot.set_ylabel('Normalized RFU')
    melting_curve_plot.set_xlabel('Temperature (°C)')

    # plotting our derivative plot
    derivative_plot = derivative_df.plot(x='Temperature Celsius',
                                    y=['B2','D2','E2'],
                                    kind='line',
                                    legend=True,
                                    label=['20µL Cas9','18µL Cas9','16µL Cas9'],
                                    linewidth=0.5)
    derivative_plot.set_ylabel('dRFU/dt')
    derivative_plot.set_xlabel('Temperature (°C)')

