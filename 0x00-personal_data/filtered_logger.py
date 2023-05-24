#!/usr/bin/env python3
""" a module for filter datum function """
import logging
import re
PII_FIELDS = ('password', "email", 'ssn', 'ip', 'Passportnumber', 'IP')


def filter_datum(fields: list, redaction: str,
                 message: str, separator: str) -> str:
    """ a filter datum  function """
    for field in fields:
        message = re.sub(f'(?<={field}=).*?(?=;)', redaction, message)
    return message


def get_logger() -> logging.Logger:
    """ a function to rturn a logging object """
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False
    handler = logging.StreamHandler()
    formatter = RedactingFormatter(PII_FIELDS)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, *args, **kwargs):
        """ initalizes class instances """
        if "fields" in kwargs.keys():
            self.fields = kwargs["fields"]
        logging.basicConfig(format=self.FORMAT)
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        """ uses filter datum to filter the record """
        message = super(RedactingFormatter, self).format(record)
        records = filter_datum(self.fields, self.REDACTION,
                               message, self.SEPARATOR)
        return records
