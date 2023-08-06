from typing import Callable

class MailException(Exception):
    pass

def raiseMailException(msg) -> Callable:
    def __raise():
        raise MailException(msg)
    return __raise
