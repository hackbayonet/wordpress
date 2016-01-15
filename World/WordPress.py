# coding: utf-8
# WordPress.py
# Created by Bayonet on 2016/1/12.

import wordpress_xmlrpc
import urllib2
import re
import random
import MySQLdb
import socket
from World import Error
import threading
from wordpress_xmlrpc.methods.posts import NewPost

lock = threading.Lock()

conn = MySQLdb.connect(host="192.168.0.126", user="root", passwd="", db="medical", charset="utf8")
cursor = conn.cursor()

# 发帖成功 记录位置
okFile = open('OK.log', 'a')


class worldpress():
    def __init__(self, user, pwd, host):
        self.user = user
        self.pwd = pwd
        self.host = host

        # 帖子内容
        self.title = ''
        self.content = ''
        # 病种
        # self.cdz = ['抽动症百科,抽动症人群,医院新闻,医患互动']

    def Post(self):
        """@Doc:发送帖子"""
        wp = wordpress_xmlrpc.Client(self.host, self.user, self.pwd)
        post = wordpress_xmlrpc.WordPressPost()
        post.title = self.title
        post.content = self.content
        post.post_status = 'publish'
        """
        # 栏目ID
        # post.taxonomy = self.entity
        # post.terms_names = {
        #    'post_tag': [self.entity],
        #    # 'category': ['多动症常识', '治疗多动症的医生']
        # }
        """
        id = wp.call(NewPost(post))
        host = self.host.replace('xmlrpc.php', '')
        if not id:
            raise RuntimeError("POST Send failed")
        else:
            print '[+] 报告爷 帖子发送成功' + host + str(id) + '.html'
            print >> okFile, '[+] 报告爷 帖子发送成功' + host + str(id) + '.html'

    def GetPost(self):
        """@Doc:获取全部帖子数"""
        pass

    def GetTitle(self):
        """@doc: 判断病种关键字"""
        try:
            host = self.host.replace('xmlrpc.php', '')
            req = urllib2.Request(host, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64)'})
            title = re.findall('<title>(.*)</title>', urllib2.urlopen(req, timeout=5).read())[0]
            lock.acquire()
            if re.search('多动症', title):
                self.GetData('ddz')
            elif re.search('自闭症', title):
                self.GetData('zbz')
            elif re.search('遗尿症', title):
                self.GetData('ynz')
            elif re.search('抽动症', title):
                self.GetData('cdz')
            elif re.search('智力低下', title):
                self.GetData('zldx')
            elif re.search('发育迟缓', title):
                self.GetData('fych')
            else:
                raise Error.worldError('Get Title Ok, Failed to match the disease')
            lock.release()
        except socket.timeout:
            raise

    def GetData(self, entity):
        sql = "select title,content from " + entity + ';'
        n = cursor.execute(sql)
        sql = "select title, content from " + entity + " where id=" + str(random.randint(0, n)) + ';'
        n = cursor.execute(sql)
        SqlData = cursor.fetchmany()
        try:
            self.title = SqlData[0][0]
            self.content = SqlData[0][1]
        except IndexError:
            self.GetData(entity)

    def run(self):
        self.GetTitle()
        self.Post()
