# coding: utf-8
# word.py
# Created by Bayonet on 2016/1/14.

import sys
import threading
import socket
from World import WordPress
from World import Error
import xmlrpclib
import wordpress_xmlrpc

logFile = open('Error.log', 'a')
reload(sys)
sys.setdefaultencoding('utf-8')

FileText = open('500.txt', 'rU')
Text = FileText.readlines()
urls = []
lock = threading.Lock()

# 最大线程数
Maxthreading = 10
# 最大超时时间
MaxTimeOut = 3
socket.timeout = MaxTimeOut


def start(text):
    TextList = text.split()
    try:
        wp = WordPress.worldpress(TextList[1], TextList[2], 'http://' + TextList[0] + '/xmlrpc.php')
        wp.run()
    except Error.worldError:
        print '[-] 标题获取成功, 但未取到病种!'
        print >> logFile, '[-] 标题获取成功, 但未取到病种! http://www.' + TextList[0]
    except socket.timeout:
        print '[-] 连接超时 文章发送失败!'
        print >> logFile, '[-] 报告爷 连接超时 文章发送失败! http://www.' + TextList[0]
    except socket.error:
        print '[-] 网站找不到主机 http://www.' + TextList[0]
        print >> logFile, '[-] 报告爷网站找不到主机 http://www.' + TextList[0]
    except UnboundLocalError:
        print '[-] POST 数据错误' + TextList[0]
        print >> logFile, '[-] POST 数据错误' + TextList[0]
    except xmlrpclib.Error:
        print '[-] xmlrpclib 数据错误 http://www.' + TextList[0]
        print >> logFile, '[-] xmlrpclib 数据错误 http://www.' + TextList[0]
    except wordpress_xmlrpc.InvalidCredentialsError:
        print '[-] 用户或密码错误 http://www.' + TextList[0]
        print >> logFile, '[-] 用户或密码错误 http://www.' + TextList[0]
    except RuntimeError:
        print '[-] 发送失败 http://www.' + TextList[0]


def func():
    tContext = []
    for i in range(0, Maxthreading):
        text = urls[0]
        del urls[0]
        # 开启多线程处理数据
        thread = threading.Thread(target=start, args=(text,))
        tContext.append(thread)
        thread.start()

    for t in tContext:
        t.join()
    try:
        print urls[0]
    except IndexError:
        main()


def main():
    # 每次去除 Maxthreading 个数据
    if len(urls) < Maxthreading:
        for i in range(0, Maxthreading):
            try:
                # 取出第一个数据并删除第一个数据
                text = Text[0]
                del Text[0]
                urls.append(text)
            except IndexError:
                # 如果索引错误 则退出程序
                exit()
        main()
    else:
        print len(urls)
        func()


if __name__ == '__main__':
    main()
