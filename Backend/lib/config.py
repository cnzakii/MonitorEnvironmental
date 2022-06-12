from configparser import ConfigParser
import os


# **********
# 此文件中保存的是对配置文件的操作
# What is saved in this file is the operation on the configuration file
# **********

# 此方法读取配置文件
# This method reads the configuration file
def read_config(section):
    conn = ConfigParser()
    # 获取配置文件的路径
    # Get the path of the configuration file
    file_path = os.path.join(os.path.abspath('..'), 'db_config.ini')
    if not os.path.exists(file_path):
        raise FileNotFoundError
    # 读取配置文件
    # Read configuration file
    conn.read(file_path)
    # 获取该section下的所有键值对，用k_v保存并返回
    # Obtain all key value pairs under the section, and use K_ V save and return
    options = conn.options(section)
    k_v = {}
    for i in range(len(options)):
        value = conn.get(section, options[i])
        k_v.setdefault(options[i], value)
    return k_v


# 修改配置
# Modify configuration
def set_config(section, option, value):
    conn = ConfigParser()
    file_path = os.path.join(os.path.abspath('..'), 'db_config.ini')
    if not os.path.exists(file_path):
        raise FileNotFoundError
    conn.read(file_path)
    now = value
    # 判断是否要修改配置
    # Determine whether to modify the configuration
    flag = False
    # 判断是否存在该section
    # Determine whether the section exists
    if not conn.has_section(section):
        conn.add_section(section)
        flag = True
    # 判断是否存在该option
    # Determine whether the option exists
    elif not conn.has_option(section, option):
        flag = True
    # 判断是否对应的值是否变化
    # Judge whether the corresponding value changes
    else:
        last = conn.get(section, option)
        if last != now:
            conn.remove_option(section, option)
            flag = True

    if flag:
        conn.set(section, option, now)
        conn.write(open(file_path, 'w'))
