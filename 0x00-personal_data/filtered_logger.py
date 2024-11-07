#!/usr/bin/env python3
"Regex-ing"
import re
from typing import List
import logging


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    "Obfuscate specific fields in a log message"
    for f in fields:
        ptrn = rf"{f}=[^{separator}]*"
        message = re.sub(ptrn, f"{f}={redaction}", message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """
    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        "init"
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        "Format log record and redact specified fields as required."
        return filter_datum(self.fields, self.REDACTION,
                            super().format(record), self.SEPARATOR)
