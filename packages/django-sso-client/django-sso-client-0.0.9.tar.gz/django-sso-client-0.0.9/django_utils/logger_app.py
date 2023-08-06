import logging

def get_logger(class_name:str):
    """ Formas de uso : info, warn, warning, error e debug
    
    Args:
        class_name : Nome da classe que será efetuado o log

    Returns:
        Logger : instance
    """
    logger = logging.getLogger(class_name)
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    
    return logger