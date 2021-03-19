import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import date
from datetime import datetime
import urllib3

class Report():
    def __init__(self):
        self.http = urllib3.PoolManager()
        self.dfpAds = True
    def main(self):
        urls = requests.get("https://filesstaticpulzo.s3-us-west-2.amazonaws.com/pulzo-lite/jsons/admin/bd_report_webvitals.json")
        urls = urls.json()
        i=2
        if 'pruebas' in urls:
            for tipo in urls['pruebas']:
                if tipo['nombre'] == "home":
                    indexPag = 0
                    i = self.index(indexPag)
                    for dis in tipo['dispositivos']:
                        for portales in tipo['portales']:
                            self.writeSheet(portales['nombre'], portales['url'], dis, i, indexPag)
                            i=i+1
                if tipo['nombre'] == "Articulos":
                    indexPag = 1
                    i = self.index(indexPag)
                    for dis in tipo['dispositivos']:
                        for portales in tipo['portales']:
                            self.writeSheet(portales['nombre'], portales['url'], dis, i, indexPag)
                            i=i+1
                if tipo['nombre'] == "AMP":
                    indexPag = 2
                    i = self.index(indexPag)
                    for dis in tipo['dispositivos']:
                        for portales in tipo['portales']:
                            self.writeSheet(portales['nombre'], portales['url'], dis, i, indexPag)
                            i=i+1
    def writeSheet(self, nombre, url, tipo, i,indexPag):
        if tipo=='mobile':
            strategy ='&strategy=mobile'
        else :
            strategy = ''
        if url[len(url)-1] !='/':
            url =url+'/'
        info = self.apis(url,strategy)
        self.conexionDoc(indexPag, 'A', i, nombre)
        self.conexionDoc(indexPag, 'B', i, url)
        self.conexionDoc(indexPag, 'C', i, str(date.today()))
        self.conexionDoc(indexPag, 'D', i, tipo)
        self.conexionDoc(indexPag, 'E', i, info['first-contentful-paint']['displayValue'])
        self.conexionDoc(indexPag, 'F', i, info['speed-index']['displayValue'])
        self.conexionDoc(indexPag, 'G', i, info['interactive']['displayValue'])
        self.conexionDoc(indexPag, 'H', i, info['first-meaningful-paint']['displayValue'])
        self.conexionDoc(indexPag, 'I', i, info['first-cpu-idle']['displayValue'])
        self.conexionDoc(indexPag, 'J', i, info['estimated-input-latency']['displayValue'])

    def apis(self, url,type):
        x = 'https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=https://'+url+type+'&key=AIzaSyAwMEAQbR1OM6aoHpGiT0W42K2hlDnRJ5c' 
        f= requests.get(x)
        s=f.json()
        return s['lighthouseResult']['audits']

    def conexionDoc(self, indexPag, col, row, data):
        scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
        # add credentials to the account
        creds = ServiceAccountCredentials.from_json_keyfile_name('BellaDurmiente-bc8549c7c1c7.json', scope)
        # authorize the clientsheet 
        client = gspread.authorize(creds)
        # get the instance of the Spreadsheet
        sheet = client.open('BaseDatosReportes')
        # get the first sheet of the Spreadsheet
        sheet_instance = sheet.get_worksheet(indexPag)
        sheet_instance.update_acell(col+str(row),data)

    def index(self, page):
        scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
        # add credentials to the account
        creds = ServiceAccountCredentials.from_json_keyfile_name('BellaDurmiente-bc8549c7c1c7.json', scope)
        # authorize the clientsheet 
        client = gspread.authorize(creds)
        # get the instance of the Spreadsheet
        sheet = client.open('BaseDatosReportes')
        # get the first sheet of the Spreadsheet
        sheet_instance = sheet.get_worksheet(page)
        values_list = sheet_instance.col_values(1)
        return(len(values_list)+1)

