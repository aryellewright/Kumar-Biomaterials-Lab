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

    # creating a polynomial fitted plot to take the derivative of
    x = np.array(melting_curve_df_scaled['Temperature Celsius']) 

    y_1 = np.array(melting_curve_df_scaled['B2']) 
    y_2 = np.array(melting_curve_df_scaled['D2'])
    y_3 = np.array(melting_curve_df_scaled['E2'])

    # Fit a X degree polynomial to the data
    coeffs_1 = np.polyfit(x, y_1, deg=30)
    coeffs_2 = np.polyfit(x, y_2, deg=30)
    coeffs_3 = np.polyfit(x, y_3, deg=30)

    # Generate the fitted curve
    polynomial_B2 = np.poly1d(coeffs_1)
    polynomial_D2 = np.poly1d(coeffs_2)
    polynomial_E2 = np.poly1d(coeffs_3)

    # creating a new figure 
    plt.figure()

    # Plot the data and the fitted curve
    plt.plot(x, y_1, '-', label='20 µL Cas9')
    plt.plot(x, polynomial_B2(x), '-', label='Fitted Polynomial')

    plt.plot(x, y_2, '-', label='18 µL Cas9')
    plt.plot(x, polynomial_D2(x), '-', label='Fitted Polynomial')

    plt.plot(x, y_3, '-', label='16 µL Cas9')
    plt.plot(x, polynomial_E2(x), '-', label='Fitted Polynomial')
    plt.xlabel('Temperature (°C)')
    plt.ylabel('Normalized RFU')
    plt.legend()
    plt.show()
    # mp.show()

    # plotting our derivative plot of our fitted polynomial
    plt.figure()
    x = np.array(melting_curve_df_scaled['Temperature Celsius']) 
    
    # Evaluate the polynomial at the x values
    y_1 = np.polyval(coeffs_1, x)
    y_2 = np.polyval(coeffs_2, x)
    y_3 = np.polyval(coeffs_3, x)

    # Compute the derivative of the polynomial
    deriv_coeffs_1 = np.polyder(coeffs_1)
    deriv_coeffs_2 = np.polyder(coeffs_2)
    deriv_coeffs_3 = np.polyder(coeffs_3)

    # Evaluate the derivative at the x values
    dy_1 = np.polyval(deriv_coeffs_1, x)
    dy_2 = np.polyval(deriv_coeffs_2, x)
    dy_3 = np.polyval(deriv_coeffs_3, x)

    # Plot the results
    plt.plot(x, y_1, label='20µL Cas9 Polynomial')
    plt.plot(x, dy_1, label='20µL Cas9 Derivative')

    plt.plot(x, y_2, label='18µL Cas9 Polynomial')
    plt.plot(x, dy_2, label='18µL Cas9 Derivative')

    plt.plot(x, y_3, label='16 µL Cas9 Polynomial')
    plt.plot(x, dy_3, label='16µL Cas9 Derivative')

    plt.axhline(0, color='black', lw=0.5)
    plt.legend()
    plt.xlabel('Temperature (°C)')
    plt.ylabel('dRFU/dt')
    plt.show()
