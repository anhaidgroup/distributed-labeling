#!/home/slamphear/miniconda2/bin/python
import logging
logging.basicConfig(filename='log-mur.txt',
                            filemode='a',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.DEBUG)

logging.info("Running Urban Planning")




