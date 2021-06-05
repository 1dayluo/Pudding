#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import hashlib
import datetime
import json
from argparse import ArgumentParser

from pprint import pprint
from collections import Counter
import mimetypes
import gzip,tarfile,zipfile,py7zr
import undetected_chromedriver.v2 as uc
from email import message_from_file
from email.header import decode_header,Header
from email.utils import parseaddr,parsedate


MAIL_OUTPUT_DIR = 'Attachment'
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
        print(os.getcwd())
        with open(file, 'rb') as fp:
            data = fp.read()

        file_md5 = hashlib.md5(data).hexdigest()
        md5dict[file] = file_md5
    return md5dict


def _dir(path):
    if os.path.isdir(path):
        pass
    else:
        os.mkdir(path)
    return path

def get_FileSize(filePath):
    """
    获取文件大小 单位：MB
    :param filePath:
    :return:
    """
    fsize = os.path.getsize(filePath)
    fsize = fsize / float(1024 * 1024)
    return round(fsize, 3)


def save_attach(attach_name,data,mail_info):
    attachment_info = {}
    check_type = attach_name.split('.')[-1]
    save_path = MAIL_OUTPUT_DIR + '/' + '[{}]'.format(mail_info['file_name']) + attach_name

    if not os.path.exists(MAIL_OUTPUT_DIR):
        os.mkdir(MAIL_OUTPUT_DIR)

    with open(save_path,'wb') as f:
        f.write(data)

    attachment_info['attach_name'] = attach_name
    attachment_info['attach_md5'] = hashlib.md5(data).hexdigest()
    attachment_info['attach_size'] = "{}MB".format(get_FileSize(save_path))
    attachment_info['addition'] = []
    add_dict = {}

    if check_type in ['zip','tar','gz','7z']: #压缩包类型

        # archive_dir = _dir(MAIL_OUTPUT_DIR + '/' + 'Archive')



        extarct_dir = _dir(MAIL_OUTPUT_DIR + '/' + attach_name.split('.')[:-1][0])


        if check_type == 'zip':
            zip_file = zipfile.ZipFile(save_path)
            with zip_file:
                for names in zip_file.namelist():
                    names_path = extarct_dir + '/' + names
                    zip_file.extract(names, extarct_dir)
                    add_dict['filename'] = names
                    add_dict['md5'] = calc_md5([names_path]).get(names_path)
                    add_dict['size'] = '{}MB'.format(get_FileSize(names_path))
                    attachment_info['addition'].append(add_dict)


        if check_type == 'rar':
            pass
        if check_type == 'tar':
            tar_file = tarfile.open(save_path)

            with tar_file:
                for names in tar_file.getnames():
                    names_path = extarct_dir + '/' + names
                    tar_file.extract(names, extarct_dir)
                    add_dict['filename'] = names
                    add_dict['md5'] = calc_md5([names_path]).get(names_path)
                    add_dict['size'] = '{}MB'.format(get_FileSize(names_path))
                    attachment_info['addition'].append(add_dict)

        if check_type == '7z':

            sevenz_file = py7zr.SevenZipFile(save_path)
            with sevenz_file:
                os.chdir(extarct_dir)
                for names in sevenz_file.getnames():
                    names_path = extarct_dir + '/' + names
                    # os.mkdir(names)
                    sevenz_file.extract('.',names)
                    add_dict['filename'] = names
                    add_dict['md5'] = calc_md5([names]).get(names)
                    add_dict['size'] = '{}MB'.format(get_FileSize(names))
                    attachment_info['addition'].append(add_dict)
            os.chdir('../..')


    return attachment_info

def read_mail(eml_path='mail/extarct_file.eml'):
    """
    输入：邮件地址
    输出：json（邮件的信息）
    :param target:
    :return:
    """
    def msg_date(msg_date):
        """
        mail日期
        :param msg_date:
        :return:
        """
        date_list = [str(i) for i in parsedate(msg_date)][:-3]
        year = date_list[:1]

        day = date_list[1:3]
        time = date_list[3:]
        date_str = "{}-{} {}".format(year[0],"-".join(day),":".join(time))
        return date_str





    mail_info = {}
    mail_info['attach'] = []

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
            mail_info['file_name'] = eml_path.split('/')[-1]
            attach_name_list = []
            for part in msg.walk():
                if part.get_content_maintype() == 'multipart':continue
                filename = part.get_filename() #获取附件
                # print(msg.keys())

                if filename:
                    savename = filename

                    if filename in attach_name_list:
                        # print(Counter(attach_name_list)[filename])

                        savename = ''.join(filename.split('.')[:-1]) + '(' + str(Counter(attach_name_list)[filename]) + ').' + ''.join(filename.split('.')[-1:])


                    data = part.get_payload(decode=True)
                    attachment_info  = save_attach(savename, data, mail_info)

                    attach_name_list.append(filename)
                    mail_info['attach'].append(attachment_info)

            pprint(mail_info)

        return mail_info

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-mail',nargs=1,help=u'input path of dir,and read all format of eml files')
    parser.add_argument('-md5',nargs=1,help=u'choice target dir')
    parser.add_argument('-md5default',action="store_true",help=u'default，read input file')
    args = parser.parse_args()


    if args.md5:
        all_files = current_file(args.target[0])

    if args.md5default:
        all_files = current_file()
        print(calc_md5(all_files))
    if args.mail:
        files = current_file(args.mail[0])
        mails = [] # all
        mails_attach = [] # has attach
        md5list = []
        for file in files:
            mail_info = read_mail(file)
            mails.append(mail_info)
            if mail_info.get('attach') :
                if len(mail_info.get('attach')) > 0:
                    mails_attach.append(mail_info)

                    md5list.extend([ {attach['attach_name'] :attach['attach_md5']} for attach in mail_info['attach']])


        with open('all_mail.json','w',encoding='utf-8') as f:
            json.dump({'data': mails}, f, ensure_ascii=False, indent=2)

        with open('attach_mail.json','w',encoding='utf-8') as f:
            json.dump({'data': mails_attach, 'md5list': md5list}, f, ensure_ascii=False,indent=2)


        with open('md5list.json','w',encoding='utf-8') as f:
            json.dump({'md5list': md5list}, f, ensure_ascii=False, indent=2)