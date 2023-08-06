import argparse
from agent import DataMakerAgentCreator
from logs import log


def get_args():
    parser = argparse.ArgumentParser(description='SQL Data Maker CLI', add_help=False)


    # 添加参数选项
    parser.add_argument('database', nargs='?', help='Name of the database')


    parser.add_argument('-h', '--host', dest='host', metavar='host', help='Connect to host.')
    parser.add_argument('-u', '--user', dest='user', metavar='user', help='User for login')
    parser.add_argument('-p', '--password', dest='password', nargs='?', const='name',
                        help='Password to use when connecting to server. If password is not given, it\'s asked from the tty.')
    parser.add_argument('-P', '--port', dest='port', type=int, default=3306,
                        help='Port number to use for connection, default (3306).')
    parser.add_argument('--help', action='help',
                        help='Show this help message and exit.')  # 添加自定义的帮助选项

    # 解析命令行参数
    args = parser.parse_args()
    return args


def get_db_uri_from_args(args):
    db_host = args.host or "127.0.0.1"
    db_port = int(args.port) or 3306
    db_user = args.user or "root"
    db_password = args.password or ""
    db_name = args.database or "test"

    db_uri = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    return db_uri

if __name__ == "__main__":

    args = get_args()
    db_uri = get_db_uri_from_args(args)

    creator = DataMakerAgentCreator(db_uri)

    while True:

        # request = "生成一个看病挂号系统的数据库，并插入测试数据"
        request = input("""
e.g. 创建一个考勤系统的数据库，并插入测试数据
     生成一个具有挂号、看病、开药、住院功能的医院系统的数据库，并插入测试数据
     生成一个具备用户注册、登录、发帖、评论、点赞、关注、私信功能的社交网站的数据库，并插入测试数据
     创建一个具备用户登录，购买，支付，评论功能的电商网站的数据库，并插入测试数据，每张表不少于2000条
     对 user 表生成1000条测试数据
     对 user 和 book 表各生成1000条测试数据
     根据 user 和 product 表的数据，生成 1000 条 order 表的数据

请输入命令：""")


        with creator.get_llm_callback() as cb:
            creator.agent.run(request)
            log.llm_billing(request, cb)