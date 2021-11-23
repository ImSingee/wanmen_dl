# 某某培训机构视频下载器

## 配置 Token 与下载路径

创建 config.json 文件，写入类似下面的内容

```json
{
    "Authorization":"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjVhYTFkM2U5MWUwM2UzNzkxODg2NjJlNyIsImlhdCI6MTYzNjg4Njk3NiwiZXhwIjoxNjM5NDc4OTc2LCJpc3MiOiJ1cm46YXBpIn0.SUNiOJ7cM-ngFb7Yb9qSq5nAEiuUL2oQ5WWtr91_ONQ",
    "DownloadTo": "/path/to/dir"
}
```

Authorization 的内容修改为电脑登录后 localstorage 中 authorization 的值
DownloadTo 的内容修改为下载目标路径

## 下载

直接 `./download [课程ID] [课程名]`

课程 ID 来源为电脑端课程播放页面 `https://www.wanmen.org/courses/aaa/lectures/bbb` 中的 `aaa` 部分
课程名可以任意填写，意义为上一步配置的 DownloadTo 中的子目录名


## 后台下载

本程序采用单进程单线程的方式，并未针对后台下载做特殊优化。如需后台下载请使用 tmux + ./download 脚本进行

## 免责声明

该脚本来源于网络，并非本人编写，本人从未对该培训机构和相关的视频加密提供方进行逆向工程，本人也从未使用过该脚本

该脚本的发布仅为学习使用，本人不承担使用者的行为所带来的任何法律后果

该脚本使用 [No License](https://choosealicense.com/no-permission/) 协议发布，版权人未知，因此任何人都不得对该项目进行修改、拷贝、分发、用于商业用途
