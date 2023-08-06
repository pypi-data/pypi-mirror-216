import sys

from langchain.sql_database import SQLDatabase
from langchain.sql_database import sqlalchemy
from langchain.chat_models import ChatOpenAI

from tools import parse_sql_script, check_function_creation
from logs import log

class ChatOpenAIWithLog(ChatOpenAI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self, text: str, **kwargs) -> str:
        rst = super().predict(text=text, **kwargs)
        log.llm(text, rst)
        return rst


# new SQLDatabase Object with log
class SQLDatabaseWithLog(SQLDatabase):
    def __init__(self, *args, **kwargs):
        try:
            super().__init__(*args, **kwargs)
        except sqlalchemy.exc.OperationalError as e:
            log.error(f"连接数据库失败，请检查参数是否正确。{e.orig or e}")
            sys.exit(1)


        if not check_function_creation(self):
            log.error(f"数据库参数 log_bin_trust_function_creators 未设置为 ON，无法使用该功能。"
                  f"如何设置：https://github.com/DataMini/datamini_toolkits/blob/main/toolkits/mock_data/HELP.md"
                  f"#log_bin_trust_function_creators-%E6%9C%AA%E8%AE%BE%E7%BD%AE%E4%B8%BA-1")
            sys.exit(1)

    def run(self, command: str, **kwargs):
        rst = super().run(command=command, **kwargs)
        log.db(command, rst)
        return rst

    def run_multi_sql_script(self, sql_script: str):
        rsts = []
        sqls = parse_sql_script(sql_script)
        for sql in sqls:
            _rst = self.run(sql)
            rsts.append(_rst)
        return rsts
