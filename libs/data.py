import pandas as pd
import folium as fm

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

    df = df.query('(pH >= 0.001) & (pH < 14) & (OD >= 0.01) & (OD < 100) & (K >= 0.07) & (K < 500000)')

    len_after = len(df)

    analysis.update({'A': 'Se analizaron {} mediciones'.format(len_after)})

    if len_before == len_after:
        analysis.update({'B': 'Los datos cumplen con los rangos de medición estándar de las sondas'})

    else:
        analysis.update({'B': 'Se eliminaron {} datos que no cumplen con los rangos de medición de las sondas'.format(
            len_before - len_after)})

    # ANCHOR - Análisis Estadístico

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

    analysis.update({'C': quickTab})

    # ANCHOR - Cumplimiento de Resolución y Objetivos

    data = {}
    for col in df.columns:
        values = []

        for val in df[col]:

            if col == 'pH':
                values.append('✔') if val >= 5 and val <= 9 else values.append('X')

            elif col == 'K':
                values.append('✔') if val >= 0 and val <= 1000 else values.append('X')

            elif col == 'OD':
                values.append('✔') if val >= 4 else values.append('X')

            elif col == 'T':
                values.append('✔') if val >= 4 else values.append('X')

            else:
                values.append('*')

        data[col] = values

    table = pd.DataFrame(data)

    verif = []
    for row in range(table.shape[0]):

        i = 0
        for col in range(table.shape[1]):

            if table.values[row, col] == '✔': i += 1

        verif.append('✔') if i == 4 else verif.append('X')

    tabVerif = table.assign(Cumplimiento=verif)

    analysis.update({'D': tabVerif})

    # ANCHOR - Porcentaje de cumplimiento por variable

    data = {}
    for col in df.columns[2:6]:
        count = (table[col].value_counts() / table[col].count()) * 100
        data[col] = count

    tabCount = pd.DataFrame(data).fillna(0).astype('float')

    for row in range(tabCount.shape[0]):

        i = 0
        for col in range(tabCount.shape[1]):
            tabCount.values[row, col] == tabCount.values[row, col] * 100 / len_after
            i += 1

    analysis.update({'E': tabCount})

    # ANCHOR - Porcentaje de cumplimiento total

    tabTotal = pd.DataFrame(tabVerif['Cumplimiento'].value_counts(normalize=True) * 100)
    tabTotal.columns = ['% Cumplimiento Total']

    analysis.update({'F': tabTotal})

    # ANCHOR - Mapa del recorrido

    lat = df['Lat'].tolist()
    lng = df['Lng'].tolist()

    # i = 0
    # for dato in lat:
    #     dec, ent = math.modf(dato)
    #     if dec < 0.76:
    #         num = ent + (dec + (0.76 - round(dec, 2)))
    #         lat[i] = num
    #     i += 1
    #
    # i = 0
    # for dato in lng:
    #     dec, ent = math.modf(dato)
    #     if abs(dec) > 0.109:
    #         num = ent + (dec + (abs(dec) - 0.109))
    #         lng[i] = num
    #     i += 1

    if lat[0] != 0 and lng[0] != 0:
        loc = [sum(lat) / len(lat), sum(lng) / len(lng)]

    else:
        loc = [4.6311086, -78.8356402]

    m = fm.Map(location=loc, zoom_start=14)

    for i in range(len_after):

        if lat[0] != 0 and lng[0] != 0:

            if verif[i] == '✔':
                colCirc = 'darkgreen'
                colLine = 'mediumseagreen'
            else:
                colCirc = 'darkred'
                colLine = 'crimson'

            if i == 0:
                fm.Marker([lat[0], lng[0]], icon=fm.Icon(color='darkblue'), tooltip='Inicio').add_to(m)

            elif i == len_after - 1:

                fm.Circle((lat[i], lng[i]), radius=1, color=colCirc).add_to(m)

                fm.PolyLine([[lat[i - 1], lng[i - 1]], [lat[i], lng[i]]], color=colLine).add_to(m)

                fm.Marker([lat[i], lng[i]], icon=fm.Icon(color='darkblue'), tooltip='Final').add_to(m)

            else:
                fm.Circle((lat[i], lng[i]), radius=1, color=colCirc).add_to(m)

                fm.PolyLine([[lat[i - 1], lng[i - 1]], [lat[i], lng[i]]], color=colLine).add_to(m)

    m.save('templates/map.html')

    return analysis
