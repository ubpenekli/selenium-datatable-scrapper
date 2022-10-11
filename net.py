from src import Lisans
from src import Onlisans
from src import Netdata
import json
import time
class NetWizard:
    def __init__(self):
        self.started_net_wizard = True
        
    def fetchNetdata(self, pagesCount = False, rowsCount = False):
        lisansDepartmentsFile = open('./asset/lisans.json', 'r', encoding='utf-8')
        onlisansDepartmentsFile = open('./asset/onlisans.json', 'r', encoding='utf-8')
        lisans = json.load(lisansDepartmentsFile)
        onlisans = json.load(onlisansDepartmentsFile)

        for index, department in enumerate(lisans):
            id = department['id']
            name = department['name']
            allData = []
            if index == 0:
                scrapper = Netdata(
                    'https://yokatlas.yok.gov.tr/netler-tablo.php?b=' + department['id'],
                    'mydata',
                    1.5,
                    50
                )
            else:
                scrapper.setSource(
                    'https://yokatlas.yok.gov.tr/netler-tablo.php?b=' + department['id']
                )
            
            if pagesCount is not False and rowsCount is not False:
                scrapper.fetchPages(pagesCount, rowsCount)
            else:
                scrapper.fetchPages()
            typeData = scrapper.format()
            f = open('./extracted/test-netdata/lisans/'+id+'.json', 'w+', encoding='utf-8')
            f.write(json.dumps(typeData, ensure_ascii=False).encode('utf8').decode())
            f.close()
            allData = allData + typeData

        for index, department in enumerate(onlisans):
            id = department['id']
            name = department['name']
            allData = []
            if index == 0:
                scrapper = Netdata(
                    'https://yokatlas.yok.gov.tr/netler-onlisans-tablo.php?b=' + department['id'],
                    'mydata',
                    1.5,
                    50
                )
            else:
                scrapper.setSource(
                    'https://yokatlas.yok.gov.tr/netler-onlisans-tablo.php?b=' + department['id']
                )
            if pagesCount is not False and rowsCount is not False:
                scrapper.fetchPages(pagesCount, rowsCount)
            else:
                scrapper.fetchPages()
            typeData = scrapper.format()
            f = open('./extracted/test-netdata/onlisans/'+id+'.json', 'w+', encoding='utf-8')
            f.write(json.dumps(typeData, ensure_ascii=False).encode('utf8').decode())
            f.close()
            allData = allData + typeData

        return json.dumps(allData, ensure_ascii=False).encode('utf8').decode()

    def merge_jsons(self):
        FullJSON = []
        files = glob.glob("./extracted/test-netdata/lisans/*.json")
        files = files + glob.glob("./extracted/test-netdata/onlisans/*.json")
        for jsonFile in files:
            f = open(jsonFile)
            jsonData = json.load(f)
            f.close()
            FullJSON = FullJSON + jsonData
        newFile = open('./extracted/net.json', 'w+', encoding='utf8')
        newFile.write(json.dumps(FullJSON, ensure_ascii=False).encode('utf8').decode())
        newFile.close()

    def run(self):
        self.fetchNetdata()
        self.merge_jsons()