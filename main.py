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
global urlpage

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
    datas = apis(url,strategy)
    performance = datas[1]
    info = datas[0]
    fecha = date.today().strftime('%Y-%m-%d')
    if info != None:      
      data = [nombre,url,fecha,tipo, float(info['first-contentful-paint']['displayValue'].replace('s', '').strip()),float(info['speed-index']['displayValue'].replace('s', '').strip()), float(info['interactive']['displayValue'].replace('s', '').strip()), float(info['first-meaningful-paint']['displayValue'].replace('s', '').strip()), float(info['total-blocking-time']['displayValue'].replace(',', '').replace('ms', '').strip()), float(info['cumulative-layout-shift']['displayValue'].replace(',', '').strip()), float(info['largest-contentful-paint']['displayValue'].replace(',', '').replace('s', '').strip()), float(info['max-potential-fid']['displayValue'].replace(',', '').replace('ms', '').strip()), (performance*100)]  
      conexionDoc(indexPag, i, data)
    

def apis(url,tipo):
    key= config['DEFAULT']['KEY']
    x = 'https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=https://'+url+tipo+'&key='+key 
    print(x)
    f= requests.get(x, timeout=(500,500))
    s=f.json()
    if 'lighthouseResult' in s:
        return s['lighthouseResult']['audits'], s['lighthouseResult']['categories']['performance']['score']

def conexionDoc(indexPag, row, data):
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    # add credentials to the account
    creds = ServiceAccountCredentials.from_json_keyfile_name('/home/ubuntu/apps/belladurmiente/BellaDurmiente-bc8549c7c1c7.json', scope)
    # authorize the clientsheet 
    client = gspread.authorize(creds)
    # get the instance of the Spreadsheet
    sheet = client.open(urlpage)
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
    sheet = client.open(urlpage)
    # get the first sheet of the Spreadsheet
    sheet_instance = sheet.get_worksheet(page)
    values_list = sheet_instance.col_values(1)
    return(len(values_list)+1)



if len(sys.argv) == 2:
    urlpage = sys.argv[1]
    main()
else:
    print("Error - Introduce los argumentos correctamente")