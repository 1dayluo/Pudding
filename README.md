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

输出：

-   全部邮件信息（`.json`)

-   所有带有附件的邮件信息(`.json`)

-   md5(`.json`) <u>待优化</u>

    

输出示例：

````json

{
    "attach": [
        {
            "attach_name": "test.tar",
            "attach_md5": "59dea35cdf6ae0d1faf8ecfa85fd1b55",
            "attach_size": "0.236MB",
            "addition": [
                {
                    "filename": "13qzx1.png",
                    "md5": "3ed83a02e9de4f0f90aabcc4188e81e4",
                    "size": "0.234MB"
                }
            ]
        },
        {
            "attach_name": "test(1).tar",
            "attach_md5": "8af090d03ae366c5e761d9ec9e9d9d7a",
            "attach_size": "0.106MB",
            "addition": [
                {
                    "filename": "9f124a2fb89871dde11bbd7b5743ccfd06e81b42.jpg",
                    "md5": "36ebe2522b8343d341a7e1200fe4d7cf",
                    "size": "0.105MB"
                }
            ]
        },
        {
            "attach_name": "test(2).tar",
            "attach_md5": "e422de5ab0afe00439e9aa7878f1521d",
            "attach_size": "0.45MB",
            "addition": [
                {
                    "filename": "7bd9ec968738adcc41608ba680c6bafd461ab41172c79-2uao3R.png",
                    "md5": "f56b15c04531e66f7e15a23689f425c9",
                    "size": "0.448MB"
                }
            ]
        }
    ],
    "subject": "attach_files",
    "receiver": "*@qq.com",
    "sender": "*@foxmail.com",
    "cc": "*@qq.com",
    "date": "2021-6-5 22:49:32",
    "eml_size": "1.089MB",
    "file_name": "attach_test2.eml"
}
````



### Todo

-   [x] md5计算

-   [x] eml读取，提取基础信息（收件人，发件人，cc）

-   [x] eml附件信息(差一个rar的)

-   [x] 解决附件名称一样的情况

-   [ ] 邮件内url

-   [ ] 爬虫查找md5 有无历史记录

    

## 运行说明

````bash
usage: run.py [-h] [-mail MAIL] [-md5 MD5] [-md5default]

optional arguments:
  -h, --help   show this help message and exit
  -mail MAIL   input path of dir,and read all format of eml files
  -md5 MD5     choice target dir
  -md5default  default，read input file

````

