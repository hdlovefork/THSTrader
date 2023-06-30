# coding=utf-8

import logging
import os

LOGLEVEL = os.getenv("LOGLEVEL", "DEBUG")

log = logging.getLogger("PYTHS")
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log.setLevel(LOGLEVEL)

console_handler = logging.StreamHandler()
console_handler.setLevel(LOGLEVEL)
console_handler.setFormatter(formatter)

file_handler = logging.FileHandler('app.log')
file_handler.setLevel(LOGLEVEL)
file_handler.setFormatter(formatter)

log.addHandler(console_handler)
log.addHandler(file_handler)
