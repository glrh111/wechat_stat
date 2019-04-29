# WeChat Group Message Stat

This repo is intended to collect messages with filter, 
and export those info.

[![LICENSE](https://img.shields.io/badge/license-MIT%20(The%20996%20Prohibited%20License)-blue.svg)](https://github.com/996icu/996.ICU/blob/master/LICENSE)

[
![GitHub watchers](https://img.shields.io/github/watchers/glrh111/wechat_stat.svg)
![GitHub stars](https://img.shields.io/github/stars/glrh111/wechat_stat.svg)
![GitHub forks](https://img.shields.io/github/forks/glrh111/wechat_stat.svg)
![GitHub issues](https://img.shields.io/github/issues/glrh111/wechat_stat.svg)
![GitHub last commit (branch)](https://img.shields.io/github/last-commit/glrh111/wechat_stat.svg)
](https://github.com/glrh111/wechat_stat)

## Description

### base

+ python 3
+ wxpy
+ pyinstaller

### export format

Export format could be csv like below:
```
time(Asia/Shanghai),group_id,group_name,from_id,from_nickname,content_type,content
2019-04-29 11:49:30,8d**89,交大投更搭,e37930,SKEHFGSE,a,a
2019-04-29 11:51:31,8d**89,交大投更搭,e37930,SKEHFGSE,Picture,
2019-04-29 11:51:43,8d**86,交大投更搭,e37930,SKEHFGSE,Text,[捂脸]
2019-04-29 11:51:48,8d**89,交大投更搭,e37930,SKEHFGSE,Text,😳
```

### release

`pyinstaller -F src/wechat_stat.py -i assert/favicon.ico`

notice
+ just `ico`

### run

+ `python wechat_stat.py` in `src`
+ or run `.exe` in `dist`

notice
+ press severl `Enter` may take effort when the program not respond

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
