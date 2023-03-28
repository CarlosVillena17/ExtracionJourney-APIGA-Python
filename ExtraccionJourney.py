"""
CREADO POR CARLOS RICARDO VILLENA CABREJOS
"""
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from datetime import datetime
import pandas as pd

UserID_Enero=pd.read_excel("JUNIO.xlsx")
UserIDtengo=pd.read_excel("Journeys (2).xlsx", sheet_name="Enero")
lista_ID=UserID_Enero["userID"].unique().tolist()

creds = Credentials.from_service_account_file('api-python-380220-366fd91b39ae.json')

analytics = build('analyticsreporting', 'v4', credentials=creds)

DF_FINAL = pd.DataFrame(columns=['URL', 'Fecha', 'Pageviews'])
i=0
for userID in lista_ID:
    report = analytics.reports().batchGet(
        body={
            'reportRequests': [
                {
                    'viewId': '242748645',
                    'dateRanges': [{'startDate': '2022-06-01', 'endDate': '2022-06-30'}],
                    'metrics': [{'expression': 'ga:pageviews'}],
                    'dimensions': [{'name': 'ga:pagePath'}, {'name': 'ga:dateHourMinute'}],
                    'dimensionFilterClauses': [
                        {
                            'filters': [
                                {
                                    'dimensionName': 'ga:dimension3',  # Nombre de la dimensión personalizada
                                    'expressions': [userID],  # Valor a comparar
                                    'operator': 'EXACT'  # Operador de comparación
                                }
                            ]
                        }
                    ]
                }]
        }
    ).execute()


    data = []
    for report in report.get('reports', []):
        columnHeader = report.get('columnHeader', {})
        dimensionHeaders = columnHeader.get('dimensions', [])
        metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])
        rows = report.get('data', {}).get('rows', [])

        for row in rows:
            dimensions = row.get('dimensions', [])
            metrics = row.get('metrics', [])
            date_format = '%Y%m%d%H%M'
            datetime_object = datetime.strptime(dimensions[1], date_format)
            formatted_date = datetime_object.strftime('%d/%m/%Y %H:%M:%S')
            data.append([dimensions[0], formatted_date, metrics[0]['values'][0]])

    df = pd.DataFrame(data, columns=['URL', 'Fecha', 'Pageviews'])
    if df.empty == False:
        df['userID']=userID
        DF_FINAL = pd.concat([DF_FINAL, df], ignore_index=True)
        print(userID)
        print(DF_FINAL)
        print("============================")
    else:
        print(userID)


    print(i)
    i=i+1
    if i%100==0:
        print("IMPRIMIENDO JOURNEY")
        DF_FINAL.to_excel('journey_junio.xlsx')
    if i==500:
        DF_FINAL.to_excel('journey_junio.xlsx')

DF_FINAL.to_excel('journey_junio.xlsx')