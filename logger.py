from datetime import datetime
import logging
from pathlib import Path


def get_logger(name='logger', level='DEBUG', to_console=True, to_file=False, file_path=None, file_name=None):
    """get a python logger"""

    def _log_level(level):
        return {'debug': logging.DEBUG,
                'info': logging.INFO,
                'warning': logging.WARNING,
                'error': logging.ERROR,
                'critical': logging.CRITICAL}.get(level.lower())

    logger = logging.getLogger(name)
    logger.setLevel(_log_level(level))
    formatter = logging.Formatter('%(asctime)s.%(msecs)03d\t%(levelname)s\t%(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    if to_console is True:
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        logger.addHandler(ch)

    if to_file is True:
        if file_path is None:
            raise ValueError(f'file_path must be provided when log_to_file is True')
        log_path = Path(file_path)
        log_path.mkdir(exist_ok=True)
        f_name = file_name or f'{name}_{datetime.now()}.log'
        fh = logging.FileHandler(str(log_path.joinpath(f_name)), mode='w')
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    return logger