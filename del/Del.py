#  -*- coding:utf-8 -*-
# Del.py
# Created by Bayonet on 2016/1/14.

import wordpress_xmlrpc
import sys
import threading
import socket
import xmlrpclib

logFile = open('Error.log', 'a')
reload(sys)
sys.setdefaultencoding('utf-8')

FileText = open('500.txt', 'rU')
Text = FileText.readlines()
urls = []
lock = threading.Lock()

# 最大线程数
Maxthreading = 20
# 最大超时时间
MaxTimeOut = 3
socket.timeout = MaxTimeOut


def GetTitle(text):
    textList = text.split()
    try:
        try:
            wp = wordpress_xmlrpc.Client('http://www.' + textList[0] + '/xmlrpc.php', textList[1], textList[2])
            # 获取前100个帖子
            getPost = wordpress_xmlrpc.methods.posts.GetPosts({'orderby': 'post_modified', 'number': 100})
            post = wp.call(getPost)
        except socket.error:
            print '[-] 报告爷网站找不到主机 http://www.' + textList[0]
            print >> logFile, '[-] 报告爷网站找不到主机 http://www.' + textList[0]
        try:
            # 如果没有获取到数据 则不处理
            if not post == []:
                # 如果有数据
                for i in post:
                    # 删除hello 文章
                    # if wp.call(wordpress_xmlrpc.methods.posts.DeletePost(1)):
                    # 删除全部文章
                    if wp.call(wordpress_xmlrpc.methods.posts.DeletePost(i.id)):
                        print '[+] 报告爷 删除成功!\t' + textList[0]
                    else:
                        print '[-] 报告爷 删除失败!\t' + textList[0]
                        print >> logFile, '[-] 报告爷 删除失败!\t'
            else:
                print '[+] 报告爷 文章已被删除!\t' + textList[0]
        except UnboundLocalError:
            print '[-] POST 数据错误' + textList[0]
            print >> logFile, '[-] POST 数据错误' + textList[0]
    except xmlrpclib.Error:
        print '[-] xmlrpclib 数据错误 http://www.' + textList[0]
        print >> logFile, '[-] xmlrpclib 数据错误 http://www.' + textList[0]
    except wordpress_xmlrpc.InvalidCredentialsError:
        print '[-] 用户或密码错误 http://www.' + textList[0]
        print >> logFile, '[-] 用户或密码错误 http://www.' + textList[0]


def func():
    tContext = []
    for i in range(0, Maxthreading):
        text = urls[0]
        del urls[0]
        # 开启多线程处理数据
        thread = threading.Thread(target=GetTitle, args=(text,))
        tContext.append(thread)
        thread.start()

    for t in tContext:
        t.join()
    try:
        print urls[0]
    except IndexError:
        main()


def main():
    # 每次去除 5个数据
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
