#!/usr/bin/env python3
"Regex-ing"
import re
from typing import List


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    "Obfuscate specific fields in a log message"
    for f in fields:
        pattern = rf"{f}=[^{separator}]*"
        msg = re.sub(pattern, f"{f}={redaction}", message)  
    return msg
