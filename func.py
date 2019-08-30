#-*-coding:utf-8-*-
import json
import pymysql
import datetime
import requests
import hashlib
import os

import smtplib
from email.mime.text import MIMEText
from email.MIMEMultipart import MIMEMultipart
from email.header import Header

import form

sqlpasswd = "password"
admin_list = ['2f16c12f16c12f16c12f16c12f16c12f16c12f16c12f16c12f16c12f16c1', '2f16c12f16c12f16c12f16c12f16c12f16c12f16c12f16c12f16c12f16c1']

def mk_fallback(value):    
    if(len(value["contexts"]) == 0): # Normal Fallback
        return json.dumps(insert_text(form.home_json, "무슨 소리인지 모르겠어...;;"))
    else: ### uploaddone (add text explanation)
        params = value["contexts"][0]["params"] # To get user text explaination when uploads image
        name = value["contexts"][0]["name"]
        if("resturls" == name):
            return mk_uploaddone(value)
        elif("mailflag" == name):
            if(params['stage']['value'] == '0'):
                return mk_mailveri1(value)
            else:
                return mk_mailveri2(value)
        else: # Error case
            print("error is here")
            return json.dumps(insert_text(form.home_json, "Error: at fallback\n무슨 소리인지 모르겠어...;;"))

def insert_text(base_json, text):
    base = json.loads(base_json)
    text_form = json.loads('{"simpleText": {"text": "' + text + '"}}')
    base['template']['outputs'].insert(0, text_form)
    return base

def delta_minutes(last):
    delta = datetime.datetime.now() - last
    return delta.days * 1440 + delta.seconds//60

def label2kor(rest, sort_type, page):
    if(rest == 'student'):
        rest_ = "학생식당 "
    elif(rest == 'r1'):
        rest_ = "연구동   "
    elif(rest == 'staff'):
        rset_ = "교직원   "
    else:
        rest_ = "기타     "
    if(sort_type == "latest"):
        sort_ = "최신순"
    elif(sort_type == "mostlike"):
        sort_ = "좋아요순(every)"
    elif(sort_type == "mostlike_today"):
        sort_ = "좋아요순(today)"
    elif(sort_type == "mycard"):
        sort_ = "내 포스트"
    else:
        sort_ = "기타정렬"
    return rest_ + sort_ + "\\n" + str(page + 1) + " 페이지"

            
def mk_uploaddone(value):
    params = value["contexts"][0]["params"] # To get user text explaination when uploads image
    rest = params["rest"]["value"]
    urls = params["urls"]["value"].split(',')
    text = value["userRequest"]["utterance"]
    user_id = value["userRequest"]["user"]["id"]
# print(rest, urls, text)
    micro = str(datetime.datetime.now().microsecond)
    date = today_date()
    filename = date + hashlib.md5(micro+date).hexdigest() + '.jpg'
    # Do DB works here
    conn = pymysql.connect(host='localhost', user='root', password=sqlpasswd, db='open_kakao')
    curs = conn.cursor()
    seperate = text.find('\n')
    title = ""
    if(seperate != -1):
        title = text[:seperate]
    text = text[seperate+1:]
    sql = "INSERT INTO cards(id, rest, img_name, title, text) VALUES(\"%s\",\"%s\",\"%s\",\"%s\",\"%s\")" %(user_id, rest, filename, title, text)
    curs.execute(sql)
    conn.commit() # should be added if sql INSERT!
    rows = curs.fetchall()
    conn.close() 

    # SAVE IMAGE IN URL
    for url in urls:
        r = requests.get(url)
        with open('/home/web/www/html/kakao_files/' + filename,'wb') as f:
            f.write(r.content)
        break # FOR NOW, ONLY FIRST IMAGE WILL BE SAVED.
    return json.dumps(insert_text(mk_seebobs(), "게시되었습니다."))



def save_img(urls):
    for url in urls:
        r = requests.get(url)
        with open('/home/web/www/html/menu_data/','wb') as f:
            f.write(r.content)



def proper_time():
    today = datetime.datetime.today()
    if(today.hour >= 16 and today.hour <= 23):
        return 'dinner'
    else:
        return 'lunch'    

def today_date():
    today = datetime.datetime.today()
    ret = today.strftime("%Y%m%d")
    return ret

def get_img(rest_type):
    conn = pymysql.connect(host='localhost', user='root', password=sqlpasswd, db='open_kakao')
    curs = conn.cursor()
    if(proper_time() == 'lunch'):
        sql = "SELECT img_name FROM cards WHERE rest=\"%s\" AND DATE(update_time)=DATE(NOW()) AND HOUR(update_time) < 16 ORDER BY likes DESC LIMIT 1" %(rest_type)

    else:
        sql = "SELECT img_name FROM cards WHERE rest=\"%s\" AND DATE(update_time)=DATE(NOW()) AND HOUR(update_time) >= 16 ORDER BY likes DESC LIMIT 1" %(rest_type)

