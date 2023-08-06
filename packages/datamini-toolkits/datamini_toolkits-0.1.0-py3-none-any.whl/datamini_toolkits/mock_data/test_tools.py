from unittest import TestCase
import unittest
from tools import parse_sql_script


class TestParseSqlScript(TestCase):
    sql_script_text1 = """
       select * from mock_employee;
       select * from mock_employee;
       select * from mock_employee;
       """

    sql_script_text2 = """
    select * from mock_employee;
    """

    sql_script_text3 = """select * from mock_employee"""

    sql_script_text4 = """CREATE TABLE IF NOT EXISTS `mock_leave` (
        `id` INT PRIMARY KEY AUTO_INCREMENT COMMENT '主键',
        `employee_id` INT NOT NULL COMMENT '员工ID',
        `leave_start_date` DATE NOT NULL COMMENT '请假开始日期',
        `leave_end_date` DATE NOT NULL COMMENT '请假结束日期',
        `leave_reason` VARCHAR(255) NOT NULL COMMENT '请假原因',
        INDEX idx_employee_id(`employee_id`),
        INDEX idx_leave_start_date(`leave_start_date`)
    ) DEFAULT CHARSET=utf8mb4 COMMENT='请假信息表';

    CREATE TABLE IF NOT EXISTS `mock_overtime` (
        `id` INT PRIMARY KEY AUTO_INCREMENT COMMENT '主键',
        `employee_id` INT NOT NULL COMMENT '员工ID',
        `overtime_date` DATE NOT NULL COMMENT '加班日期',
        `overtime_hours` DECIMAL(5,2) NOT NULL COMMENT '加班时长',
        `overtime_reason` VARCHAR(255) NOT NULL COMMENT '加班原因',
        INDEX idx_employee_id(`employee_id`),
        INDEX idx_overtime_date(`overtime_date`)
    ) DEFAULT CHARSET=utf8mb4 COMMENT='加班信息表';
    -- END"""

    sql_script_text5 = """
-- BEGIN 
DELIMITER $$
CREATE FUNCTION _datamini_mock_mock_employee_20230626091249()
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

    def _test_parse_sql_script(self, sql_script_text: str, sql_num: int):
        sqls = parse_sql_script(sql_script_text)
        assert len(sqls) == sql_num
        return sqls

    def test1(self):
        self._test_parse_sql_script(self.sql_script_text1, 3)

    def test2(self):
        self._test_parse_sql_script(self.sql_script_text2, 1)

    def test3(self):
        self._test_parse_sql_script(self.sql_script_text3, 1)

    def test4(self):
        self._test_parse_sql_script(self.sql_script_text4, 2)

    def test5(self):
        self._test_parse_sql_script(self.sql_script_text5, 1)



if __name__ == '__main__':
    unittest.main()