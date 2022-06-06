from configparser import ConfigParser
import os


# **********
# 此文件中保存的是对配置文件的操作
# **********

# 此方法读取配置文件
def read_config(section):
    conn = ConfigParser()
    # 获取配置文件的路径
    file_path = os.path.join(os.path.abspath('..'), 'db_config.ini')
    if not os.path.exists(file_path):
        raise FileNotFoundError
    # 读取配置文件
    conn.read(file_path)
    # 获取该section下的所有键值对，用k_v保存并返回
    options = conn.options(section)
    k_v = {}
    for i in range(len(options)):
        value = conn.get(section, options[i])
        k_v.setdefault(options[i], value)
    return k_v


# 修改配置文件
def set_config(section, option, value):
    file_path = os.path.join(os.path.abspath('..'), '../db_config.ini')
    conn = ConfigParser()
    conn.read(file_path)
    now = value
    flag = False  # 是否要修改配置文件的标志
    # 判断是否存在该section
    if not conn.has_section(section):
        conn.add_section(section)
        conn.set(section, option, now)
        flag = True
    # 判断是否存在该option
    elif not conn.has_option(section, option):
        conn.set(section, option, now)
        flag = True
    # 判断是否对应的值是否变化
    else:
        last = conn.get(section, option)
        if last != now:
            conn.remove_option(section, option)
            conn.set(section, option, now)
            flag = True
    if flag:
        conn.write(open(file_path, 'w'))
