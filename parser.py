import importer
from mypackage.parser import Parser


def get_pastebin():
    return importer.import_data_json()


def remove_duplicate(_list):
    temp_list = []
    for x in _list:
        if x not in temp_list:
            temp_list.append(x)
    return temp_list


data = remove_duplicate(get_pastebin())
for x in data:
    print(x)


#with Parser() as p:
#    p.parseall(data)
