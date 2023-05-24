#!/usr/bin/env python3
""" a module for filter datum function """
import re


def filter_datum(fields: list, redaction: str,
                 message: str, separator: str) -> str:
    """ a filter datum  function """
    for field in fields:
        message = re.sub(f'(?<={field}=).*?(?=;)', redaction, message)
    return message
