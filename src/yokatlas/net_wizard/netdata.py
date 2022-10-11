from selenium.webdriver.common.by import By
from src.datatable import DatatableScrapper as Scrapper
from bs4 import BeautifulSoup
from datetime import datetime
import re

class NetdataScrapper(Scrapper):

    def __init__(self, url, dtId, delay, perPage):
        super().__init__(url, dtId, delay, perPage)

    def format(self, extra_fields = False):
        formatted = []
        for index, cols in enumerate(self.data):
            formattedData = self.formatRecursively(index, cols, extra_fields)
            formatted.append(formattedData)
            print('(' + formattedData['bolum_turu'].upper() + ') Formatted ' + str(index) + ': ' + formattedData['yop_kodu'] + ' - ' + BeautifulSoup(cols[1], 'html.parser').a.get_text())
        return formatted

    def formatRecursively(self, index, cols, extra_fields = False):
        department_type = re.findall(r'\((SAY|SÖZ|EA|DİL|TYT)\)', self.title)[0]
        try:
            formattedData = {
                'yop_kodu' : BeautifulSoup(cols[1], 'html.parser').find_all('a')[0].get('href').replace('lisans.php?y=',''),
                'yil' : BeautifulSoup(cols[2], 'html.parser').get_text(),
                'katsayi': BeautifulSoup(cols[4], 'html.parser').get_text(),
                'yerlesen_son_kisi_obp': BeautifulSoup(cols[5], 'html.parser').get_text(),
                'yerlesen_kisi_sayisi': BeautifulSoup(cols[6], 'html.parser').get_text(),
                'bolum_turu': department_type,
                'tyt' : {
                    'turkce': BeautifulSoup(cols[7],'html.parser').get_text(),
                    'sosyal': BeautifulSoup(cols[8],'html.parser').get_text(),
                    'matematik': BeautifulSoup(cols[9],'html.parser').get_text(),
                    'fen': BeautifulSoup(cols[10],'html.parser').get_text()
                }
            }
            if formattedData['bolum_turu'] == 'SAY':
                formattedData['ayt'] = {
                    'matematik': BeautifulSoup(cols[11],'html.parser').get_text(),
                    'fizik': BeautifulSoup(cols[12],'html.parser').get_text(),
                    'kimya': BeautifulSoup(cols[13],'html.parser').get_text(),
                    'biyoloji': BeautifulSoup(cols[14],'html.parser').get_text()
                }
            elif formattedData['bolum_turu'] == 'SÖZ':
                formattedData['ayt'] = {
                    'edebiyat': BeautifulSoup(cols[11],'html.parser').get_text(),
                    'tarih1': BeautifulSoup(cols[12],'html.parser').get_text(),
                    'cografya1': BeautifulSoup(cols[13],'html.parser').get_text(),
                    'tarih2': BeautifulSoup(cols[14],'html.parser').get_text(),
                    'cografya2': BeautifulSoup(cols[15],'html.parser').get_text(),
                    'felsefe': BeautifulSoup(cols[16],'html.parser').get_text(),
                    'din': BeautifulSoup(cols[17],'html.parser').get_text()
                }
            elif formattedData['bolum_turu'] == 'EA':
                formattedData['ayt'] = {
                    'matematik': BeautifulSoup(cols[11],'html.parser').get_text(),
                    'turkce': BeautifulSoup(cols[12],'html.parser').get_text(),
                    'tarih1': BeautifulSoup(cols[13],'html.parser').get_text(),
                    'cografya1': BeautifulSoup(cols[14],'html.parser').get_text()
                }
            elif formattedData['bolum_turu'] == 'DİL':
                formattedData['ydt'] = {
                    'dil': BeautifulSoup(cols[11],'html.parser').get_text(),
                }
            if extra_fields is not False:
                for field in extra_fields:
                    formattedData[field['key']] = field['value']
            return formattedData
        except:
            self.formatRecursively(index, cols, extra_fields)