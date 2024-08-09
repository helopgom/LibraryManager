import logging


def setup_logging():
    logging.basicConfig(format='%(levelname)s (%(asctime)s): %(message)s (Line: %(lineno)d [%(filename)s]',
                        datefmt='%d/%m/%Y %I:%M:%S %p',
                        level=logging.DEBUG,
                        filename='application.log',
                        filemode='w')


setup_logging()


