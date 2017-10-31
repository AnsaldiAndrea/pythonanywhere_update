import re
import pprint
import MySQLdb as mysql
import importer
from datetime import datetime
import release

pp = pprint.PrettyPrinter()

db = mysql.connect(
        host='Raistrike.mysql.pythonanywhere-services.com',
        user="Raistrike",
        passwd="Nuvoletta2",db="Raistrike$data")
print('database connected')

def get_pastebin():
    return importer.import_data()

def regex_planet(values, title_dict):
    match = re.fullmatch('((.*)\\s(\\d+))|(.*)',values['title_volume'])
    if match and match.group(1):
        title = match.group(2)
        volume = int(match.group(3))
        lower = re.sub('[^\w]','',title).lower()
        if lower in title_dict:
            release.insert(db,to_dict(title_dict[lower],volume,values))
        else:                                                                   # manga is not in database and is not one-shot
            release.unknown(db,values)
    elif match and match.group(4):                                              # one-shot
        title = match.group(4)
        lower = re.sub('[^\w]','',title).lower()
        if lower in title_dict:
            release.insert(db,to_dict(title_dict[lower],1,values))
        else:
            release.unknown(db,values)

def regex_star(values, title_dict):
    match = re.fullmatch('((.*)\\sn\\.\\s(\\d+))|((.*)\\svolume\\sunico)',values['title_volume'])
    if match and match.group(1):
        title = match.group(2)
        volume = int(match.group(3))
        lower = re.sub('[^\w]','',title).lower()
        if lower in title_dict:
            release.insert(db,to_dict(title_dict[lower],volume,values))
        else:
            release.unknown(db,values)
    elif match and match.group(4):                                          # one-shot
        title = match.group(5)
        lower = re.sub('[^\w]','',title).lower()
        if lower in title_dict:
            release.insert(db,to_dict(title_dict[lower],1,values))
        else:
            release.unknown(db,values)


def regex_jpop(values,title_dict,to_correct):
    match = re.fullmatch('((.*)\\s(\\d+))|(.*)',values['title_volume'])
    if match and match.group(1):
        title = match.group(2)
        volume = int(match.group(3))
        lower = re.sub('[^\w]','',title).lower()
        if lower in title_dict:
            to_correct.append(to_dict(title_dict[lower],volume,values))
        else:
            release.unknown(db,values)
    elif match and match.group(4):                                          # one-shot
        title = match.group(4)
        lower = re.sub('[^\w]','',title).lower()
        if lower in title_dict:
            to_correct.append(to_dict(title_dict[lower],1,values))
        else:
            release.unknown(db,values)


def correct_jpop(values):
    news_list = [x for x in values if not x['cover']]
    other = [x for x in values if x not in news_list]
    for n in news_list:
        o = [x for x in other if x['manga_id']==n['manga_id'] and x['volume']==n['volume']]
        if o:
            n['cover']=o[0]['cover']
    return news_list

def remove_duplicate(list):
    temp_list = []
    for x in list:
        if x not in temp_list:
            temp_list.append(x)
    return temp_list

def get_title_from_id(cursor,id):
    cursor.execute('select title from manga where id={}'.format(id))
    result = cursor.fetchone()
    return result[0] if result else ''

'''
def insert_release(cursor,manga_id,subtitle,volume,release_date,price,cover):
    try:
        if release_date:
            ex = ('insert into releases (manga_id,subtitle,volume,release_date,price,cover) '
            'values({},"{}",{},\'{}\',{},"{}") '
            'on duplicate key update cover=values(cover), release_date=values(release_date)').format(manga_id,subtitle,volume,release_date,price,cover)
            cursor.execute(ex)
            db.commit()
        else:
            ex = ('insert into releases (manga_id,subtitle,volume,price,cover) '
            'values({},"{}",{},{},"{}") '
            'on duplicate key update cover=values(cover)').format(manga_id,subtitle,volume,price,cover)
            print('here?')
            cursor.execute(ex)
            db.commit()
        update_collection(manga_id,subtitle,volume,cover)
    except Exception as e:
        print(e)
        db.rollback()

def to_array(manga_id,volume,values):
    release_date = datetime.strptime(values[2], '%d/%m/%Y') if values[2] else datetime.now()
    release_date = release_date.strftime('%Y-%m-%d')
    return (manga_id,
            values[1],
            volume,
            release_date,
            values[3] if values[3] else '0',
            values[4])


def insert_from(manga_id,volume,values):
    subtitle = values[1]
    release_date = datetime.strptime(values[2], '%d/%m/%Y') if values[2] else datetime.now()
    release_date = release_date.strftime('%Y-%m-%d')
    price = values[3] if values[3] else '0'
    cover = values[4]
    insert_release(db.cursor(),manga_id,subtitle,volume,release_date,price,cover)




def update_collection(manga_id,subtitle,volume,cover):
    c = db.cursor()
    try:
        c.execute('insert into collection (manga_id,subtitle,volume,cover) values({},"{}",{},"{}")'.format(manga_id,subtitle,volume,cover))
        db.commit()
    except Exception:
        db.rollback()
        c.execute('update collection set cover="{}" where manga_id={} and volume={}'.format(cover,manga_id,volume))
        db.commit()

def update_manga(manga_id,volume,cover,release_date):
    t = datetime.strptime('%Y-%m-%d',release_date).isocalendar()[:2]
    now = datetime.now().isocalendar()[:2]
    if t<=now:
        c = db.cursor()
        c.execute('select volumes,released,status from manga where id={}'.format(manga_id))
        x = c.fetchone()
        volumes,released,status = x[0],x[1],x[2]
        if volume>volumes:
            c.execute('update manga set cover={} where id={}'.format(cover,manga_id))
            # TO DO
'''
def to_dict(manga_id,volume,values):
    release_date = datetime.strptime(values['release_date'], '%d/%m/%Y') if values['release_date'] else datetime.now()
    release_date = release_date.strftime('%Y-%m-%d')
    price = values['price'] if values['price'] else '0'
    return {'manga_id':manga_id,
        'subtitle':values['subtitle'],
        'volume':volume,
        'publisher':values['publisher'],
        'release_date':release_date,
        'price':price,
        'cover':values['cover']}


cur = db.cursor()
cur.execute('select id,title from manga')
title_dict = { re.sub('[^\w]','',x[1]).lower():x[0] for x in cur.fetchall() }
cur.execute('select * from alias')
for x in cur.fetchall():
    title_dict[x[1]] = x[0]

raw_data = remove_duplicate(get_pastebin())
to_correct = []

for x in raw_data:
    x_dict = {'title_volume':x[0],'subtitle':x[1],'publisher':x[5],'release_date':x[2],'price':x[3],'cover':x[4]}
    if x[5] == 'planet':
        regex_planet(x_dict,title_dict)
        continue
    if x[5] == 'star':
        regex_star(x_dict,title_dict)
        continue
    if x[5] == 'jpop':
        regex_jpop(x_dict,title_dict,to_correct)
        continue
for x in correct_jpop(to_correct):
    release.insert(db,x)

db.close()