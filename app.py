from flask import Flask, request, jsonify, render_template, make_response, send_from_directory, redirect
from module.db import DB

from datetime import datetime, time, date, timedelta

app = Flask(__name__)
db = DB()

#@app.route('/favicon.ico')
#def favicon():
#    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

#@app.errorhandler(404)
#def page_not_found(error):
#    return render_template('404.html')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/gen_record')
def gen_record():
    users = list(db.get_users())
    users += db.get_users_plus()

    return make_response(render_template('gen_record.html',
        users = users,
        enumerate = enumerate
    )), 200

@app.route('/name_check')
def name_check():
    username = request.args.get('name', '')
    if username == '':
        overlap = 'none'
    else:
        try:
            users = db.get_user_by_name(username)
            if len(users) == 0:
                overlap = 'pass'
            else:
                overlap = 'fail'
        except:
            overlap = 'fail'

    context = { 'overlap': overlap }
    return jsonify(context)

@app.route('/add_user')
def add_user():
    users = db.get_user_names()
    return render_template('add_user.html', users = [_['UserName'] for _ in users]), 200

@app.route('/insert_user')
def insert_user():
    name = request.args.get('name', '')
    if name is not '':
        db.insert_user(name)
    return redirect('/')

@app.route('/show_records')
def show_records():
    EXT = ['', '비너스 넥스트', '서곡', '개척기지', '격동']

    start_day = request.args.get('start', '')
    end_day = request.args.get('end', '')
    name = request.args.get('name', '')
    ext = request.args.get('extension', '')

    if start_day == '':
        d = date.today()
        t = time(0, 0, 0, 0)
        start_day = datetime.combine(d, t).timestamp()
    else:
        d = datetime.strptime(start_day, "%Y-%m-%d").date()
        t = time(0, 0, 0, 0)
        start_day = datetime.combine(d, t).timestamp()

    if end_day == '':
        d = date.today() + timedelta(days=1)
        t = time(0, 0, 0, 0)
        end_day = datetime.combine(d, t).timestamp()
    else:
        d = datetime.strptime(end_day, "%Y-%m-%d").date()
        t = time(0, 0, 0, 0)
        end_day = datetime.combine(d, t).timestamp()

    datas = db.get_record(start_day, end_day, name, ext)
    for v in datas:
        ext = v['Extension']
        v['Extension'] = ""
        _tmp = ext.split('|')[:-1]
        for i, _ in enumerate(_tmp):
            if i == len(_tmp) - 1:
                v['Extension'] += EXT[int(_)]
            else:
                v['Extension'] += EXT[int(_)] + ", "

        _time = v['DATE_TIME']
        v['DATE_TIME'] = str(datetime.fromtimestamp(_time).time())

    return make_response(render_template('show_records.html',
        datas = datas,
        len = len(datas)
    )), 200

@app.route('/today_record')
def today_record():
    return render_template('today_record.html')

@app.route('/get_names')
def get_names():
    return jsonify(db.get_user_names_by_name(request.args.get('value', '')))

@app.route('/get_corps')
def get_corps():
    return jsonify(db.get_company_names_by_name(request.args.get('value', '')))

@app.route('/add_record')
def add_record():
    return make_response(render_template('add_record.html',
        users = db.get_user_names(),
        companys = db.get_company_names(),
        range = range
    )), 200

@app.route('/insert_record')
def insert_record():
    extension = request.args.get('extension', '')
    users = [ 
        [ request.args.get('name_id_1', ''), request.args.get('name_1', ''), request.args.get('corp_id_1', ''), request.args.get('corp_1', ''), request.args.get('score_1', 0) ],
        [ request.args.get('name_id_2', ''), request.args.get('name_2', ''), request.args.get('corp_id_2', ''), request.args.get('corp_2', ''), request.args.get('score_2', 0) ],
        [ request.args.get('name_id_3', ''), request.args.get('name_3', ''), request.args.get('corp_id_3', ''), request.args.get('corp_3', ''), request.args.get('score_3', 0) ],
        [ request.args.get('name_id_4', ''), request.args.get('name_4', ''), request.args.get('corp_id_4', ''), request.args.get('corp_4', ''), request.args.get('score_4', 0) ],
    ]
    db.insert_record(users, extension)

    for i, user in enumerate(users):
        tmp = db.get_user(user[0])[0]
        tmp['AverageScore'] = ((tmp['AverageScore'] * tmp['Amount']) + int(user[4])) / (tmp['Amount'] + 1)
        tmp['AverageRank'] = ((tmp['AverageRank'] * tmp['Amount']) + (i + 1)) / (tmp['Amount'] + 1)
        tmp['Rank_{}'.format((i+1))] += 1
        tmp['Amount'] += 1

        db.update_user(tmp)

    return redirect('/')

@app.route('/search_record')
def search_record():
    return render_template('search_record.html')

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=80, debug=True)