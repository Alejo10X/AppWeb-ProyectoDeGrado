import numpy as np
import pandas as pd
import folium as fm
import branca as br

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

    analysis.update({'A': 'Se analizaron {} mediciones'.format(len_after)})

    if len_before == len_after:
        analysis.update({'B': 'todas cumplen con los rangos de medición de cada una de las sondas implementadas en el sistema.'})

    else:
        analysis.update({'B': 'se eliminaron {} que no cumplen con los rangos de medición de cada una de las sondas implementadas en el sistema.'.format(len_before - len_after)})

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

    try:
        quickTab = quickTab.rename_axis(['Estadísticas']).reset_index()
        quickTab['Estadísticas'] = np.where(quickTab['Estadísticas'].duplicated(), '', quickTab['Estadísticas'])

    except:
        None

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

    try:
        tabCount = tabCount.rename_axis(['Calificación']).reset_index()
        tabCount['Calificación'] = np.where(tabCount['Calificación'].duplicated(), '', tabCount['Calificación'])

    except:
        None

    analysis.update({'E': tabCount})

    # ANCHOR - Porcentaje de cumplimiento total

    tabTotal = pd.DataFrame(tabVerif['Cumplimiento'].value_counts(normalize=True) * 100)
    tabTotal.columns = ['% Cumplimiento Total']

    try:
        tabTotal = tabTotal.rename_axis(['Calificación']).reset_index()
        tabTotal['Calificación'] = np.where(tabTotal['Calificación'].duplicated(), '', tabTotal['Calificación'])

    except:
        None

    analysis.update({'F': tabTotal})

    # ANCHOR - Mapa del recorrido

    lat = df['Lat'].tolist()
    lng = df['Lng'].tolist()

    legend = br.element.MacroElement()
    legend._template = br.element.Template(
        '''
        {% macro html(this, kwargs) %}

        <div style="
            position: fixed;
            bottom: 10px;
            left: 10px;
            width: 180px;
            height: 66px;
            z-index:9998;
            font-size:14px;
            background-color: #ffffff;
            opacity: 1;
            border-radius: 3px;
            box-shadow: 0 1px 5px rgb(0 0 0 / 65%);
            ">

            <p style="margin: 0px;">
                <a style="color:MediumSeaGreen;font-size:150%;margin: 0px 10px;">▬</a> Posible potabilidad
            </p>
            <hr style="margin: 0 auto;">
            <p style="margin: 0px;">
                <a style="color:Crimson;font-size:150%;margin: 0px 10px;">▬</a> Malas condiciones
            </p>

        </div>
        {% endmacro %}
        '''
    )

    if lat[0] != 0 and lng[0] != 0:
        loc = [sum(lat) / len(lat), sum(lng) / len(lng)]

    else:
        loc = [5.6311086, -78.8356402]

    m = fm.Map(location=loc, zoom_start=14)

    for i in range(len_after):

        popup = '''
            <h5 style="text-align: center;"><b>Datos del Tramo</b></h5>
            
            <hr style="margin: 4px auto;">
            <p style="margin: 6px 0;"><b>Fecha/Hora:</b></p>
            <p style="margin: 6px 0;">{}</p>
            <hr style="margin: 4px auto;">

            <p style="margin: 6px 0;"><b>Latitud:</b> {}</p>
            <p style="margin: 6px 0;"><b>Longitud:</b> {}</p>
            <p style="margin: 6px 0;"><b>Altitud:</b> {} msnm</p>

            <hr style="margin: 4px auto;">

            <div style="display: grid; grid-template-columns: 55px 70px 20px; align-items: center;">
                <p style="margin: 6px 0;">▸ <b>pH:</b></p> <p style="margin: 6px 0;">&ensp;{}&ensp;</p>  <b>{}</b>
                <p style="margin: 6px 0;">▸ <b>Cond:</b></p> <p style="margin: 6px 0;">&ensp;{}&ensp;</p>  <b>{}</b>
                <p style="margin: 6px 0;">▸ <b>OD:</b></p> <p style="margin: 6px 0;">&ensp;{}&ensp;</p>  <b>{}</b>
                <p style="margin: 6px 0;">▸ <b>Temp:</b></p> <p style="margin: 6px 0;">&ensp;{}&ensp;</p>  <b>{}</b>
            </div>

            <hr style="margin: 4px auto;">

            <p style="margin: 6px 0; text-align: center;"><b>Resultado:&ensp;{}</p></b>
        '''.format(
            df['Timestamp'][i],
            df['Lat'][i],
            df['Lng'][i],
            df['Alt'][i],
            df['pH'][i],
            tabVerif['pH'][i],
            df['K'][i],
            tabVerif['K'][i],
            df['OD'][i],
            tabVerif['OD'][i],
            df['T'][i],
            tabVerif['T'][i],
            tabVerif['Cumplimiento'][i]
        )

        if lat[0] != 0 and lng[0] != 0:

            if verif[i] == '✔':
                colCirc = 'DarkGreen'
                colLine = 'MediumSeaGreen'

            elif verif[i] == 'X':
                colCirc = 'DarkRed'
                colLine = 'Crimson'

            if i == 0:
                fm.Marker((lat[0], lng[0]), icon=fm.Icon(color='black', icon='play', prefix='fa'),
                          tooltip='Inicio').add_to(m)

            elif i == len_after - 1:

                fm.Circle((lat[i], lng[i]), radius=1, color=colCirc).add_to(m)

                fm.PolyLine([[lat[i - 1], lng[i - 1]], [lat[i], lng[i]]], color=colLine, popup=popup).add_to(m)

                fm.Marker([lat[i], lng[i]], icon=fm.Icon(color='black', icon='stop', prefix='fa'),
                          tooltip='Final').add_to(m)

            else:
                fm.Circle((lat[i], lng[i]), radius=1, color=colCirc).add_to(m)

                fm.PolyLine([[lat[i - 1], lng[i - 1]], [lat[i], lng[i]]], color=colLine, popup=popup).add_to(m)

    m.get_root().add_child(legend)
    m.save('templates/map.html')

    return analysis
