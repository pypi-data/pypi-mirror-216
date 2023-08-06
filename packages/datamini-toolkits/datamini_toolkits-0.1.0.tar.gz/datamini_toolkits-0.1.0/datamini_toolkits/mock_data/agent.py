import os
from datetime import datetime

from langchain.callbacks import get_openai_callback
from langchain.agents import initialize_agent, AgentType
from langchain.agents.tools import Tool
from langchain.memory import ConversationBufferMemory
from langchain.chains import SQLDatabaseChain


from prompts import RECORD_CREATOR_PROMPT_TEMPLATE, TABLE_CREATOR_PROMPT_TEMPLATE, SCHEMA_DESIGNER_PROMPT_TEMPLATE
from base import ChatOpenAIWithLog, SQLDatabaseWithLog
from logs import log



class DataMakerAgentCreator(object):
    def __init__(self, db_uri):

        self.db_uri = db_uri

        self.db = SQLDatabaseWithLog.from_uri(self.db_uri, sample_rows_in_table_info=2)

        self.llm = ChatOpenAIWithLog(temperature=0, model_name="gpt-3.5-turbo", max_tokens=2000)
        self.llm.openai_proxy = os.environ.get("OPENAI_HTTP_PROXY", None)
        self.get_llm_callback = get_openai_callback

        self.db_chain = SQLDatabaseChain.from_llm(self.llm, self.db, verbose=True)
        memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

        self.agent = initialize_agent(tools=self.tools,
                                      llm=self.llm,
                                      agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
                                      verbose=True,
                                      memory=memory)


    @property
    def tools(self):
        return [
            Tool.from_function(
                func=self.data_record_maker,
                name="Data Record Maker Tool",
                description="用于向给定的表（Table）中生成一定数量的数据（Record）"
                            "输入格式为： TABLE_NAME: ROWS_TO_GENERATE，多个表之间用英文逗号分隔。"
                            "比如：table001: 100, table002: 100",
            ),
            Tool.from_function(
                func=self.data_schema_maker,
                name="Data Schema Maker Tool",
                description="useful for when you need to design and create tables "
                            "in SQL database using business scene. "
                            "比如输入： 一个图书借阅系统，支持用户注册、用户借阅、新书入库等场景"
            ),
            Tool(
                name="Data Query Tool",
                func=self.db_chain.run,
                description="用于从数据库中查询数据"
            )

        ]

    def data_schema_maker(self, business_scene):
        # business_scene like this: "，总共包含5张表。"

        # 1. design table, return tables_name_desc
        log.info("根据业务场景分析需要创建哪些表: \n" + business_scene)

        tables_name_desc_sample_str = "mock_user: 用于记录用户信息的表\n" \
                                      "mock_book: 用于记录书籍信息的表\n"
        prompt = SCHEMA_DESIGNER_PROMPT_TEMPLATE.format(business_scene=business_scene,
                                                        tables_name_desc_sample_str=tables_name_desc_sample_str)
        tables_name_desc = self.llm.predict(prompt)
        log.info(f"分析完毕！需要创建这些表: \n{tables_name_desc}")

        # 2. generate table creation sql
        prompt = TABLE_CREATOR_PROMPT_TEMPLATE.format(business_scene=business_scene,
                                                      tables_name_desc=tables_name_desc)

        tables_creation = self.llm.predict(prompt)

        # 3. execute sql
        self.db.run_multi_sql_script(tables_creation)
        log.info(f"表创建完毕！ \n{tables_name_desc}")

        return tables_name_desc

    def _get_table_count_by_table_name(self, table_name):
        rst = self.db.run(f"select count(*) from {table_name}")
        # 将字符串 rst: str 转化为list，比如将 [(49,)] 转化为整数 49
        rst = rst.strip("[]").strip("()").split(",")[0]
        return int(rst)

    def data_record_maker_for_one_table(self, table):
        # table = {"table_name": "app_user", "rows_need_to_generated": 1000}

        # 1. 获取表结构
        log.debug(f"获取表结构: {table['table_name']}")
        table_info = self.db.get_table_info([table["table_name"]])
        log.debug(f"表结构获取完毕！ \n{table_info}")

        # 2. 生成函数的创建语句
        sql_function_name = "_datamini_mock_" + table["table_name"] + "_" + datetime.now().strftime("%Y%m%d%H%M%S")
        prompt = RECORD_CREATOR_PROMPT_TEMPLATE.format(table_info=table_info,
                                                       rows_need_to_generated=table["rows_need_to_generated"],
                                                       sql_function_name=sql_function_name)
        sql_function_creation = self.llm.predict(prompt)

        # 3. 记录插入前的数据量
        table["count_before_insert"] = self._get_table_count_by_table_name(table["table_name"])

        # 4. 执行函数，生成数据
        self.db.run_multi_sql_script(sql_function_creation)
        self.db.run(f"select {sql_function_name}();")
        self.db.run(f"DROP FUNCTION {sql_function_name};")

        # 5. 检查数据是否生成成功
        table["count_after_insert"] = self._get_table_count_by_table_name(table["table_name"])
        table["rows_generated"] = table["count_after_insert"] - table["count_before_insert"]
        return table

    def data_record_maker(self, tables):
        # tables like this: "table001: 100, table002: 100"

        tables_generated = []
        for _table in tables.split(","):
            table_name, rows_need_to_generated = _table.strip().split(":")
            log.info(f"表名:{table_name} 行数：{rows_need_to_generated}  数据生成中... ")
            result = self.data_record_maker_for_one_table(
                {"table_name": table_name,
                 "rows_need_to_generated": int(rows_need_to_generated)
                 }
            )
            tables_generated.append(result)
            log.info(f"表名:{table_name} 行数：{rows_need_to_generated}  数据生成完成！")
        return tables_generated
