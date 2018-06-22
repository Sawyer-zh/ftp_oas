#!/usr/bin/env python2
# -*- coding:utf-8 -*-

import os
from ftp_file import FtpFile
from oas.ease.vault import Vault
from oas.oas_api import OASAPI
import hashlib
import time


class BackUpLogic(object):
    """backup logic class"""
    # current directory name
    oasConf = {
        'server_host': '',
        'access_key_id': '',
        'access_key_secret': ''
    }
    vaultConf = {
        'vault_id': '',
        'vault_name': '',
    }

    # stack to store the directory
    __dirStack = ['srv']
    # __dirStack = ['Users', 'fx', 'wwwroot', 'ftp_oas']

    def __init__(self):
        self.__ftpFile = FtpFile()
        self.initOas()

    @property
    def baseDir(self):
        '''get current directory by directory stack'''
        return '/' + '/'.join(self.__dirStack) + '/'

    def initOas(self):
        '''initialize oas api'''
        api = OASAPI(self.oasConf['server_host'],
                     self.oasConf['access_key_id'],
                     self.oasConf['access_key_secret'])
        self.__vault = Vault.get_vault_by_id(api, self.vaultConf['vault_id'])

    def backUp(self, pid):
        '''backup current directory recrusively'''
        current = self.__ftpFile.getDetailById(pid)
        self.__dirStack.append(current['file_name'])
        files = self.__ftpFile.getChildrenById(pid)
        kept = self.checkAddOrDel(files, pid)
        if kept:
            self.procModify(kept)

    def checkAddOrDel(self, files, pid):
        '''check current directory add or missing'''
        current = self.__dirStack[-1]
        now = os.listdir(self.baseDir)
        # hold the missing and remain file or dir
        missed = []
        kept = []
        for item in files:
            if item['file_name'] not in now:
                missed.append(item)
            else:
                kept.append(item)
                now.remove(item['file_name'])
        if len(now) > 0:
            self.procAdd(now, pid)
            self.__dirStack.append(current)
        if len(missed) > 0:
            self.procDel(missed)
            self.__dirStack.append(current)
        if len(kept) > 0:
            return kept
        else:
            self.__dirStack.pop()
            return False

    def procDel(self, missed):
        '''process deleted files or directory recrusively'''
        for item in missed:
            if item['is_dir'] == 1:
                self.__ftpFile.markAsDel(item['id'])
                subMissed = self.__ftpFile.getChildrenById(item['id'])
                self.__dirStack.append(item['file_name'])
                self.procDel(subMissed)
            else:
                self.oasDel(item['archive_id'])
                self.__ftpFile.markAsDel(item['id'])
        self.__dirStack.pop()

    def procAdd(self, remainFiles, pid):
        '''process added files or directory recrusively'''
        for item in remainFiles:
            absolutePath = self.baseDir + item
            modifyTime = (int)(os.path.getmtime(absolutePath))
            addTime = (int)(time.time())
            if os.path.isdir(absolutePath):
                data = (pid, item, modifyTime, '', 1, 1, '',
                        self.vaultConf['vault_id'], 0, addTime)
                subPid = self.__ftpFile.addRecord(data)
                subRemainFiles = os.listdir(absolutePath)
                if subRemainFiles:
                    self.__dirStack.append(item)
                    self.procAdd(subRemainFiles, subPid)
            else:
                archiveId = self.oasUpload(absolutePath)
                fileSize = (int)(os.path.getsize(absolutePath))
                md5 = self.getFileMd5(absolutePath)
                data = (pid, item, modifyTime, md5, 0, 1, archiveId,
                        self.vaultConf['vault_id'], fileSize, addTime)
                self.__ftpFile.addRecord(data)
        self.__dirStack.pop()

    def procModify(self, kept):
        '''process modified files or directory recrusively'''
        for item in kept:
            absolutePath = self.baseDir + item['file_name']
            modifyTime = (int)(os.path.getmtime(absolutePath))
            if os.path.isdir(absolutePath):
                data = (modifyTime, '', '', self.vaultConf['vault_id'], 0)
                self.__ftpFile.modifyRecord(data, item['id'])
                self.backUp(item['id'])
            else:
                if (int)(os.path.getmtime(absolutePath)) \
                        != item['modify_time'] and \
                        self.getFileMd5(absolutePath) \
                        != item['md5']:
                    archiveId = self.oasUpload(absolutePath)
                    fileSize = (int)(os.path.getsize(absolutePath))
                    md5 = self.getFileMd5(absolutePath)
                    data = (modifyTime, md5, archiveId,
                            self.vaultConf['vault_id'], fileSize,)
                    self.__ftpFile.modifyRecord(data, item['id'])
                    self.oasDel(item['archive_id'])
        self.__dirStack.pop()

    def oasUpload(self, fileName):
        '''process upload to oas '''
        # print 'upload' + fileName
        return self.__vault.upload_archive(fileName)

    def oasDel(self, archiveId):
        '''process delete in oas'''
        # print 'delete' + archiveId
        self.__vault.delete_archive(archiveId)

    def getFileMd5(self, fileName):
        '''get md5 of a file'''
        if not os.path.isfile(fileName):
            return
        fileHash = hashlib.md5()
        f = open(fileName, 'rb')
        while True:
            b = f.read(8096)
            if not b:
                break
            fileHash.update(b)
        f.close()
        return fileHash.hexdigest()

    def getArchive(self, archiveId, filePath):
        ''' download file to given filepath through archive_id'''
        job = self.__vault.retrieve_archive(archiveId)
        job.download_to_file(filePath)

    def getRestorePath(self, id):
        ''' restore to the original path'''
        dirStack = []
        thisDetail = self.__ftpFile.getDetailById(id)
        while thisDetail and thisDetail['id'] != 1:
            dirStack.append(thisDetail['file_name'])
            thisDetail = self.__ftpFile.getDetailById(thisDetail['pid'])
        dirStack.reverse()
        return '/srv/' + '/'.join(dirStack)


if __name__ == '__main__':
    back = BackUpLogic()
    back.backUp(1)
