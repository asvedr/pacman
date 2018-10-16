import logging

def prepare_logger():
    logger = logging.getLogger('pacman')
    logger.setLevel(logging.DEBUG)
    _FORMAT = logging.Formatter('%(asctime)-15s %(clientip)s %(user)-8s %(message)s')
    _handler = logging.FileHandler('pacman.log')
    _handler.setFormatter(_FORMAT)
    _handler.setLevel(logging.DEBUG)
    logger.addHandler(_handler)
    # return logger
