def findPeaks(data, n = 500) :
    
    #print(data)

    df = pd.DataFrame(data)
    dataName = df.columns.values[0]

    #print(dataName)

    '''for i in range(len(df[dataName])) :
        if abs(df.at[i+1, dataName]) <= 25 :
            df.at[i, dataName] = 0'''

    #print(df)

    minIndexes = argrelextrema(df[dataName].values, np.less, order=n)[0]
    maxIndexes = argrelextrema(df[dataName].values, np.greater, order=n)[0]

    #print(minIndexes)

    for i in range(len(minIndexes)) : 
        index = minIndexes[i]
        if abs(df.at[index, dataName]) >= 5 :
            print(df.at[index, dataName])
            #input()
            np.delete(minIndexes, i)

    df['min'] = df.iloc[minIndexes][dataName]
    df['max'] = df.iloc[maxIndexes][dataName]

    return df

    #print(df['min'])

def derivative(df) :

    df['Horodate'] = pd.to_datetime(df['Date de prélèvement'] + ' ' + df['Heure de prélèvement'])
    df['dT'] = df['Horodate'].diff()
    df['dX'] = df['DEBIT_ENTREE (m3/h)'].diff()
    df.drop(index = 0, axis = 0, inplace=True)
    df['dT'] = df['dT'].dt.total_seconds()
    df['dX/dT'] = df['dX']/ df['dT']

    return df