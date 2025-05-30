import logging
import socketserver
import struct
import pickle
from typing import cast


LOG_FILE = "automation.log"


class LogRecordStreamHandler(socketserver.StreamRequestHandler):
    def handle(self):
        while True:
            chunk = self.connection.recv(4)
            if len(chunk) < 4:
                break
            slen = struct.unpack(">L", chunk)[0]
            chunk = self.connection.recv(slen)
            while len(chunk) < slen:
                chunk += self.connection.recv(slen - len(chunk))
            obj = pickle.loads(chunk)
            record = logging.makeLogRecord(obj)
            server = cast(LogRecordSocketReceiver, self.server)
            server.logger.handle(record)


class LogRecordSocketReceiver(socketserver.ThreadingTCPServer):
    allow_reuse_address = True

    def __init__(self, host="localhost", port=9020, handler=LogRecordStreamHandler):
        super().__init__((host, port), handler)
        self.logger = logging.getLogger("CentralLogger")
        self.logger.setLevel(logging.DEBUG)
        fh = logging.FileHandler(LOG_FILE)
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(name)s - %(test_context)s : %(message)s",
            datefmt="%d.%m.%Y %H:%M:%S",
        )
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)


def serve():
    server = LogRecordSocketReceiver()
    print("Log server running on port 9020...")
    server.serve_forever()


if __name__ == "__main__":
    serve()
