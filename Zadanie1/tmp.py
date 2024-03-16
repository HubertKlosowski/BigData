import pandas as pd
import requests
from bs4 import BeautifulSoup
import gspread
import numpy as np


def web_scrape(url, table_class):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    indiatable = soup.find('table', {'class': table_class})
    dataframe = pd.read_html(str(indiatable))
    return pd.DataFrame(dataframe[0])


def prepare_currencies(dataframe):
    dataframe.dropna(inplace=True)
    dataframe['Country'] = dataframe['Country'].str.title()  # tylko pierwsza litera z dużej
    dataframe['Country'] = dataframe['Country'].apply(lambda x: x.split(' (')[0])  # usuń zbędne znaki
    dataframe.drop(['Number'], axis=1, inplace=True)  # usunięcie zbędnej kolumny
    dataframe['Country'] = dataframe['Country'].str.split(', ')  # rozbicie wierszy na poszczególne kraje
    dataframe = dataframe.explode('Country')
    dataframe.loc[dataframe['Country'] == 'Russian Federation', 'Country'] = 'Russia'
    dataframe.loc[dataframe['Country'] == 'Republic Of North Macedonia', 'Country'] = 'Macedonia'
    dataframe.loc[dataframe['Country'] ==
                  'United Kingdom Of Great Britain And Northern Ireland', 'Country'] = 'United Kingdom'
    # dataframe.to_csv('czesc7/world_curriencies.csv', index=False)
    return dataframe


def update_sheets():
    for i, el in enumerate(curr):
        worksheet = sh.add_worksheet(title=f'{el}', rows=1827, cols=26, index=i)
        worksheet.update_cell(1, 1, f'=GOOGLEFINANCE("{el}"; "price"; DATE(2019;1;1); DATE(2024;1;1))')


def get_sheets_data():
    sheets = [sh.worksheet(el) for el in curr]
    result = pd.DataFrame()
    for sheet in sheets:
        data = sheet.get_values()[1:]
        sheet_data = pd.DataFrame(data, columns=['date', sheet.title])
        sheet_data['date'] = pd.to_datetime(sheet_data['date']).dt.date
        result = sheet_data if result.empty else result.merge(sheet_data, on='date', how='outer')
    # result.to_csv('czesc7/currency_data.csv', index=False)
    return result


def del_worksheets():
    sheets = [sh.worksheet(el) for el in curr]
    for sheet in sheets:
        sh.del_worksheet(sheet)


gc = gspread.service_account()
sh = gc.open("Currencies")

world_currencies = web_scrape('https://www.iban.com/currency-codes', 'table table-bordered downloads tablesorter')
europe_countries = ['Albania', 'Andorra', 'Austria', 'Belarus', 'Belgium', 'Bosnia And Herzegovina', 'Bulgaria',
                    'Croatia', 'Cyprus', 'Czech Republic', 'Denmark', 'Estonia', 'Finland', 'France', 'Germany',
                    'Greece', 'Hungary', 'Iceland', 'Ireland', 'Italy', 'Latvia', 'Liechtenstein', 'Lithuania',
                    'Luxembourg', 'Macedonia', 'Malta', 'Moldova', 'Monaco', 'Montenegro',
                    'Netherlands', 'Norway', 'Poland', 'Portugal', 'Romania', 'Russia', 'San Marino',
                    'Serbia', 'Slovakia', 'Slovenia', 'Spain', 'Sweden', 'Switzerland', 'Ukraine', 'United Kingdom']

world_currencies = prepare_currencies(world_currencies)
world_currencies = world_currencies[world_currencies['Country'].isin(europe_countries)].reset_index(drop=True)
world_currencies.drop(index=[41, 43], inplace=True)  # 2 waluty z Szwajcarii nie rozpoznawane są
world_currencies.reset_index(drop=True, inplace=True)

curr = world_currencies['Code'].unique().tolist()
curr = ['USD' + el for el in curr]
update_sheets()
currencies_data = get_sheets_data()
del_worksheets()

currencies_data = currencies_data.ffill(axis=1)
currencies_data['date'] = pd.to_datetime(currencies_data['date'])
convert = [col for col in currencies_data.columns if 'USD' in col]
for col in convert:
    currencies_data[col] = currencies_data[col].str.replace(',', '.')
    currencies_data[col] = currencies_data[col].astype(np.float64)

gasoline_UK = pd.read_excel('czesc7/Weekly_Gasoline_Prices_UK.xlsx')
gasoline_UK.rename(columns={'Date': 'date', 'ULSP:  Pump price (p/litre)': 'UK Gasoline Prices $/litre'}, inplace=True)
gasoline_UK = pd.merge(gasoline_UK, currencies_data[['date', 'USDGBP']], on='date', how='inner')
gasoline_UK['UK Gasoline Prices $/litre'] = gasoline_UK['UK Gasoline Prices $/litre'] / gasoline_UK['USDGBP']
gasoline_UK['UK Gasoline Prices $/litre'] = gasoline_UK['UK Gasoline Prices $/litre'].apply(lambda x: round(x, 2))
gasoline_UK.drop(['USDGBP'], axis=1, inplace=True)
gasoline_UK.to_csv('czesc7/xd.csv', index=False)
