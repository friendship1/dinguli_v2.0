from flask import Flask, render_template, request
import json

import form
import func

app = Flask(__name__)

'''
rules
make simple main.py
    do json.dumps not here
'''

@app.route('/')
def main():
    return 'Hello!'
@app.route('/fallback', methods=['POST'])
def fallback():
    value = request.get_json()
    print(value)
    user_id = value['userRequest']['user']['id']
    func.insert_lastlog(user_id)
    return func.mk_fallback(value)

@app.route('/home', methods=['POST'])
def test():
    value = request.get_json()
    print(value)
    ### do database work here - log username
    user_id = value['userRequest']['user']['id']
    func.insert_lastlog(user_id)
    return form.home_json

@app.route('/seebobs', methods=['POST'])
def seebobs():
    value = request.get_json()
    print(value)
    return func.mk_seebobs()
@app.route('/starchoose', methods=['POST'])
def starchoose():
    value = request.get_json()
    print(value)
    return form.starchoose_json
@app.route('/stargive', methods=['POST'])
def stargive():
    value = request.get_json()
    print(value)
    stargive = json.loads(form.stargive_json) # copy json (quite messy method)
    stargive['context']['values'][0]['params']['rest'] = value['action']['clientExtra']['rest'] # to send 'quickreply extra value' to next entity.
    return json.dumps(stargive)
@app.route('/stardone', methods=['POST'])
def stardone():
    value = request.get_json()
    print(value) 
    user_id = value['userRequest']['user']['id']
    rest_type = value['contexts'][0]['params']['rest']['value']
    meal_type = func.proper_time()
    star = value['userRequest']['utterance'] 
    ### do database work here - apply star rating
    func.insert_star(user_id,rest_type,meal_type,star)
    return func.mk_stardone()
@app.route('/studentimg', methods=['POST'])
def studentimg():
    value = request.get_json()
    print(value)
    return func.mk_img('student') 
@app.route('/r1img', methods=['POST'])
def r1img():
    value = request.get_json()
    print(value)
    return func.mk_img('r1') 
@app.route('/staffimg', methods=['POST'])
def staffimg():
    value = request.get_json()
    print(value)
    return func.mk_img('staff') 
@app.route('/lifeinfo', methods=['POST'])
def lifeinfo():
    value = request.get_json()
    print(value)
    return form.lifeinfo_json
@app.route('/imgupload', methods=['POST'])
def imgupload():
    value = request.get_json()
    print(value)
    return func.mk_imgupload(value)
@app.route('/uploadchoose', methods=['POST'])
def uploadchoose():
    value = request.get_json()
    print(value)
    return func.mk_uploadchoose(value)
    return form.uploadchoose_json
@app.route('/showchoose',methods=['POST'])
def showchoose():
    value = request.get_json()
    print(value)
    return form.tempcard_json
@app.route('/showcards',methods=['POST'])
def showcards():
    value = request.get_json()
    print(value)
    if(value['action']['clientExtra'] != None and 'rest' in value['action']['clientExtra']):
        return func.mk_showcards1(value)
    else:
        return func.mk_showcards2(value)
@app.route('/carddeletecheck', methods=['POST'])
def carddeletecheck():
    value = request.get_json()
    print(value)
    return func.mk_carddeletecheck(value)
@app.route('/carddelete', methods=['POST'])
def carddelete():
    value = request.get_json()
    print(value)
    return func.mk_carddelete(value)
@app.route('/cardlike', methods=['POST'])
def cardlike():
    value = request.get_json()
    print(value)
    return func.mk_like(value)
@app.route('/mailgive', methods=['POST'])
def mailgive():
    value = request.get_json()
    print(value)
    return form.mailgive_json




    


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888)