# sql = "SELECT name_save, reg_time FROM upload_menu WHERE rest_type=\"%s\" AND meal_type=\"%s\" AND DATE(reg_time)=DATE(NOW()) ORDER BY reg_time DESC LIMIT 2" %(rest_type, proper_time()) # This was for web upload only
    curs.execute(sql)
    rows = curs.fetchall()
    conn.close()
    if(len(rows) == 0): # if file not exist
        return (("error.jpg"),)
    return rows

def get_star(rest_type):
    return 0
    conn = pymysql.connect(host='localhost', user='root', password=sqlpasswd, db='open_kakao')
    curs = conn.cursor()
    sql = ""

def mk_bob_menu():
    rest_list = ['student', 'r1', 'staff']
    addr = "http://www.dgrang.com/kakao_files/"
    time = proper_time()
    bob_menu = json.loads(form.bob_menu_json)

    if(time == 'dinner'):  # set title
        bob_menu['listCard']['header']['title'] = "오늘의 저녁"
    conn = pymysql.connect(host='localhost', user='root', password=sqlpasswd, db='open_kakao')
    curs = conn.cursor()
    for idx,rest in enumerate(rest_list):
        val = get_img(rest)[0][0]
        if val == 'error.jpg': val = '' # THIS IS BECAUSE CAHCHED IMAGE
        bob_menu['listCard']['items'][idx]['imageUrl'] = addr + val
        sql = "SELECT AVG(star), COUNT(star) FROM stars WHERE rest_type=\"%s\" AND meal_type=\"%s\" AND time=\"%s\"" %(rest, time, today_date())
        curs.execute(sql)
        rows = curs.fetchall()
        stars = " -  "
        if(rows[0][1] != 0):
            stars = rows[0][0]
        bob_menu['listCard']['items'][idx]['title'] += str(stars)[:4] + " /5"
        bob_menu['listCard']['items'][idx]['description'] = str(rows[0][1]) + "명이 참여했습니다."
    conn.close()
    return bob_menu

def mk_seebobs():
    seebobs = json.loads(form.seebobs_json)
    seebobs["template"]["outputs"].append(mk_bob_menu())
    return json.dumps(seebobs)

def mk_stardone():
    stardone = json.loads(form.stardone_json)
    stardone["template"]["outputs"].append(mk_bob_menu())
    return json.dumps(stardone)

def insert_lastlog(user_id): # works at /home
    conn = pymysql.connect(host='localhost', user='root', password=sqlpasswd, db='open_kakao')
    curs = conn.cursor()
    sql = "INSERT INTO users(id,last) VALUES(\"%s\",NOW()) ON DUPLICATE KEY UPDATE last=NOW()" %(user_id)
    curs.execute(sql)
    conn.commit() # should be added if sql INSERT!
    rows = curs.fetchall()
    conn.close()
    
def insert_star(user_id, rest_type, meal_type, star):
    conn = pymysql.connect(host='localhost', user='root', password=sqlpasswd, db='open_kakao')
    curs = conn.cursor()
    today = today_date() 
    sql = "INSERT INTO stars VALUES(\"%s\",\"%s\",\"%s\",\"%s\",\"%s\") ON DUPLICATE KEY UPDATE star=\"%s\", rest_type=\"%s\", time=\"%s\"" %(user_id, rest_type, meal_type, star, today, star, rest_type, today)
    curs.execute(sql)
    conn.commit() # should be added if sql INSERT!
    rows = curs.fetchall()
    conn.close()

def mk_img(rest_type): # return menu real image (currently disabled)
    img = json.loads(form.img_json)
    time = proper_time()
    num = 1;
    if(time == 'lunch' and (rest_type == 'student' or rest_type == 'r1') ):
        num = 2;  # two img exists
    filenames = get_img(rest_type) # if none, return /menu_data/error.jpg
    num = min(num,len(filenames))
    for idx in range(num):
        simpleImage = json.loads(form.simpleImage_json)
        simpleImage["simpleImage"]["imageUrl"] += filenames[idx][0]
        img["template"]["outputs"].append(simpleImage)
    return json.dumps(img)
    
def mk_imgupload(value): # Get the image url frm Plugin, and move to get input about text explanation. 
    rest = value["action"]["clientExtra"]["rest"]
    param = value["action"]["params"]["secureimage"]
    param = json.loads(param)
    urls = param["secureUrls"]
    urls = urls[urls.find('(') +1:urls.rfind(')')]
