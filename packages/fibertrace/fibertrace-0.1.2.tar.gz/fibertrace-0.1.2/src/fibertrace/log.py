import json
import logging
import os
import sys
import time
import getpass
import inspect
from pathlib import Path

class LogEntry:
    def __init__(self, timestamp, level, application, module, message, user):
        self.timestamp = timestamp
        self.level = level
        self.application = application
        self.module = module
        self.message = message
        self.user = user

class Logger:
    def __init__(self, log_file_path, application, json_format):
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s [%(levelname)s] [%(application)s] [%(module)s] [%(user)s]: %(message)s')

        if log_file_path:
            log_file_path = os.path.abspath(log_file_path)
            log_dir = os.path.dirname(log_file_path)
            Path(log_dir).mkdir(parents=True, exist_ok=True)

            self.file_handler = logging.FileHandler(log_file_path)
            self.file_handler.setLevel(logging.DEBUG)
            self.file_handler.setFormatter(formatter)
            self.logger.addHandler(self.file_handler)

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        self.application = application
        self.json_format = json_format

    def info(self, message):
        self.log("INFO", message)

    def error(self, message):
        self.log("ERROR", message)

    def debug(self, message):
        self.log("DEBUG", message)

    def errorf(self, message):
        self.log("ERROR", message)
        sys.exit(1)

    def log(self, level, message):
        frame_info = inspect.stack()[1]
        frame_filename = frame_info.filename
        frame_lineno = frame_info.lineno
        frame_function = frame_info.function

        module = os.path.basename(frame_filename)

        user = getpass.getuser()

        log_entry = LogEntry(
            timestamp=time.strftime("%Y/%m/%d %H:%M:%S"),
            level=level,
            application=self.application,
            module=module,
            message=message,
            user=user
        )

        if self.json_format:
            self.log_json(log_entry)
        else:
            self.log_text(log_entry)
        self.console(log_entry)

    def log_json(self, log_entry):
        log_json = json.dumps(log_entry.__dict__)
        self.write_to_file(log_json.encode())

    def log_text(self, log_entry):
        timestamp = log_entry.timestamp
        log_text = f"[{timestamp}] [{log_entry.level}] [{self.application}] [{log_entry.module}] [{log_entry.user}]: {log_entry.message}"
        self.write_to_file(log_text.encode())

    def console(self, log_entry):
        timestamp = log_entry.timestamp
        log_text = f"[{timestamp}] [{log_entry.level}] [{self.application}] [{log_entry.module}] [{log_entry.user}]: {log_entry.message}"
        print(log_text)

    def write_to_file(self, log_data):
        if hasattr(self, 'file_handler'):
            log_data = log_data.decode()  # Bytes in eine Zeichenkette umwandeln
            self.file_handler.stream.write(log_data)
            self.file_handler.stream.write('\n')  # Zeilenumbruch als Zeichenkette
            self.file_handler.stream.flush()