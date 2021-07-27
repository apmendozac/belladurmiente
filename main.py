import sys, subprocess
import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import date
from datetime import datetime
import urllib3
import configparser

config = configparser.ConfigParser()
config.read('/home/ubuntu/apps/belladurmiente/config.ini')


def main():
    urls = requests.get("https://filesstaticpulzo.s3-us-west-2.amazonaws.com/pulzo-lite/jsons/admin/bd_report_webvitals.json")
    urls = urls.json()
    if 'pruebas' in urls:
        for tipo in urls['pruebas']:
            if tipo['nombre'] == "home":
                indexPag = 0
                i = index(indexPag)
                for dis in tipo['dispositivos']:
                    for portales in tipo['portales']:
                        writeSheet(portales['nombre'], portales['url'], dis, i, indexPag)
                        i=i+1
            if tipo['nombre'] == "Articulos":
                indexPag = 1
                i = index(indexPag)
                for dis in tipo['dispositivos']:
                    for portales in tipo['portales']:
                        writeSheet(portales['nombre'], portales['url'], dis, i, indexPag)
                        i=i+1
            if tipo['nombre'] == "AMP":
                indexPag = 2
                i = index(indexPag)
                for dis in tipo['dispositivos']:
                    for portales in tipo['portales']:
                        writeSheet(portales['nombre'], portales['url'], dis, i, indexPag)
                        i=i+1
def writeSheet(nombre, url, tipo, i,indexPag):
    if tipo=='mobile':
        strategy ='&strategy=mobile'
    else :
        strategy = ''
    info = apis(url,strategy)
    fecha = date.today().strftime('%Y-%m-%d')
    if info != None:        
      data = [nombre,url,fecha,tipo, info['first-contentful-paint']['displayValue'].replace('s', ''),info['speed-index']['displayValue'].replace('s', ''),info['interactive']['displayValue'].replace('s', ''),info['first-meaningful-paint']['displayValue'].replace('s', ''),info['first-cpu-idle']['displayValue'].replace('s', ''),info['estimated-input-latency']['displayValue'].replace(',', '').replace('ms', '')]  
      conexionDoc(indexPag, i, data)
    

def apis(url,tipo):
    key= config['DEFAULT']['KEY']
    x = 'https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=https://'+url+tipo+'&key='+key 
    print(x)
    f= requests.get(x, timeout=(500,500))
    s=f.json()
    if 'lighthouseResult' in s:
        return s['lighthouseResult']['audits']

def conexionDoc(indexPag, row, data):
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    # add credentials to the account
    creds = ServiceAccountCredentials.from_json_keyfile_name('/home/ubuntu/apps/belladurmiente/BellaDurmiente-bc8549c7c1c7.json', scope)
    # authorize the clientsheet 
    client = gspread.authorize(creds)
    # get the instance of the Spreadsheet
    sheet = client.open('BaseDatosReportes')
    # get the first sheet of the Spreadsheet
    sheet_instance = sheet.get_worksheet(indexPag)
    sheet_instance.insert_row(data, row)
    sheet_instance.update_acell('C'+str(row),data[2])

def index(page):
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    # add credentials to the account
    creds = ServiceAccountCredentials.from_json_keyfile_name('/home/ubuntu/apps/belladurmiente/BellaDurmiente-bc8549c7c1c7.json', scope)
    # authorize the clientsheet 
    client = gspread.authorize(creds)
    # get the instance of the Spreadsheet
    sheet = client.open('BaseDatosReportes')
    # get the first sheet of the Spreadsheet
    sheet_instance = sheet.get_worksheet(page)
    values_list = sheet_instance.col_values(1)
    return(len(values_list)+1)

main()
