import os
import sys
from wsgiref.simple_server import make_server

sys.path.append('..')
from flask import Flask, render_template, send_from_directory
from flask_cors import CORS
from lib import set_config
from celery_tasks import search, result
import jinja2

app = Flask(__name__, static_folder="templates")
# Settings can be accessed across domains
CORS(app, supports_credentials=True)


@app.route("/realTime")
def real_time():
    # 传入SQl语句，处理得到的数据，返回当前时间数据
    # Pass in the SQL statement, process the obtained data, and return the current time data
    sql = "SELECT co2,temperature,humidity,DATE_FORMAT(`time`,'%y-%m-%d %H:%i:%s') as time FROM `data` WHERE`time` >DATE_SUB(NOW(),INTERVAL 10 SECOND);"
    r = search.delay(sql)
    d = result(r)
    if len(d) > 0:
        data = d[len(d) - 1]
        data_dict = {'co2': data[0], 'temperature': data[1], 'humidity': data[2], 'time': data[3]}
    else:
        data_dict = "There is no real-time data at the current time"
    return data_dict


@app.route("/temperature")
def temperature_picture():
    # 从数据库中获取温度的最新时间的HTMl文件路径，然后进行渲染
    # Get the HTML file path of the latest time of temperature from the database, and then render it
    sql = "SELECT tfile  FROM path WHERE `time` = ( SELECT MAX( `time` ) AS result FROM path );"
    r = search.delay(sql)
    d = result(r)
    if len(d) > 0:
        file_name = d[0][0]
        print(file_name)
        return render_template(file_name)
    else:
        return "No picture"


@app.route("/co2")
def co2_picture():
    # Get the HTML file path of the latest time of co2 from the database, and then render it
    sql = "SELECT cfile  FROM path WHERE `time` = ( SELECT MAX( `time` ) AS result FROM path );"
    r = search.delay(sql)
    d = result(r)
    if len(d) > 0:
        file_name = d[0][0]
        print(file_name)
        return render_template(file_name)
    else:
        return "No picture"


@app.route("/humidity")
def humidity_picture():
    # Get the HTML file path of the latest time of humidity from the database, and then render it
    sql = "SELECT rfile  FROM path WHERE time = ( SELECT MAX( time ) AS result FROM path );"
    r = search.delay(sql)
    d = result(r)
    if len(d) > 0:
        file_name = d[0][0]
        print(file_name)
        return render_template(file_name)
    else:
        return "No picture"


@app.route("/real/<name>")
def web(name):
    if name == "温度.html":
        return render_template("real/温度.html")
    elif name == "二氧化碳浓度.html":
        return render_template("real/二氧化碳浓度.html")
    elif name == "湿度.html":
        return render_template("real/湿度.html")
    elif name == "contact.html":
        return render_template("real/contact.html")
    elif name == "index.html":
        return render_template("real/index.html")
    else:
        return "No"


@app.route("/favicon.ico", methods=["GET", "HEAD"])
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='favicon.ico')


@app.route("/static/<name>", methods=["GET", "HEAD"])
def lib(name):
    return send_from_directory(os.path.join(app.root_path, 'static'), name)


@app.route("/static/images/<name>", methods=["GET", "HEAD"])
def images_lib(name):
    return send_from_directory(os.path.join(app.root_path, 'static/images'), name)


@app.route("/static/js/<name>", methods=["GET", "HEAD"])
def js_lib(name):
    return send_from_directory(os.path.join(app.root_path, 'static/js'), name)


if __name__ == "__main__":
    file_path = os.path.join(os.path.abspath('.'), 'templates')
    if not os.path.exists(file_path):
        os.mkdir(file_path)
    set_config('other', 'flask_path', file_path)
    server = make_server('0.0.0.0', 4350, app)
    server.serve_forever()
