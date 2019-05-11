# # -*- coding: utf-8 -*-
# # @Time    : 4/14/2019 13:46
# # @Author  : MARX·CBR
#  @File    : 多进程.py
# from multiprocessing import Process
# import time
#
#
# def test(name):
#     print("%s is running " % name)
#     time.sleep(2)
#     print('%s is done' % name)
#
# def run():
#     for i in range(2,35):
#         print(i)
#
#
# if __name__ == '__main__':
#     # 在windows系统之上，开启子进程的操作一定要放在这下面
#     # Process(target=test,kwargs={'name':'monicx'})
#     p = Process(target=test, args=('monicx',))
#     p.start()  # 向操作系统发送一个请求，操作系统会申请内存空间给，然后把父进程的数据拷贝给子进程，作为子进程的初始数据。
#     print('=======主')
#     run()


# -*- coding: utf-8 -*-
# @Time    : 4/14/2019 12:43
# @Author  : MARX·CBR
# @File    : __init__.py.py
import multiprocessing

import requests
from bs4 import BeautifulSoup
import re
import time
import lxml


class DownloadPexelSpider:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
            'cookie': '__cfduid=d6abd7c099adcbbee835df61de3e6ef3c1555167983; locale=en-US; _ga=GA1.2.1156545351.1555167990; _gid=GA1.2.1239065177.1555167990; pexels_auth=true; remember_user_token=W1sxMTMzOTU1XSwiJDJhJDEwJDZ0LlBsMWxyVkhwY3lYbS9UdlludmUiLCIxNTU1MTY4MDYzLjI4MzI4NzMiXQ%3D%3D--24ba6f9dec0d1f96e9aace28d6ba68061db32ada; _fbp=fb.1.1555168539454.2076601344; _pexels_session=YlNzcnZDTGhvNG1IUUlmUnRQQ080OENZZy9tZW1aUUU0RE1vSjJWSVBDb1loaFJ4bHlpWk5MYk9zNW1QVHdBMWJSMGVqcXlNdkl6NnAyT00vTG9FbTFuMS96N0U4Y1FNTjJBcGk3SjhteFlGdi8zSjgrZUhHQzNJd2l3aHJ3RHdJQnBCRWluRVdZakpVU2p2d2xIc0JnRkxqMHJRRjhHRlBwWjVjdml2Yml5UHhva29nQTJwblpORkV6dzRiYWQ1aUgwVnhOSUlyTHJDSXg3aVJEVUhxakg5N29FODQ1eDBYQWVabjlyd1oxRjVnWVpIWXFOVjRoQkVhb1B3MWtXTy0tc2IvRm0zdWorcTkxSm11c05QcjBydz09--c43adb3bc514ed6f627cc5f6e01eaafcfc58468b',
        }
        self.download_image_url = []
        self.raw_url = []
        self.session = requests.session()

    def change_page(self, page):
        ou = 'https://www.pexels.com/search/desktop%20wallpaper/?format=js&seed=2019-04-14%2004%3A22%3A06%20%2B0000&dark=true&page={}&type='.format(
            page)
        r = self.session.get(
            ou,
            headers=self.headers)
        print(ou)
        r.encoding = r.apparent_encoding
        data = r.text
        pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')  # 匹配模式
        url = re.findall(pattern, data)
        print(url)
        for i in url:
            if 'dl' in i:
                if i not in self.raw_url:
                    print("准备插入",i)
                    self.raw_url.append(i)
        print(self.raw_url)

        thr=[]


        for g in self.raw_url:
            try:
                thr.append(self.get_download(g))
            except:
                print('error', g)

        # def do_something(i):
        #     time.sleep(i)
        #     print
        #     'good:%d' % i
        #     return 'good:%d' % i

        print(multiprocessing.cpu_count())
        pool = multiprocessing.Pool(processes=4)
        result = pool.map(self.single_file_download, thr)
        pool.close()
        pool.join()


    def get_download(self, url):
        # tt='https://images.pexels.com/photos/2116222/pexels-photo-2116222.jpeg?cs=srgb&amp;dl=chair-furniture-indoors-2116222.jpg&amp;fm=jpg'
        tt = url
        newtt = tt[:41:].replace("images", 'www').replace('photos', 'photo')
        print(newtt)
        r = self.session.get(newtt, headers=self.headers)
        # print(r.text)
        soup = BeautifulSoup(r.text, 'lxml')
        for k in soup.findAll('input'):
            if k.get('name') == 'download-size':
                size = k.get('value')
                size = size.split('x')
                if int(size[0]) > 1920:
                    structure = "?dl&fit=crop&crop=entropy&w={}&h={}".format(size[0], size[1])
                    print('查找成功')
                    self.download_image_url.append(tt + structure)
                    return (tt + structure)
                    # self.single_file_download(tt + structure)
                    break

    def single_file_download(self, url):
        i = url.replace('\\', '').replace('\'', '')
        print(i)
        name = i[33:39:]
        w = i[-11:-7:]
        print("准备下载", i)
        with open('./images/{}_{}.png'.format(name, w), 'wb') as f:
            raw = self.session.get(i, headers=self.headers)
            content = raw.content
            f.write(content)
        i = i[:-11:] + "1920&h=1080"
        with open('./images/{}_1920.png'.format(name, w), 'wb') as f:
            raw = self.session.get(i, headers=self.headers)
            content = raw.content
            f.write(content)

        print("{}下载完毕".format(name))
        # print(self.download_image_url)
        # while len (self.download_image_url) != 0:
        #     print("ok ",self.download_image_url)
        #     for i in self.download_image_url:

        # while 1:

    def download_image(self):
        print(self.download_image_url)
        while len(self.download_image_url) != 0:
            print("ok ", self.download_image_url)
            for i in self.download_image_url:
                i = i.replace('\\', '').replace('\'', '')
                print(i)
                name = i[33:39:]
                w = i[-11:-7:]
                print("准备下载", i)
                with open('{}_{}.png'.format(name, w), 'wb') as f:
                    raw = self.session.get(i, headers=self.headers)
                    content = raw.content
                    f.write(content)
                i = i[:-11:] + "1920&h=1080"
                with open('{}_1920.png'.format(name), 'wb') as f:
                    raw = self.session.get(i, headers=self.headers)
                    content = raw.content
                    f.write(content)

                print("{}下载完毕".format(name))
        # while 1:

    def run(self, s, e):
        # Windows 平台要加上这句，避免 RuntimeError

        for i in range(s, e + 1):
            # self.pool.apply_async(self.download_image, args=())
            print(self.change_page(i))


