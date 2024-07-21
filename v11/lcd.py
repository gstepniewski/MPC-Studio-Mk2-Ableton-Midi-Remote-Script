import concurrent.futures

import json
import http.client

import logging
from threading import Timer
logger = logging.getLogger(__name__)

class Config:
    PORT = 6727

class Cache:
    BIG = ""
    SMALL = ""
    timer = None


def run_script(big, small):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.submit(run_script_sync, big, small)


def run_script_sync(big, small):
    request = {'big': big, 'small': small}
    headers = {"Content-Type": "application/json"}
    conn = http.client.HTTPConnection("localhost", port=Config.PORT)
    conn.request("POST", "/", body=json.dumps(request), headers=headers)
    conn.close()


def show_lcd_message_2(big, small):
    if Cache.timer is not None:
        Cache.timer.cancel()
    Cache.BIG = big
    Cache.SMALL = small
    run_script(big, small)


def show_lcd_message(single):
    show_lcd_message_2(single, '')


def show_lcd_dialog_2(big, small):
    run_script(big, small)
    if Cache.timer is not None:
        Cache.timer.cancel()
    Cache.timer = Timer(2.0, show_lcd_message_2, (Cache.BIG, Cache.SMALL))
    Cache.timer.start()


def show_lcd_dialog(single):
    show_lcd_dialog_2(single, '')
