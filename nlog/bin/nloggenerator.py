#!/usr/bin/env python3
# Author: Leon Cowle (leon_cowle@neimanmarcus.com)
import datetime
import time
import random
import logging
import socket
from rfc5424logging import Rfc5424SysLogHandler

logger = logging.getLogger('syslogtest')
logger.setLevel(logging.INFO)

sh = Rfc5424SysLogHandler(address=('fluent-bit', 1514), socktype=socket.SOCK_STREAM)
logger.addHandler(sh)

srcDomains = [
            "env1.fluentdemocat.com", "env2.fluentdemocat.com", "env3.fluentdemocat.com", "env4.fluentdemocat.com",
            "env1.fluentdemodog.com", "env2.fluentdemodoc.com", "env3.fluentdemodog.com", "env4.fluentdemodog.com",
            "env1.fluentdemobird.com", "env2.fluentdemobird.com", "env3.fluentdemobird.com", "env4.fluentdemobird.com"
            ]

while True:
    nowdt = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S +0000")
    random_ip = random.randint(1, 254)
    random_status = random.choice(['200', '301', '302', '400', '403', '404', '500', '503'])
    random_size = random.randint(100, 1000)
    random_url = "/abc/def/image-" + str(random_size) + ".png"
    random_dom = random.choice(srcDomains)
    random_method = random.choice(['GET', 'POST', 'PUT'])
    random_elapsed_usec = random.randint(5000, 50000)
    out_str = \
        '''10.1.2.{0} "-" "-" [{1}] "{7} {2} HTTP/1.1" {3} {4} {5} elapsed.usec={6}'''.format(random_ip,
                                                                                                       nowdt,
                                                                                                       random_url,
                                                                                                       random_status,
                                                                                                       random_size,
                                                                                                       random_dom,
                                                                                                       random_elapsed_usec,
                                                                                                       random_method)
    print(out_str)
    logger.info(out_str)
    time.sleep(0.5)
