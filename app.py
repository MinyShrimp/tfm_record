from flask import Flask, request, jsonify, render_template, make_response, send_from_directory, redirect
from module.db import DB

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
    return make_response(render_template('gen_record.html',
        users = db.get_users()
    )), 200

@app.route('/today_record')
def today_record():
    return make_response(render_template('today_record.html',
        datas = db.get_today_record()
    )), 200

@app.route('/search_record')
def search_record():
    return render_template('search_record.html')

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=80, debug=True)