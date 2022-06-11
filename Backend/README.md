# CS183FZ-19th-Backend

## Author

- #### Name: Chen Zikang

- #### Email: zikang.chen.2022@mumail.ie



## Tech Stack

**Client:** websocket

**Server:** websocket , celery , flask , RabbitMQ , MySQL



## Project structure

There is one under the same level directory The contents of the files at the end of `.ximd` are the same as these, but they are more intuitive, so ==I recommend you to see <u>***structure.ximd***</u> file==

```bash
(py39) [root@VM-12-10-centos home]# tree backend
backend
├── celery_tasks
│   ├── draw_picture
│   │   ├── draw.py
│   │   ├── __init__.py
│   │   ├── picture_template.py
│   │   └── submit_path.py
│   ├── async_tasks.py
│   ├── curb.py
│   ├── __init__.py
│   ├── result.py
│   └── test.py
├── flask_front
│   ├── app.py
│   ├── static
│   └── templates
│       └── real
├── lib
│   ├── config.py
│   └── __init__.py
├── Pi_Sensor
│   └── server.py
├── db_config.ini
└── start.sh
```

### celery_tasks

```bash
(py39) [root@VM-12-10-centos backend]# tree celery_tasks
celery_tasks
├── async_tasks.py
├── curb.py
├── draw_picture
│   ├── draw.py
│   ├── __init__.py
│   ├── picture_template.py
│   └── submit_path.py
├── __init__.py
└── result.py
```

- #### Function

  Execute asynchronous and scheduled tasks through **celery** (a distributed framework)

- #### async_tasks.py

  Create the celery object, configure the broker (message middleware, using **RabbitMQ**), bank (the way to store results, using "rpc//"), and beat (regularly draw the environment trend graph)

- #### curb.py

  Encapsulate and register the database operation as a task, which improves the running efficiency

- #### draw_picture

  - ##### draw.py ( Scheduled task )

    Read the database data and pass these data and other necessary parameters into picture_template.py

  - ##### picture_template.py

    Receive the data and necessary parameters, draw the environment trend chart, and save it in the templates folder of flask_ front

  - ##### submit_path.py

    Receive the file name and submit it to the `path` table of the `data` database

- #### result.py

  When you run an asynchronous task, you will get a unique ID, The job is to judge the task status through the ID and return the result

### flask_front

```bash
(py39) [root@VM-12-10-centos backend]# tree flask_front
flask_front
├── app.py
└── templates
```

- #### Function

  This is a server that receives front-end messages and returns corresponding data

- #### app.py

  Create a server through the flask framework, and send real-time data and rendered environment trend graph to the front end

- #### static

  Save the necessary static files for the web page ,  such as : css, js ....

- #### templates

  Save environment trend chart file and static files for the web page

### lib

```bash
(py39) [root@VM-12-10-centos backend]# tree lib
lib
├── config.py
└── __init__.py
```

- #### Function

  Self created tool class, used to read configuration files and operate on databases

- #### config.py

  Reading and modifying configuration files

### Pi_Sensor

```bash
(py39) [root@VM-12-10-centos backend]# tree Pi_Sensor
Pi_Sensor
└── server.py
```

- #### Function

  As a server, it receives sensor data sent by the client (raspberry pie)

- #### server.py

  Use WebSockets to implement a long connection with the client, and submit the received data to the database

## Environment Variables

To run this project , you need to build a python environment that contains all the following dependencies (it is recommended to use [anaconda](https://www.anaconda.com/products/distribution#Downloads) to build a virtual environment)

### Versions

#### Language&Framework

```basic
python                    3.9.12
flask                     2.1.2
celery                    5.2.7
```

#### MySQL

```basic
mysql                     5.6.50-log
```

#### RabbitMQ

```basic
RabbitMQ                  3.10.2
Erlang                    24.3.4
```

#### Other dependencies

```basic
asyncio                   3.4.3
flask-cors                3.0.10
flask-sqlalchemy          2.5.1 
pyecharts                 1.9.1
pymysql                   1.0.2
flower                    1.0.0
jinja2                    3.1.2 
```

### Port

⚠️Make sure that the computer or server port is open and free , if a port must be modified, please go to the corresponding file for modification

| Port |              Explain              |
| :--: | :-------------------------------: |
| 4350 |       Server(app) -- app.py       |
| 8080 | Server(raspberry pi) -- server.py |
| 3306 |      MySQL -- db_config.ini       |
| 5555 |        Monitoring( flower)        |


## Run Locally

### Get project files

Extract the file from the **zip** or pull the project from the **GitHub**

```bash
  git clone https://github.com/zk1528437521/pythonProject.git
```

Go to the project directory

```bash
  cd Backend
```



### Set up the MySQL database

You can run <u>***data.sql***</u> file, which is used to create tables 

⚠️this file only contains structures and no data



### update configuration

Open db_config file to update configuration

⚠️The relevant configuration must be filled in correctly to ensure the successful operation of the project

```ini
# **********
# This document is a configuration file
# Including database and RabbirMQ information, 
# server information, HTML file storage address, etc
# **********

# The following is the database information, please fill it in manually!!!!
# In sequence: database address, port, user name, password, database name, character 
[mysql]
host = localhost
port = 3306
user = 
password = 
database = 
charset = utf8

# The following is the IP information of the ECS. Please fill it in manually!!!
[ecs]
public_ip = 
intranet_ip = 

# The following is the RabbitMQ information, please fill it in manually!!!!
# In sequence: User name, password, address, port and virtual host name
[rabbitmq]
user = 
password = 
host = localhost
port = 5672
v_host = 

#The following is other information, such as the upper level path for storing the environment trend chart, which will be automatically generated or modified by the program!!!!!!
[other]
flask_path = 
```

### Run start.sh file

```bash
  sh start.sh
```



