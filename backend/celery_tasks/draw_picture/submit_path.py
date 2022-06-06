import os
from .. import *


def submit(root, arr):
    # 将路径名添加到数据库中
    # Add pathname to database
    sql = "INSERT INTO `path` VALUES(NOW(),'%s','%s','%s') " % (arr[0], arr[1], arr[2])
    update.delay(sql)

    # 查找将一天前的文件的路径
    # Find the path to the file that will be one day ago
    sql = "SELECT `tfile`,`cfile`,`rfile` FROM `path` WHERE `time` < DATE_SUB(NOW(),INTERVAL 1 DAY );"
    d = a_search(sql)

    # 判断是否有一天前的数据
    # Determine whether there is data from a day ago
    if len(d) > 0:
        # 删除文件
        # Delete file
        delete(root, d)
        # 删除数据库中的相关数据
        # Delete relevant data in the database
        sql = "DELETE FROM `path` WHERE `time` < DATE_SUB(NOW(),INTERVAL 1 DAY );"
        update.delay(sql)


# Delete file
def delete(root, d):
    for x in range(len(d)):
        for y in range(len(d[0])):
            # path
            path = d[x][y]
            my_file = os.path.join(root, path)
            if os.path.exists(my_file):
                os.remove(my_file)
