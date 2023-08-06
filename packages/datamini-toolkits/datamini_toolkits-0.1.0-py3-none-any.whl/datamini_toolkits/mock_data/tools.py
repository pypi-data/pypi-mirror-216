
def parse_sql_script(sql_script_text: str):
    stmts = []
    DELIMITER = ';'
    stmt = ''

    for line in sql_script_text.splitlines():

        if not line.strip():
            continue

        if line.strip().startswith('--'):
            continue

        if 'DELIMITER' in line:
            DELIMITER = line.split()[1]
            continue


        if DELIMITER in line:
            line = line.replace(DELIMITER, '')
            stmt += line
            stmts.append(stmt.strip())
            stmt = ''
        else:
            stmt += line

    if stmt:
        stmts.append(stmt.strip())
    return stmts


def check_function_creation(db):
    fun_create_sql = """create function _datamini_check_function_creation() returns int begin return 1; end;"""
    try:
        db.run(fun_create_sql)
    except Exception as e:
        if int(e.orig.args[0]) == 1418:
            return False
        else:
            raise e

    db.run("drop function _datamini_check_function_creation;")
    return True



