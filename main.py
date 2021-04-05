import sys, subprocess
import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import date
from datetime import datetime
import urllib3


def main():
    urls = requests.get("https://filesstaticpulzo.s3-us-west-2.amazonaws.com/pulzo-lite/jsons/admin/bd_report_webvitals.json")
    urls = urls.json()
    i=2
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
    if url[len(url)-1] !='/':
        url =url+'/'
    info = apis(url,strategy)
    if info != None:        
      conexionDoc(indexPag, 'A', i, nombre)
      conexionDoc(indexPag, 'B', i, url)
      conexionDoc(indexPag, 'C', i, str(date.today()))
      conexionDoc(indexPag, 'D', i, tipo)
      conexionDoc(indexPag, 'E', i, info['first-contentful-paint']['displayValue'])
      conexionDoc(indexPag, 'F', i, info['speed-index']['displayValue'])
      conexionDoc(indexPag, 'G', i, info['interactive']['displayValue'])
      conexionDoc(indexPag, 'H', i, info['first-meaningful-paint']['displayValue'])
      conexionDoc(indexPag, 'I', i, info['first-cpu-idle']['displayValue'])
      conexionDoc(indexPag, 'J', i, info['estimated-input-latency']['displayValue'])

def apis(url,type):
    x = 'https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=https://'+url+type+'&key=AIzaSyAwMEAQbR1OM6aoHpGiT0W42K2hlDnRJ5c' 
    f= requests.get(x)
    s=f.json()
    if 'lighthouseResult' in s:
        return s['lighthouseResult']['audits']

def conexionDoc(indexPag, col, row, data):
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    # add credentials to the account
    creds = ServiceAccountCredentials.from_json_keyfile_name('/home/ubuntu/apps/belladurmiente/BellaDurmiente-bc8549c7c1c7.json', scope)
    # authorize the clientsheet 
    client = gspread.authorize(creds)
    # get the instance of the Spreadsheet
    sheet = client.open('BaseDatosReportes')
    # get the first sheet of the Spreadsheet
    sheet_instance = sheet.get_worksheet(indexPag)
    sheet_instance.update_acell(col+str(row),data)

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
