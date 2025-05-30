import logging
import logging.handlers


class Logger:

    def __init__(self, log_level=logging.DEBUG, log_name=None):
        self.logger = logging.getLogger(log_name)
        self.logger.setLevel(log_level)

        if not self.logger.handlers:
            sh = logging.handlers.SocketHandler("localhost", 9020)
            self.logger.addHandler(sh)

    def get_logger(self):
        return self.logger

    def get_adapter(self, test_context=""):
        return logging.LoggerAdapter(self.logger, {"test_context": test_context})
