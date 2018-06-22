#!/usr/bin/env python2
# -*- coding:utf-8 -*-

import pymysql


class FtpFile(object):
    """
    This is a model with common used methods
    include add delete update and query
    """

    def __init__(self):
        '''db connection'''
        self.__conn = pymysql.connect(
            host='127.0.0.1', user='root', passwd='root', db='ftp_file',
            cursorclass=pymysql.cursors.DictCursor)
        self.cursor = self.__conn.cursor()

    def getChildrenById(self, pid):
        '''find the children of the giving id in the table'''
        sql = "select * from ftp_file where pid = %s and status = 1"
        self.cursor.execute(sql, pid)
        return self.cursor.fetchall()

    def addRecord(self, data):
        '''add the record to the table'''
        sql = "insert into ftp_file (`pid`,`file_name`,`modify_time`,`md5` , \
        `is_dir` , `status` , `archive_id`,`vault_id`,`file_size` ,  \
        `add_time`) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        self.cursor.execute(sql, data)
        self.__conn.commit()
        return self.cursor.lastrowid

    def modifyRecord(self, data, id):
        '''update the record which has be modified'''
        sql = "update ftp_file set modify_time=%s , md5 = %s , archive_id = \
             %s , vault_id = %s , file_size = %s where id = " + str(id)
        self.cursor.execute(sql, data)
        self.__conn.commit()

    def markAsDel(self, id):
        '''mark the record as deleted'''
        sql = "update ftp_file set status=-1 where id = %s"
        self.cursor.execute(sql, id)
        self.__conn.commit()

    def getDetailById(self, id):
        '''get the detail info in the oas by id'''
        sql = "select * from ftp_file where id = %s"
        self.cursor.execute(sql, id)
        return self.cursor.fetchone()

    def __del__(self):
        self.cursor.close()
        self.__conn.close()
