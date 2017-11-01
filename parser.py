import importer
from mypackage.parser import parser

def get_pastebin():
    return importer.import_data()

def remove_duplicate(list):
    temp_list = []
    for x in list:
        if x not in temp_list:
            temp_list.append(x)
    return temp_list

raw_data = remove_duplicate(get_pastebin())
data = [{'title_volume':x[0],'subtitle':x[1],'publisher':x[5],'release_date':x[2],'price':x[3],'cover':x[4]} for x in raw_data]
p = parser()
p.parseall(data)
p.close()