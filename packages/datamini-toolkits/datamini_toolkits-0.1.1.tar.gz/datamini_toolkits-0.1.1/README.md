# An AI-First toolkit for Data
@DataMini

## 简介 | Introduction
一个基于AI的数据工具包，用于数据的生成、清洗、分析、可视化等工作。


### SQL Data Maker
第一个工具叫 sql-data-maker，用于生成测试数据。
目前仅支持MySQL数据库，后续会支持更多的数据库。

```bash
sql-data-maker

e.g. 创建一个考勤系统的数据库，并插入测试数据
     生成一个具有挂号、看病、开药、住院功能的医院系统的数据库，并插入测试数据
     生成一个具备用户注册、登录、发帖、评论、点赞、关注、私信功能的社交网站的数据库，并插入测试数据
     创建一个具备用户登录，购买，支付，评论功能的电商网站的数据库，并插入测试数据，每张表不少于2000条
     对 user 表生成1000条测试数据
     对 user 和 book 表各生成1000条测试数据
     根据 user 和 product 表的数据，生成 1000 条 order 表的数据

请输入命令：创建一个考勤系统的数据库，并插入测试数据

```


## 使用方法 | Usage

### 1. 安装 | Installation

`pip install datamini_toolkits`

### 2. 配置参数 | Config

系统的环境变量中增加OPENAI的参数，如果在国内访问，建议配置HTTP代理
```bash
EXPORT OPENAI_API_KEY=sk-bMZ92NKosdfsFCHwsdfssaaawerFJAy4bsdfHiyVgjMFol2
EXPORT OPENAI_HTTP_PROXY=http://127.0.0.1:8001
```


### 3.1 运行命令行工具 | Run Command Line

```bash
$ sql-data-maker --help
usage: sql-data-maker [-h name] [-u name] [-p [PASSWORD]] [-P PORT] [--help] [database]

Command line argument parser

positional arguments:
  database              Database name

options:
  -h name, --host name  Connect to host.
  -u name, --user name  User for login
  -p [PASSWORD], --password [PASSWORD]
                        Password to use when connecting to server. If password is not given, it's asked from the tty.
  -P PORT, --port PORT  Port number to use for connection, default (3306).
  --help                Show this help message and exit.


```

#### 日志 | Log

程序运行的日志文件在当前目录下
- llm.log: 用于记录访问大模型的Prompt和返回的Completion
- db.log: 用于记录数据库的SQL和Response
- llmbilling.log: 用于记录OpenAI的计费情况



### 3.2 开发者 | For Developer
```python

```
