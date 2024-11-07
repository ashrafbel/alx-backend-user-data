#!/usr/bin/env python3
"Regex-ing"
import re
from typing import List


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    "Obfuscate specific fields in a log message"
    for f in fields:
        ptrn = rf"{f}=[^{separator}]*"
        message = re.sub(ptrn, f"{f}={redaction}", message)
    return message
