# -*- coding: utf-8 -*-
''''''
import scrapy
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import re
import time
from random import randint
from threading import Thread


'''
firefox_options = Options()
firefox_options.add_argument('--headless')
driver = webdriver.Firefox(firefox_options=firefox_options, firefox_profile=None)
driver.get('https://item.jd.com/4845275.html')
time.sleep(randint(5, 7))
# 点击页面中的评论选项
for i in range(0, 10):
    print('1')
    a = driver.find_element_by_xpath("//div[@class='item ellipsis']").text
    if re.match('.*(手机壳).*', a):
        continue
    else:
        print('2')
'''
'''
# 这是使用asyncio模块进行编程的例子
import asyncio

async def get_html(url):
    print("start the url")
    asyncio.sleep(2)
    print("end get url")
    return "lawaiter"


if __name__ == "__main__":
    start = time.time()
    loop = asyncio.get_event_loop()
    task = [get_html("www") for i in range(10)]
    tasks = loop.create_task(asyncio.gather(*task))
    loop.run_forever()
    print(time.time() - start)
    print(tasks.result())
'''
'''
# 这是取消future(task)的例子
import asyncio
import time

async def get_html(url):
    print("waiting")
    await asyncio.sleep(url)
    print("do after {}s".format(url))

if __name__ == "__main__":
    task1 = get_html(2)
    task2 = get_html(3)
    task3 = get_html(4)

    tasks = [task1, task2, task3]

    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(asyncio.wait(tasks))
    except KeyboardInterrupt:
        all_tasks = asyncio.Task.all_tasks()
        for task in all_tasks:
            print("cancal task")
            print(task.cancel())
        loop.stop()
        loop.run_forever()
    finally:
        loop.close()
'''

import asyncio

'''
def callback(sleep):
    print("sleep_time {} sccess".format(sleep))
    
# 这是使用call_soon的例子, call_later是在指定的时间之后运行某个回调函数
# call_at是在loop.time()，即为单调时间上面的函数，即为内部的时钟时间
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.call_soon(callback, 2)
    loop.run_forever()
'''

# 这是使用asyncio模拟Http请求的例子
# asyncio 没有提供http协议的需求


# 这是处理已经排序的序列，使用bisect模块处理排序的序列
"""
import bisect

inter_list = []
bisect.insort(inter_list, 13)
bisect.insort(inter_list, 12)
print(bisect.bisect(inter_list, 13))
"""




from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0


firefox_options = Options()
firefox_options.add_argument('--headless')

# Create a new instance of the Firefox driver
driver = webdriver.Firefox(firefox_options=firefox_options)

# go to the google home page
driver.get("http://www.baidu.com")
driver.find_elements_by_class_name('div')
pass