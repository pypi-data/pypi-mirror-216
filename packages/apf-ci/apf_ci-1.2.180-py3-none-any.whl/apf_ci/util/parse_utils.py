from apf_ci.util.log_utils import logger


def parse_str_to_int(str_value):
    int_value = str_value
    if isinstance(str_value, str):
        if len(str_value) > 0:
            logger.debug("parse_str_to_int() %s 转换为int" % str_value)
            int_value = int(str_value)
        else:
            logger.debug(" parse_str_to_int() str_value 长度为0")
            int_value = 0

    return int_value


