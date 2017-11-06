import importer
from mypackage.parser import Parser


def get_pastebin():
    return importer.import_data()


def remove_duplicate(_list):
    temp_list = []
    for x in _list:
        if x not in temp_list:
            temp_list.append(x)
    return temp_list


raw_data = remove_duplicate(get_pastebin())
data = [{'title_volume': x[0], 'subtitle': x[1], 'publisher': x[5], 'release_date': x[2], 'price': x[3], 'cover': x[4]}
        for x in raw_data]
p = Parser()
p.parseall(data)
p.close()
