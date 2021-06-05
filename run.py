#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import hashlib
import datetime
from argparse import ArgumentParser
import undetected_chromedriver.v2 as uc
from pprint import pprint
import mimetypes
from email import message_from_file
from email.header import decode_header
from email.utils import parseaddr,parsedate
TEMP_DICT = {
    'file_name': '',  # 离线文件名
    'eml_size': '',  # 邮件大小
    'subject': '',  # 邮件主题
    'sender': '',  # 发送人
    'receiver': '',  # 收件人
    'date': '',     #发件日期
    'cc': '',  # 抄送
    'attachment_name': '',  # 附件
    'attach_size': '',  # 附件大小
    'attach_md5': ''  # 附件md5值
}


def current_file(path='input',file_lists=[]):
    """
    遍历文件-包括子文件夹下的文件
    :return:
    """

    for target in os.listdir(path):
        target_path = path + '/' + target
        if os.path.isdir(target_path):
            current_file(target_path,file_lists)
        if os.path.isfile(target_path):
            file_lists.append(target_path)
    return file_lists


def calc_md5(files):
    """
    输入：文件路径的list
    输出：md5的字典。每个元素为：{路径名：md5值}
    :param files:
    :return:
    """
    md5dict = {}

    for file in files:
        with open(file, 'rb') as fp:
            data = fp.read()

        file_md5 = hashlib.md5(data).hexdigest()
        md5dict[file] = file_md5
    return md5dict



def read_mail(eml_path='mail/helloworld2.eml'):
    """
    输入：邮件地址
    输出：json（邮件的信息）
    :param target:
    :return:
    """
    def msg_date(msg_date):
        date_list = [str(i) for i in parsedate(msg_date)][:-3]
        year = date_list[:1]

        day = date_list[1:3]
        time = date_list[3:]
        date_str = "{}-{} {}".format(year[0],"-".join(day),":".join(time))
        return date_str


    def get_FileSize(filePath):
        fsize = os.path.getsize(filePath)
        fsize = fsize / float(1024 * 1024)
        return round(fsize, 3)


    mail_info = TEMP_DICT
    if os.path.exists(eml_path):
        with open(eml_path) as f:
            msg = message_from_file(f)
            print(msg.keys())
            mail_info['subject'] =  msg["Subject"]
            mail_info['receiver'] = parseaddr(msg.get('To'))[1]
            mail_info['sender'] = parseaddr(msg.get('From'))[1]
            mail_info['cc'] = parseaddr(msg.get('Cc'))[1]
            mail_info['date'] =  msg_date(msg['Date'])
            mail_info['eml_size'] = "{}MB".format(get_FileSize(eml_path))
            pprint(mail_info)
            for part in msg.walk():
                if part.get_content_maintype() == 'multipart':continue
                filename = part.get_filename() #获取附件
                # print(msg.keys())



                if filename:
                    print(filename)



if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-target',nargs=1,help=u'选择目标目录')
    parser.add_argument('-default',action="store_true",help=u'默认模式，读取当前目录下input文件夹')
    args = parser.parse_args()


    if args.target:
        all_files = current_file(args.target[0])

    if args.default:
        all_files = current_file()
        print(calc_md5(all_files))

    read_mail()
