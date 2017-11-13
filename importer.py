from mypackage.pastebin import PastebinAPI
from mypackage import csvstring, encoder
from lxml import etree
import json


def import_data():
    api_key = 'bdb21db2a07cb713b7e6a1713257564d'
    x = PastebinAPI()
    user_key = x.generate_user_key(api_key, 'Raistrike', 'Nuvoletta2').decode('utf-8')
    paste = x.pastes_by_user(api_key, user_key).decode('utf-8')
    root = etree.fromstring(paste)
    paste_key = root.xpath('paste_key')[0].text
    raw = x.raw(api_key, user_key, paste_key).decode('utf-8')
    decoded = encoder.decode(raw)
    print(decoded)
    return [
        {'title_volume': x[0], 'subtitle': x[1], 'publisher': x[5], 'release_date': x[2], 'price': x[3], 'cover': x[4]}
        for x in csvstring.csvstring_to_values(decoded)]


def import_data_json():
    api_key = 'bdb21db2a07cb713b7e6a1713257564d'
    x = PastebinAPI()
    user_key = x.generate_user_key(api_key, 'Raistrike', 'Nuvoletta2').decode('utf-8')
    paste = x.pastes_by_user(api_key, user_key).decode('utf-8')
    root = etree.fromstring(paste)
    paste_key = root.xpath('paste_key')[0].text
    raw = x.raw(api_key, user_key, paste_key).decode('utf-8')
    decoded = encoder.decode(raw)
    return json.loads(decoded)
