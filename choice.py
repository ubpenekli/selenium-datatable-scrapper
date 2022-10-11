from src import Lisans
from src import Onlisans
from src import Netdata
import json
import time
import glob

class ChoiceWizard:
    def __init__(self):
        self.started_choice_wizard = True
        
    def fetchYokAtlas(self, pagesCount = False, rowsCount = False):
        allData = []
        scrapper = Onlisans('https://yokatlas.yok.gov.tr/tercih-sihirbazi-t3-tablo.php?p=tyt', 'mydata', 1.5, 50)
        if pagesCount is not False and rowsCount is not False:
            scrapper.fetchPages(pagesCount, rowsCount)
        else:
            scrapper.fetchPages()
        typeData = scrapper.format(extra_fields = [{ 'key': 'bolum_turu', 'value': 'tyt'}])
        allData = allData + typeData
        del scrapper

        types = ['dil', 'say', 'söz', 'ea']
        for departmentType in types:
            scrapper = Lisans('https://yokatlas.yok.gov.tr/tercih-sihirbazi-t4-tablo.php?p='+departmentType, 'mydata', 0.5, 50)

            if pagesCount is not False and rowsCount is not False:
                scrapper.fetchPages(pagesCount, rowsCount)
            else:
                scrapper.fetchPages()
            typeData = scrapper.format(extra_fields = [{ 'key': 'bolum_turu', 'value': departmentType}])
            time.sleep(3)
            allData = allData + typeData
        del scrapper

        return json.dumps(allData, ensure_ascii=False).encode('utf8').decode()

    def run(self):
        data = self.fetchYokAtlas()

        f = open('./extracted/information.json', 'w+', encoding='utf-8')
        f.write(data)
        f.close()