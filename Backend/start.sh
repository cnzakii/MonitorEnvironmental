#!/bin/sh
cd celery_tasks
nohup celery -A async_tasks worker -B >out_beat.log 2>&1 &
nohup celery -A async_tasks flower >out_flower.log 2>&1 &
cd ..
cd Pi_Sensor
nohup python -u server.py >out_server.log 2>&1 &
cd ..
cd flask_front
nohup python -u app.py >out_front.log 2>&1 &
