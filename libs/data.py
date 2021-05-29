import pandas as pd

def dataAnalysis(datafile):

    ''' Módulo que permite realizar el análisis de las mediciones de variables físicoquimicas de la calidad del agua '''

    # ANCHOR - Inicio del Programa Principal

    analysis = {}
    headers = ('Timestamp', 'ID', 'pH', 'K', 'OD', 'T', 'Lat', 'Lng', 'Alt', 'Lat_Ch', 'Lng_Ch', 'Alt_Ch', 'Status')

    df = pd.read_csv(datafile)

    if len(df.columns) == 9:
        df.columns = headers[0:9]
    else:
        df.columns = headers

    df['Timestamp'] = pd.to_datetime(df['Timestamp'])

    len_before = len(df)

    df = df.query('(pH >= 0) & (pH < 14) & (OD >= 0) & (OD < 100) & (K >= 0) & (K < 200000)')

    len_after = len(df)

    if len_before == len_after :
        analysis.update({'A': 'Los datos cumplen con los rangos de medición estándar de las sondas'})

    else:
        analysis.update({'A': 'Se eliminaron {} datos que no cumplen con los rangos de medición de las sondas'.format(len_before-len_after)})


    data = {}
    for col in df.columns[2:6]:
        
        values = [
            round(df[col].max(), 3),
            round(df[col].min(), 3),
            round(df[col].mean(), 3),
            round(df[col].median(), 3),
            round(df[col].std(), 3)
        ]

        data[col] = values

    quickTab = pd.DataFrame(data, index=['Max', 'Min', 'Med', 'Mdna', 'Desv.Est'])

    analysis.update({'B': quickTab})


    data = {}
    for col in df.columns:
        values = []
        count = []

        for val in df[col]:

            if col == 'pH':
                values.append('✔') if val>=5 and val<=9 else values.append('X')
            
            elif col == 'K':
                values.append('✔') if val>=0 and val<=1000 else values.append('X')
            
            elif col == 'OD':
                values.append('✔') if val>=4 else values.append('X')
            
            elif col == 'T':
                values.append('✔') if val>=4 else values.append('X')
            
            else:
                values.append('*')

        data[col] = values
        
    table = pd.DataFrame(data)

    verif = []
    for row in range(table.shape[0]):

        i = 0
        for col in range(table.shape[1]):

            if table.values[row, col] == '✔': i+=1

        verif.append('✔') if i==4 else verif.append('X')

    tabVerif = table.assign(Cumplimiento = verif)

    analysis.update({'C': tabVerif})

    data = {}
    for col in df.columns[2:6]:

        count = (table[col].value_counts()/table[col].count()) * 100
        data[col] = count

    tabCount = pd.DataFrame(data).fillna(0).astype('float')

    for row in range(tabCount.shape[0]):

        i = 0
        for col in range(tabCount.shape[1]):

            tabCount.values[row, col] == tabCount.values[row, col] * 100 / len_after
            i+=1

    analysis.update({'D': tabCount})


    tabTotal = pd.DataFrame(table['Cumplimiento'].value_counts(normalize=True) * 100)
    tabTotal.columns = ['% Cumplimiento Total']

    analysis.update({'E': tabTotal})


    return analysis