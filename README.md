# 🍮Pudding

## About

邮件自动化工具，负责邮件分析(Get the Base Info of email,Categorize mail )

-   邮件基础信息
    -   主题
    -   发送者
    -   收件人
    -   CC
    -   有无附件
    -   邮件内容中的url提取
-   邮件归档（目前设置为以有无附件进行归档条件）

额外功能：

-   任意文件md5计算
-   md5网站搜索有无



>   对于附件的处理
>
>   -   提取附件从邮件中
>   -   计算附件md5
>       -   对于压缩包格式的邮件，会先解压
>       -   普通附件，直接计算md5



参考TEMP：

````python

TEMP_DICT = {
    'file_name': '',  # 离线文件名
    'mail_size': '',  # 邮件大小
    'subject': '',  # 邮件主题
    'sender': '',  # 发送人
    'receiver': '',  # 收件人
    'cc': '',  # 抄送
    'attachment': '',  # 附件
    'attach_size': '',  # 附件大小
    'attach_md5': ''  # 附件md5值
}

````



### Todo

-   [x] md5计算

-   [x] eml读取，提取基础信息（收件人，发件人，cc）

-   [ ] eml附件信息

-   [ ] 爬虫

    

## 运行说明

