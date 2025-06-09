from utils.logs.logger import Logger


def get_logger_with_context(request, log_name):
    # Prepare page to logging process
    browser_name = request.config.getoption("--browser")
    test_file = request.node.fspath
    test_name = request.node.name
    log_line_prefix = f"[{browser_name}]::{test_file}::{test_name}"
    logger_instance = Logger(log_name=log_name)
    logger_with_context = logger_instance.get_adapter(test_context=log_line_prefix)

    return logger_with_context
