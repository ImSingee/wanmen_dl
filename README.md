# 某某培训机构视频下载器

## 配置 Token 与下载路径

修改 config.py 文件，Authorization 的内容修改为电脑登录后 localstorage 中 authorization 的值

修改 main.py 文件，DOWNLOAD_TO 为下载路径，TO_DOWNLOAD_COURSE_ID 和 TO_DOWNLOAD_COURSE_NAME 分别为课程 ID 和课程名，课程 ID 来源为电脑端课程播放页面 `https://www.wanmen.org/courses/aaa/lectures/bbb` 中的 `aaa` 部分

## 下载

直接 `python3 main.py`


## 后台下载

本程序采用单进程单线程的方式，并未针对后台下载做特殊优化。如需可参考 https://github.com/ImSingee/mashibing_dl 中的相关脚本自行编写

## 免责声明

该脚本来源于网络，并非本人编写，本人从未对该培训机构和相关的视频加密提供方进行逆向工程，本人也从未使用过该脚本

该脚本的发布仅为学习使用，本人不承担使用者的行为所带来的任何法律后果

该脚本使用 [No License](https://choosealicense.com/no-permission/) 协议发布，版权人未知，因此任何人都不得对该项目进行修改、拷贝、分发、用于商业用途
