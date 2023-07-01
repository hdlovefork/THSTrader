# coding=utf-8

import logging
import os
from logging.handlers import RotatingFileHandler

LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")
LOG_FILE_SIZE_LIMIT = os.getenv("LOG_FILE_SIZE_LIMIT", 10)
LOG_FILE_COUNT_LIMIT = os.getenv("LOG_FILE_COUNT_LIMIT", 10)

log = logging.getLogger("PYTHS")
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(threadName)s - %(message)s')
log.setLevel(LOG_LEVEL)

# 控制台输出
console_handler = logging.StreamHandler()
console_handler.setLevel(LOG_LEVEL)
console_handler.setFormatter(formatter)

# 文件输出
if not os.path.exists('logs'):
    # 如果不存在则创建logs目录
    os.mkdir('logs')
file_size = int(LOG_FILE_SIZE_LIMIT) * 1024 * 1024
file_count = int(LOG_FILE_COUNT_LIMIT)
file_handler = RotatingFileHandler('logs/app.log', maxBytes=file_size, backupCount=file_count)
file_handler.setLevel(LOG_LEVEL)
file_handler.setFormatter(formatter)

log.addHandler(console_handler)
log.addHandler(file_handler)
