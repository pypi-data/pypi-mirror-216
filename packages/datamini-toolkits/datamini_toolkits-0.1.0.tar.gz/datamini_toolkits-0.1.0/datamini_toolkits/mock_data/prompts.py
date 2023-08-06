RECORD_CREATOR_PROMPT_TEMPLATE = """
你是一名非常熟悉数据库SQL语法的程序员，请根据下面提供的数据库表结构和需要的记录数，
生成用于向该表中插入测试数据的函数。

表结构：\n {table_info}，\n需要生成{rows_need_to_generated}条记录。

生成函数时，需注意，
1, 必须生成的是可以执行的函数，函数的返回值为插入的记录数。
2，当表中有自增字段时，请使用自动填充，否则会报错。
3，当表中有唯一索引或者主键时，对于这些字段，需要生成唯一的值，否则会报错。可以采用时间戳或随机数作为后缀来避免重复。
4，避免生成类似『:00』或『:abc』这样的结构，否则使用Python代码执行SQL脚本的时候会以为需要绑定变量，会报错
5,需要包含『DELIMITER $$』和『DELIMITER ;』

返回示例如下：
-- BEGIN 
DELIMITER $$
CREATE FUNCTION {sql_function_name}()        
RETURNS INT                        
BEGIN                            
    DECLARE num INT DEFAULT 1000;         
    DECLARE i INT DEFAULT 0; 

    WHILE i < num DO            
         INSERT INTO app_user(`name`,`email`,`phone`,`gender`,`password`,`age`) 
         VALUES(CONCAT('用户',i),'2548928007qq.com',CONCAT('18',FLOOR(RAND() * ((999999999 - 100000000) + 1000000000))),FLOOR(RAND()  *  2),UUID(),FLOOR(RAND()  *  100));
        SET i =  i + 1;    
    END WHILE;

    RETURN i;
END; $$
DELIMITER ;                             
-- END
"""


TABLE_CREATOR_PROMPT_TEMPLATE = """
你是一名精通数据建模的程序员，也非常熟悉各个行业的数据库表结构设计。
请根据下面提供的数据库的名称以及表的名称和含义，生成该表的建表语句。

业务场景：{business_scene}
表名称和含义: {tables_name_desc}

要求：
1，不能使用外键
2，在合适的字段上添加索引
3，加上注释

返回的示例如下：
-- BEGIN
CREATE TABLE IF NOT EXISTS `mock_user` (
    `id` INT PRIMARY KEY AUTO_INCREMENT COMMENT '主键',
    `name` VARCHAR(255) NOT NULL COMMENT '姓名',
    `email` VARCHAR(255) NOT NULL COMMENT '邮箱',
    INDEX idx_name(`name`)
    ) DEFAULT CHARSET=utf8mb4 COMMENT='用户表';

CREATE TABLE IF NOT EXISTS `mock_book` (
    `id` INT PRIMARY KEY AUTO_INCREMENT COMMENT '主键', 
    `name` VARCHAR(255) NOT NULL COMMENT '书名'
    ) DEFAULT CHARSET=utf8mb4 COMMENT='书籍表';
-- END
"""


SCHEMA_DESIGNER_PROMPT_TEMPLATE = """
你是一名精通数据建模的程序员，也非常熟悉各个行业的数据库表结构设计。
请根据提供的业务场景，设计该业务场景所需要包含的表以及这些表的含义。
一般情况下，表的数量控制在4-8个以内。

业务场景：{business_scene}

要求：
1,为了避免关键词冲突，表名前加上前缀『mock_』，例如『mock_user』

返回结果示例：
{tables_name_desc_sample_str}
"""