#urls = urls.split(',')
#for url in urls:
    print(urls)
    uploadtextgive = json.loads(form.uploadtextgive_json)
    uploadtextgive["context"]["values"][0]["params"]["rest"] = rest
    uploadtextgive["context"]["values"][0]["params"]["urls"] = urls
    return json.dumps(uploadtextgive)

def mk_uploadchoose(value): # Check whether user is verified for UPLOAD
    user_id = value['userRequest']['user']['id']
    conn = pymysql.connect(host='localhost', user='root', password=sqlpasswd, db='open_kakao')
    curs = conn.cursor()
    sql = "SELECT * FROM users WHERE id=\"%s\"" %(user_id)
    curs.execute(sql)
    rows = curs.fetchall()
    conn.close()
    if(len(rows) == 0):
        #ERROR This cannot happen
        return json.dumps(insert_text(mk_seebobs(), "오류 발생 at mk_uploadchoose"))
    else:
        if(rows[0][2] is None):
            # failure (NOT verified)
            return form.uploadchoose_json # @LURE
            return form.mailYN_json # verify Y/N check
        else:
            return form.uploadchoose_json



def mk_showcards1(value): # if came first
    rest = value['action']['clientExtra']['rest'] # get from quickreply
    user_id = value['userRequest']['user']['id']
    return mk_showcards(rest, 'latest', 0, 0, user_id)

def mk_showcards2(value): # if came from showcards recursively
    params = value["contexts"][0]["params"] # get from context
    rest = params["rest"]["value"]
    sort_type = params["sort_type"]["value"]
    prev_page = int(params["page"]["value"])
    button = value['action']['clientExtra']['page']
    page = 0
    if(button == 'before' and prev_page != 0):
        page = prev_page - 1
    elif(button == 'next'):
        page = prev_page + 1
    elif(button == 'stay'): # in case of delete button
        page = prev_page
    elif(button == 'mostlike'):
        sort_type = 'mostlike'
    elif(button == 'mostlike_today'):
        sort_type = 'mostlike_today'
    elif(button == 'latest'):
        sort_type = 'latest'
    elif(button == 'mycard'):
        sort_type = 'mycard'
    else:
        page = 0
    user_id = value['userRequest']['user']['id']
    return mk_showcards(rest,sort_type, prev_page, page, user_id)

def mk_showcards(rest, sort_type, prev_page, page, user_id): # Called from showcards1,2 and delete
    # sort_type : latest, mostlike, mostlike_today, mypost(latest)
# print(page, sort_type, rest)
    conn = pymysql.connect(host='localhost', user='root', password=sqlpasswd, db='open_kakao')
    curs = conn.cursor()
    if(sort_type == 'mostlike'):
        sql = "SELECT * FROM cards WHERE rest = \"%s\" ORDER BY likes DESC, card_id DESC LIMIT %d, %d" %(rest, page*10, (page+1)*10)
    elif(sort_type == 'mycard'):
        sql = "SELECT * FROM cards WHERE rest = \"%s\" AND id=\"%s\" ORDER BY card_id DESC LIMIT %d, %d" %(rest, user_id, page*10, (page+1)*10)
    elif(sort_type == 'mostlike_today'):
        sql = "SELECT * FROM cards WHERE rest = \"%s\" AND DATE(update_time)=DATE(NOW()) ORDER BY likes DESC, card_id DESC LIMIT %d, %d" %(rest, page*10, (page+1)*10)
    else:
        sql = "SELECT * FROM cards WHERE rest = \"%s\" ORDER BY card_id DESC LIMIT %d, %d" %(rest, page*10, (page+1)*10)
    
    curs.execute(sql)
    rows = curs.fetchall()
    conn.close()
    #print(rows)
    if(len(rows) == 0):
        if(page != 0): 
            return mk_showcards(rest, sort_type, 0, prev_page, user_id)
        else: # Even page zero is Empty.
            return json.dumps(insert_text(mk_seebobs(), "게시글이 없습니다."))
    cards = json.loads(form.cards_json)

    ### CREATE CARDS
    for row in rows:
        # print(row)
        cardId = row[0]
        card = json.loads(form.card_json)
        date = row[3].strftime("%m/%d %H:%M. ")
        likes = str(row[7]) + " likes\n"
        card['title'] = date + likes + row[5]
        card['description'] = row[6]
        card['thumbnail']['imageUrl'] = "http://www.dgrang.com/kakao_files/" + row[4]
        card['buttons'][1]['extra']['cardId'] = cardId # Save cardId info at recommand btn extra
        # Modify like button label if already liked card
        conn = pymysql.connect(host='localhost', user='root', password=sqlpasswd, db='open_kakao')
        curs = conn.cursor()
        sql = "SELECT * FROM cardlikes WHERE card_id = \"%s\" AND id=\"%s\" AND flag=1" %(cardId, user_id)
        curs.execute(sql)
        result = curs.fetchall()
        conn.close()
        if(len(result) == 0):
            card['buttons'][1]['label'] = "추천"
            card['buttons'][1]['messageText'] = "추천"
        # Add delete buttoon
        if(row[1] == user_id or user_id in admin_list): # show delete btn only if post is written by user.
            cardDelBtn = json.loads(form.cardDelBtn_json)
            cardDelBtn['extra']['cardId'] = cardId
            card['buttons'].append(cardDelBtn)
        # Modify Link button links
        card['buttons'][0]['webLinkUrl'] += str(row[0]) # Add cardId at link
        # Append at cards                                      
        cards['template']['outputs'][0]['carousel']['items'].append(card)
    cards['context']['values'][0]['params']['rest'] = rest
    cards['context']['values'][0]['params']['sort_type'] = sort_type
    cards['context']['values'][0]['params']['page'] = page
    return json.dumps(insert_text(json.dumps(cards), label2kor(rest, sort_type, page)))

