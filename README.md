# WeChat Group Message Stat

## Description

### base

+ python 3
+ wxpy

### function 

This repo is intended to collect messages with filter, 
and export those info.

### export format

Export format could be csv like below:
```
time(Asia/Shanghai),group_id,group_name,from_id,from_nickname,content_type,content
2019-04-29 11:49:30,8d**89,交大投更搭,e37930,SKEHFGSE,a,a
2019-04-29 11:51:31,8d**89,交大投更搭,e37930,SKEHFGSE,Picture,
2019-04-29 11:51:43,8d**86,交大投更搭,e37930,SKEHFGSE,Text,[捂脸]
2019-04-29 11:51:48,8d**89,交大投更搭,e37930,SKEHFGSE,Text,😳
```

### Release

### run

+ `python wechat_stat.py` in `src`
+ run `.exe` in `dist`

### import csv to Excel

+ open Excel and new a file
+ click `Data`
+ click `from text`
+ choose csv file
+ choose `seperator` and `65001: Unicode(UTF-8)`, click `next step`
+ choose only(!) `comma`
+ click `complete`

notice
+ copy csv before open it, or new messages won't be written
+ etc
