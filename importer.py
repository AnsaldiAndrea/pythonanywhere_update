from mypackage.pastebin import PastebinAPI
import encoder
import mypackage.csvstring as csvstring
from lxml import etree

def import_data():
    api_key = 'bdb21db2a07cb713b7e6a1713257564d'
    x = PastebinAPI()
    user_key = x.generate_user_key(api_key,'Raistrike','Nuvoletta2').decode('utf-8')
    paste = x.pastes_by_user(api_key,user_key).decode('utf-8')
    root = etree.fromstring(paste)
    paste_key = root.xpath('paste_key')[0].text
    raw = x.raw(api_key,user_key,paste_key).decode('utf-8')
    decoded = encoder.decode(raw,return_type='str')
    return csvstring.csvstring_to_values(decoded)