if __name__ == '__main__':
    DownloadPexelSpider().run(21, 30)
    # multiprocessing.freeze_support()
    # obj = DownloadPexelSpider()
    # p = Process(target=obj.download_image, args=())
    # p.start()  # 向操作系统发送一个请求，操作系统会申请内存空间给，然后把父进程的数据拷贝给子进程，作为子进程的初始数据。
    # print("父进程启动")
    # obj.run()
    # print("父进程启动")
    #
    # # 创建进程池,Pool默认为CPU核心数
    # pp = Pool(2)
    #    # 创建进程，放入进程池统一管理
    # pp.apply_async(obj.run(), args=())
    # pp.apply_async(obj.download_image(), args=())
    # print(pp)
    # # 进程池在调动join之前必须先调动close，调用close之后就不能再继续添加新的进程了
    # pp.close()
    # pp.join()
    #
    # print("父进程结束")

    # obj.run()
    # p = Process(target=obj.download_image())
    # p.start()
    # p.join()
    # pool = multiprocessing.Pool()
    # cpus = multiprocessing.cpu_count()
    # for i in range(0, cpus):
    #     result = pool.apply_async(obj.run(), args=())
    #     result = pool.apply_async(obj.download_image(), args=())
    # pool.close()
    # pool.join()

# #obj.run()
# threads = []
# t1 = threading.Thread(target=obj.run(), )
# threads.append(t1)
# t2 = threading.Thread(target=obj.download_image(), )
# threads.append(t2)
# print(threads)
# threads[1].setDaemon(True)
# threads[1].start()
#
# time.sleep(10)
# threads[0].setDaemon(True)
# threads[0].start()

# for t in threads:
#     t.setDaemon(True)
#     t.start()
# threads[0].setDaemon(True)
# threads[0].start()
# time.sleep(10)
# t2 = threading.Thread(target=obj.download_image, )
# threads.append(t2)
# threads[1].setDaemon(True)
# threads[1].start()
# soup = BeautifulSoup(data, 'lxml')
# print(soup.findAll('div'))
# https://www.pexels.com/photo/2116222/
# https://www.pexels.com/photos/2116222/
# 2116222


