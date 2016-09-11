# -*- coding: utf-8 -*-
from Queue import Queue, Empty
from threading import Thread
from time import sleep
from sohu import Storage, URLTool
import sys


_sentinel = object()


def check_url(url_queue, data_queue, level):
    storage = Storage()
    while True:
        url, curr_level = url_queue.get()
        if url is _sentinel:
            break
        if url not in storage and curr_level <= level:
            storage.add(url)
            data_queue.put((url, curr_level))
    print "check down"


def handle(url_queue, data_queue, level, thread_id):
    try:
        while True:
            url, curr_level = data_queue.get(timeout=5)
            tool = URLTool(url)
            page = tool.open()
            print "Thread" + thread_id, url, curr_level

            if hasattr(sys, "exc_clear"):
                sys.exc_clear()
            if curr_level < level:
                for _url in tool.matched_urls(page):
                    url_queue.put((_url, curr_level + 1))
    except Empty:
        url_queue.put((_sentinel, 0))
        print "Thread %s down" % thread_id
    except Exception as e:
        print e.message


if __name__ == '__main__':
    url_queue = Queue()
    data_queue = Queue()
    url_queue.put(("http://m.sohu.com/", 0))
    target_level = 1
    t1 = Thread(target=check_url, args=(url_queue, data_queue, target_level))
    t1.start()
    sleep(1)
    thread_num = 4
    for i in range(thread_num):
        Thread(target=handle, args=(url_queue, data_queue, target_level, str(i))).start()
