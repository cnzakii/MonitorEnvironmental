import os
import sys

sys.path.append('../..')
sys.path.append('..')
from datetime import datetime
from . import submit_path
from lib import config
from . import picture_template
from celery_tasks import cel, a_search


@cel.task(ignore_result=True)
def task():
    root = config.read_config('other').get('flask_path')
    arr = []
    # 接收文件路径，并检查文件是否存在，只有存在才能加入数据库
    # Receive the file path and check whether the file exists.
    # Only if it exists can it be added to the database
    temp = temp_pictures()
    if temp != -1:
        if os.path.exists(os.path.join(root, temp)):
            arr.append(temp)

    co2 = co2_pictures()
    if co2 != -1:
        if os.path.exists(os.path.join(root, co2)):
            arr.append(co2)

    rh = rh_pictures()
    if rh != -1:
        if os.path.exists(os.path.join(root, rh)):
            arr.append(rh)
    if len(arr) == 3:
        submit_path.submit(root, arr)
    else:
        delete(root, arr)
    print('画图完成时间 %s' % datetime.now())


def delete(root, arr):
    for i in range(len(arr)):
        # path
        path = arr[i]
        my_file = os.path.join(root, path)
        if os.path.exists(my_file):
            os.remove(my_file)


# 处理数据
def process(t):
    use_list = []
    x = 0
    while x < len(t[0]):
        arr = []
        y = 0
        while y < len(t):
            arr.append(t[y][x])
            y += 1
        use_list.append(arr)
        x += 1
    return use_list


# 绘制 温度图
# Draw temperature picture
def temp_pictures():
    sql = "SELECT `temperature`, `time`  FROM `data` WHERE`time`>DATE_SUB(NOW(),INTERVAL 24 HOUR);"
    t = a_search(sql)
    if len(t) > 0:
        total = process(t)
        x_data = total[1]
        y_data = total[0]

        background = (
            "new echarts.graphic.LinearGradient(0, 0, 0, 1, "
            "[{offset: 0, color: '#e28744'}, {offset: 1, color: '#cede9f'}], false)"
        )
        file_name = datetime.now().strftime("%Y-%m-%d %H:%M:00") + "-temperature.html"
        # 传入数据，调色方案，标题，文件名 ，得到HTML文件
        # Incoming data, color scheme, title, file name, get HTML file
        picture_template.draw(x_data, y_data, background, 'Temperature Monitoring', 'temperature/°C', file_name)
        return file_name
    else:
        return -1


# 绘制 二氧化碳图
# Draw carbon dioxide picture
def co2_pictures():
    sql = "SELECT `co2`,`time`  FROM `data`WHERE`time`>DATE_SUB(NOW(),INTERVAL 24 HOUR);"
    t = a_search(sql)
    if len(t) > 0:
        total = process(t)
        x_data = total[1]
        y_data = total[0]
        background = (
            "new echarts.graphic.LinearGradient(0, 0, 0, 1.1, "
            "[{offset: 0, color: '#13547a'}, {offset: 1, color: '#80d0c7'}], false)"
        )
        file_name = datetime.now().strftime("%Y-%m-%d %H:%M:00") + "-co2.html"
        picture_template.draw(x_data, y_data, background, 'Carbon Dioxide Monitoring', 'CO₂/ppm', file_name)
        return file_name
    else:
        return -1


# 绘制 湿度图
# Draw humidity picture
def rh_pictures():
    file_name = datetime.now().strftime("%Y-%m-%d %H:%M:00") + "-humidity.html"
    sql = "SELECT `humidity`, `time` FROM `data` WHERE`time`>DATE_SUB(NOW(),INTERVAL 24 HOUR);"
    t = a_search(sql)
    if len(t) > 0:
        total = process(t)
        x_data = total[1]
        y_data = total[0]
        background = (
            "new echarts.graphic.LinearGradient(0, 0, 0, 1, "
            "[{offset: 0, color: '#5d6c81'}, {offset: 1, color: '#afc9fa'}], false)"
        )
        picture_template.draw(x_data, y_data, background, 'Humidity Monitoring', 'rh/%', file_name)
        return file_name
    else:
        return -1
