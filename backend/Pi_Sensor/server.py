import sys
sys.path.append('..')
import asyncio
import websockets
from lib import read_config
from celery_tasks import update_arr

IP_ADDRESS = read_config('ecs').get("intranet_ip")
IP_PORT = "8080"


# 接收数据
# receive data
async def server_run(websocket):
    while True:
        message = await websocket.recv()
        # 分割数据
        # Split data
        arr = message.split(",")
        co2 = float(arr[0])
        temp = float(arr[1])
        rh = float(arr[2])
        sql0 = "INSERT INTO `data` VALUES(NOW(),%f,%f,%f) " % (co2, temp, rh)
        sql1 = "DELETE FROM `data` WHERE `time` < DATE_SUB(NOW(),INTERVAL 1 DAY ) "
        update_arr.delay([sql0, sql1])



# main function
if __name__ == '__main__':
    print("======server main begin======")
    # 等待客户端的连接。如果连接成功，返回一个websocket
    server = websockets.serve(server_run, IP_ADDRESS, IP_PORT, ping_interval=None)
    asyncio.get_event_loop().run_until_complete(server)
    asyncio.get_event_loop().run_forever()