def mk_carddeletecheck(value):
    params = value["contexts"][0]["params"] # get from context
    rest = params["rest"]["value"]
    sort_type = params["sort_type"]["value"]
    page = int(params["page"]["value"])
    cardDelChk = json.loads(form.cardDelChk_json)
    cardDelChk["context"]["values"][0]["params"]["rest"] = rest
    cardDelChk["context"]["values"][0]["params"]["sort_type"] = sort_type
    cardDelChk["context"]["values"][0]["params"]["page"] = page
    cardDelChk["context"]["values"][0]["params"]["cardId"] = value["action"]["clientExtra"]["cardId"]
    return json.dumps(cardDelChk)

def mk_carddelete(value):
    params = value["contexts"][0]["params"] # get from context
    user_id = value['userRequest']['user']['id']
    card_id = params['cardId']['value']
    conn = pymysql.connect(host='localhost', user='root', password=sqlpasswd, db='open_kakao')
    curs = conn.cursor()
    sql = "SELECT * FROM cards WHERE card_id = \"%s\"" %(card_id)
    curs.execute(sql)
    rows = curs.fetchall()
    conn.close()
    if(len(rows) != 1): # Error handle
        return form.home_json
    row = rows[0]
    if(user_id == row[1] or user_id in admin_list): # only delete If user_id matchs
        filename = '/home/web/www/html/kakao_files/' + row[4]
        if(os.path.isfile(filename)):
            os.remove(filename)
        conn = pymysql.connect(host='localhost', user='root', password=sqlpasswd, db='open_kakao')
        curs = conn.cursor()
        sql = "DELETE FROM cards WHERE card_id = \"%s\"" %(card_id)
        curs.execute(sql)
        conn.commit() 
        rows = curs.fetchall()
        conn.close()

    rest = params["rest"]["value"]
    sort_type = params["sort_type"]["value"]
    prev_page = int(params["page"]["value"])
    cards = mk_showcards(rest, sort_type, 0, prev_page, user_id)
    return json.dumps(insert_text(cards, "삭제되었습니다."))

def mk_like(value): # Apply like(recommand) to a post
    params = value["contexts"][0]["params"] # get from context
    user_id = value['userRequest']['user']['id']
    card_id = value["action"]["clientExtra"]["cardId"]

    conn = pymysql.connect(host='localhost', user='root', password=sqlpasswd, db='open_kakao')
    curs = conn.cursor()
    sql = "SELECT * FROM cardlikes WHERE card_id = \"%s\" AND id = \"%s\"" %(card_id, user_id)
    curs.execute(sql)
    rows = curs.fetchall()
    # conn.close()
    if(len(rows) != 0 and rows[0][3] == 1):
        # Delete
        flag = 0
        sql1 = "UPDATE cardlikes SET flag=0 WHERE card_id=\"%s\" AND id=\"%s\"" %(card_id, user_id)
        sql2 = "UPDATE cards SET likes = likes-1 WHERE card_id=\"%s\"" %(card_id)
    else:
        # Insert
        flag = 1
        sql1 = "INSERT INTO cardlikes(card_id, id, flag) VALUES(\"%s\", \"%s\", 1) ON DUPLICATE KEY UPDATE card_id=\"%s\", id=\"%s\", flag=1" %(card_id, user_id, card_id, user_id)
        sql2 = "UPDATE cards SET likes = likes+1 WHERE card_id=\"%s\"" %(card_id)
    curs.execute(sql1)
    curs.execute(sql2)
    conn.commit()
    conn.close()

    rest = params["rest"]["value"]
    sort_type = params["sort_type"]["value"]
    prev_page = int(params["page"]["value"])
    cards = mk_showcards(rest, sort_type, 0, prev_page, user_id)
    if(flag):
        return json.dumps(insert_text(cards, "추천했습니다."))
    else:
        return json.dumps(insert_text(cards, "추천을 취소했습니다."))

