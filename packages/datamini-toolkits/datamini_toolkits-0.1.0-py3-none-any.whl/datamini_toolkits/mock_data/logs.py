import logging

logging.basicConfig(level=logging.DEBUG)


# Configure logger 1
llmlog = logging.getLogger('llmlog')
llmlog.setLevel(logging.DEBUG)
llmhandler = logging.FileHandler('llm.log')
llmhandler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
llmlog.addHandler(llmhandler)

# Configure logger 2
dblog = logging.getLogger('dblog')
dblog.setLevel(logging.DEBUG)
dbhandler = logging.FileHandler('db.log')
dbhandler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
dblog.addHandler(dbhandler)

# configure logger 3
llmbilling = logging.getLogger('llmbilling')
llmbilling.setLevel(logging.DEBUG)
llmbillinghandler = logging.FileHandler('llmbilling.log')
llmbillinghandler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
llmbilling.addHandler(llmbillinghandler)


def log_llm_prompt_response(prompt, response):
    llmlog.info("="*30 + "[Prompt to predicting]" + "="*30)
    llmlog.info(prompt)
    llmlog.info("-"*10 + "[Completion]" + "-"*10)
    llmlog.info(response)


def log_db_sql_response(sql, response):
    dblog.info("="*30 + "[SQL to Executing]" + "="*30)
    dblog.info(sql)
    dblog.info("-"*10 + "[Response]" + "-"*10)
    dblog.info(response)


def log_llm_billing(request, result):
    llmbilling.info("="*30 + "[Request to Agent]" + "="*30)
    llmbilling.info(request)
    llmbilling.info("-"*10 + "[Response]" + "-"*10)
    llmbilling.info(result)


class log(object):
    llm = log_llm_prompt_response
    db = log_db_sql_response
    llm_billing = log_llm_billing

    info = logging.info
    error = logging.error
    warning = logging.warning
    debug = logging.debug