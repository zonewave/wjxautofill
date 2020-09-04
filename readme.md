
### 批量自动填写  问卷星互填问卷列表的问卷



##### v1.0:

运行环境：python3.7+selenium+chromedriver
运行路径：release/v1_0

运行方式：打开config.ini,设置自己问卷星的账户密码和自己要发送的问卷id（可以在个人问卷中心查找到)。

打开命令行，输入
python autofill.py
即可自动运行

##### go_v1.0
运行环境： windows+chromedriver
注意： 需要根据chrome的版本号[下载](http://npm.taobao.org/mirrors/chromedriver/)对应版本chromedrver, 并且加入到环境变量PATH里去。

运行方式：

需要填写配置文件 conf.toml
username:账户， password ：密码，  mutalid：个人发送的问卷ID

1. 下载执行文件，双击运行 2.源码编译运行，需要安装go编译器
