import json
import glob
class DataMerger:
    def __init__(self):
        self.started_merger = True
        
    def run(self):
        FullJSON = {}
        
        fileJson = json.load(open("./extracted/net.json"))
        for data in fileJson :
            yop_kodu = data['yop_kodu'].replace('/2015/on','').replace('on','')
            yil = data['yil']
            if FullJSON.get(yop_kodu) is None :
                FullJSON[yop_kodu] = {}
                data.pop("yop_kodu", None)
                data.pop("yil", None)
                FullJSON[yop_kodu][yil] = data
            else :
                if FullJSON[yop_kodu].get(yil) is None :
                    data.pop("yop_kodu", None)
                    data.pop("yil", None)
                    FullJSON[yop_kodu][yil] = data
        universities = open('./extracted/information.json')
        universityJson = json.load(universities)
        universityFullJson = {}
        for data in universityJson :
            universityFullJson[data['yop_kodu']] = data
            if not FullJSON.get(data['yop_kodu']) is None :
                universityFullJson[data['yop_kodu']]['netler'] = FullJSON[data['yop_kodu']]
        newJsonFile = open('./extracted/merged.json', 'w+', encoding='utf8')
        newJsonFile.write(json.dumps(universityFullJson, ensure_ascii=False))
        newJsonFile.close()