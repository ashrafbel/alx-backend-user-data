#!/usr/bin/env python3
"Regex-ing"
import re
from typing import List
import logging
import os
import mysql.connector


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


def get_logger() -> logging.Logger:
    """Create and return a logger for user data with redacting formatter"""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    handler = logging.StreamHandler()
    formatter = RedactingFormatter(fields=PII_FIELDS)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


PII_FIELDS = ("name", "email", "password", "ssn", "phone")


def get_db() -> mysql.connector.MySQLConnection:
    """Returns a connector to the database"""
    user = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    password = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    database = os.getenv('PERSONAL_DATA_DB_NAME')
    dbConnection = mysql.connector.connect(
        user=user,
        password=password,
        host=host,
        database=database
    )
    return dbConnection
