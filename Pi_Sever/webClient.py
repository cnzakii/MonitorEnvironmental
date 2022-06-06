import asyncio
import websockets
from scd30_i2c import SCD30
import time

scd30 = SCD30()
scd30.set_measurement_interval(5)
scd30.start_periodic_measurement()
time.sleep(5)

IP_ADDRESS = "43.138.132.187"
IP_PORT = "8080"

#此方法是得到传感器数据
def get_data():
    global data
    if scd30.get_data_ready():
        m = scd30.read_measurement()
        if m is not None:
            data = f"{m[0]:.2f},{m[1]:.2f},{m[2]:.2f}"
            return data
            time.sleep(5)
    else:
        return data
        time.sleep(0.2)

# 向服务器端发送消息
async def client_send(websocket):
    while True:
        data = get_data()
        await websocket.send(data)
        time.sleep(5)


# 进行websocket连接
async def client_run():
    ipaddress = IP_ADDRESS + ":" + IP_PORT
    async with websockets.connect("ws://" + ipaddress, ping_interval=None) as websocket:
        await client_send(websocket)


# main function
if __name__ == '__main__':
    print("======client main begin======")
    asyncio.get_event_loop().run_until_complete(client_run())