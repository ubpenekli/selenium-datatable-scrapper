from selenium.webdriver.common.by import By
from src.datatable import DatatableScrapper as Scrapper
from bs4 import BeautifulSoup
from datetime import datetime

class LisansScrapper(Scrapper):

    def __init__(self, url, dtId, delay, perPage):
        super(LisansScrapper, self).__init__(url, dtId, delay, perPage)
        self.year0 = str(datetime.today().year)
        self.year1 = str(int(datetime.today().year) - 1)
        self.year2 = str(int(datetime.today().year) - 2)
        self.year3 = str(int(datetime.today().year) - 3)

    def format(self, extra_fields = False):
        formatted = []
        for index, cols in enumerate(self.data):
            kontenjan = BeautifulSoup(cols[8], 'html.parser').find_all('font')
            yerlesen = BeautifulSoup(cols[10], 'html.parser').find_all('font')
            taban_puan_sirasi = BeautifulSoup(cols[11], 'html.parser').find_all('font')
            taban_puan = BeautifulSoup(cols[12], 'html.parser').find_all('font')
            formattedData = {
                'yop_kodu' : BeautifulSoup(cols[1], 'html.parser').find_all('a')[0].get_text(),
                'universite_adi' : BeautifulSoup(cols[2], 'html.parser').strong.get_text(),
                'fakulte_adi' : BeautifulSoup(cols[2], 'html.parser').font.get_text(),
                'bolum_adi' : BeautifulSoup(cols[3], 'html.parser').strong.get_text(),
                'egitim_detay' : BeautifulSoup(cols[3], 'html.parser').font.get_text(),
                'sehir' : BeautifulSoup(cols[4], 'html.parser').get_text(),
                'universite_tur' : BeautifulSoup(cols[5], 'html.parser').get_text(),
                'ucret_burs' : BeautifulSoup(cols[6], 'html.parser').get_text(),
                'ogretim_tur' : BeautifulSoup(cols[7], 'html.parser').get_text(),
                'kontenjan' : {
                    self.year0 : kontenjan[0].get_text(),
                    self.year1 : kontenjan[1].get_text(),
                    self.year2 : kontenjan[2].get_text(),
                    self.year3 : kontenjan[3].get_text(),
                },
                'statu' : BeautifulSoup(cols[9], 'html.parser').get_text(),
                'yerlesen' : {
                    self.year0 : yerlesen[0].get_text(),
                    self.year1 : yerlesen[1].get_text(),
                    self.year2 : yerlesen[2].get_text(),
                    self.year3 : yerlesen[3].get_text(),
                },
                'taban_puan_sirasi' : {
                    self.year0 : taban_puan_sirasi[0].get_text(),
                    self.year1 : taban_puan_sirasi[1].get_text(),
                    self.year2 : taban_puan_sirasi[2].get_text(),
                    self.year3 : taban_puan_sirasi[3].get_text(),
                },
                'taban_puan' : {
                    self.year0 : taban_puan[0].get_text(),
                    self.year1 : taban_puan[1].get_text(),
                    self.year2 : taban_puan[2].get_text(),
                    self.year3 : taban_puan[3].get_text(),
                }
            }
            if extra_fields is not False:
                for field in extra_fields:
                    formattedData[field['key']] = field['value']
            formatted.append(formattedData)
            print('(' + formattedData['bolum_turu'].upper() + ') Formatted ' + str(index) + ': ' + formattedData['yop_kodu'] + " - " + formattedData['universite_adi'] + ' / ' + formattedData['bolum_adi'])
        return formatted