def mk_mailveri1(value): # create key, store at DB (temperarly), send email.
    text = value["userRequest"]["utterance"]
    user_id = value['userRequest']['user']['id']

    seperate = text.rfind('@')
    if (text[seperate:] != "@dgist.ac.kr"):
        return json.dumps(insert_text(mk_seebobs(), "올바른 디지스트 메일 형식이 아닙니다. @dgist.ac.kr로 끝나게 해주세요."))
    else:
        ### create key
        micro = str(datetime.datetime.now().microsecond)
        key = str(hashlib.md5(micro).hexdigest())[:5]
        ### Store at DB (verify table)
        conn = pymysql.connect(host='localhost', user='root', password=sqlpasswd, db='open_kakao')
        curs = conn.cursor()
        ### Check last time
        sql = "SELECT * FROM verify WHERE id=\"%s\"" %(user_id)
        curs.execute(sql)
        rows = curs.fetchall()
        if(len(rows) != 0):
            last = rows[0][3]
            delta_minutes(last)
            if(delta_minutes(last) < 30):
                conn.close()
                return json.dumps(insert_text(mk_seebobs(), "한번 시도하시면 30분 뒤에 다시 인증 가능합니다."))
        sql = "INSERT INTO verify(id, md5, email) VALUES(\"%s\",\"%s\",\"%s\") ON DUPLICATE KEY UPDATE md5=\"%s\"" %(user_id, key, text, key)
        curs.execute(sql)
        rows = curs.fetchall()
        conn.commit() # should be added if sql INSERT!
        conn.close()
        ### Send e-mail
        mail_from = "dgtic.hello@gmail.com"
        mail_to = text
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login(mail_from, 'password') # password is here be careful
        msg=MIMEMultipart('alternative')
        msg['From'] = mail_from
        msg['To'] = mail_to
        msg['Subject'] = Header("[디지스트봇 딩굴이] 인증번호를 입력해주세요.",'utf-8')
        msg.attach(MIMEText("[디지스트봇 딩굴이]\n 인증번호는 " + key + "입니다.\n 카카오톡에 입력해주세요.", 'plain', 'utf-8'))
        s.sendmail(mail_from, text, msg.as_string())
        s.quit()
        return form.mailkey_json


def mk_mailveri2(value): # get key from user, correct it with DB, delete DB, give user verification.
    text = value["userRequest"]["utterance"]
    user_id = value['userRequest']['user']['id']
    ### Lookup DB
    conn = pymysql.connect(host='localhost', user='root', password=sqlpasswd, db='open_kakao')
    curs = conn.cursor()
    sql = "SELECT * FROM verify WHERE id=\"%s\"" %(user_id)
    curs.execute(sql)
    rows = curs.fetchall()
    conn.close()
    if(len(rows) == 0):
        # failure
        return json.dumps(insert_text(mk_seebobs(), "오류 발생 at mk_mailveri2 function"))
    else:
        key = rows[0][1]
        email = rows[0][2]
        last = rows[0][3]
        if(delta_minutes(last) > 5):
            #failure with timeout
            return json.dumps(insert_text(mk_seebobs(), "메일발송 후 5분이 경과하였습니다. 나중에 다시 시도해주세요."))
        else:
            if(text != key):
                # failure with key different
                return json.dumps(insert_text(mk_seebobs(), "인증번호가 다릅니다. 나중에 다시 시도해주세요."))
            else:
                # verify success
                conn = pymysql.connect(host='localhost', user='root', password=sqlpasswd, db='open_kakao')
                curs = conn.cursor()
                sql = "UPDATE users SET email=\"%s\" WHERE id=\"%s\"" %(email, user_id)
                curs.execute(sql)
                sql = "DELETE FROM verify WHERE id=\"%s\"" %(user_id)
                curs.execute(sql)
                conn.commit() # should be added if sql INSERT!
                # rows = curs.fetchall()
                conn.close()
                return json.dumps(insert_text(mk_seebobs(), "인증에 성공하였습니다."))

                

                

        



       










   
