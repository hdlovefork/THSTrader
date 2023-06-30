# coding=utf-8

import logging
import os
from logging.handlers import RotatingFileHandler

LOGLEVEL = os.getenv("LOGLEVEL", "DEBUG")

log = logging.getLogger("PYTHS")
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(threadName)s - %(message)s')
log.setLevel(LOGLEVEL)

console_handler = logging.StreamHandler()
console_handler.setLevel(LOGLEVEL)
console_handler.setFormatter(formatter)

# 如果不存在logs目录则创建
if not os.path.exists('logs'):
    os.mkdir('logs')
file_handler = RotatingFileHandler('logs/app.log', maxBytes=100000000, backupCount=10)  # 最大100MB，保留3个备份文件
file_handler.setLevel(LOGLEVEL)
file_handler.setFormatter(formatter)

log.addHandler(console_handler)
log.addHandler(file_handler)
