import logging

DEFAULT_BODY_SIZE = 5 * 1024


def map_log_level_to_string(level: int):
    if level == logging.ERROR:
        return "error"
    elif level == logging.WARN:
        return "warn"
    elif level == logging.INFO:
        return "info"
    elif level == logging.DEBUG:
        return "debug"
    elif level == 5:
        return "trace"
    else:
        return "info"
