import pandas
import matplotlib.pyplot as mp


if __name__ == '__main__':
    data = pandas.read_csv('./raw_data/20221105_N100H100_DSF_new.csv')
    u = data.groupby("SamplePos")["Temp", '465-580'].agg(list)
    aggregated_data = {'Temperature Celsius': u.iloc[0, 0]}

    for index, row in u.iterrows():
        if len(row['465-580']) == len(row['Temp']):
            aggregated_data[row.name] = row['465-580']

    aggregated_data = pandas.DataFrame(aggregated_data)

    derivative_data = {'Temperature Celsius': u.iloc[0, 0][1::]}

    temp = u.iloc[0, 0]

    all_samples = list(aggregated_data.columns)[1::]

    for i in all_samples[1::]:
        derivative = []
        for j, val in enumerate(aggregated_data[i][1::]):
            if (temp[j+1] - temp[j]) != 0:
                derivative.append((val - aggregated_data[i][j]) / (temp[j+1] - temp[j]))
            else:
                derivative.append(derivative[j-1])
        derivative_data[i] = derivative

    derivative_data = pandas.DataFrame(derivative_data)

    # plot_2 = derivative_data.plot(x='Temperature Celsius',
    #                               y=list(derivative_data.columns[1::]),
    #                               kind='line',
    #                               legend=False,
    #                               linewidth=0.1)
    # plot_2.set_ylabel('dRU/dt')

    plot_1 = aggregated_data.plot(x='Temperature Celsius',
                                  y=list(aggregated_data.columns)[1::],
                                  kind='line',
                                  legend=False,
                                  linewidth=1)
    plot_1.set_ylabel('RFU')

    mp.show()
