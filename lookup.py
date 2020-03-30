#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, os, argparse
from threading import Thread
from queue import Queue

test_nameserver = {
    'google_1': '8.8.8.8',
    'google_2': '8.8.4.4',
    'opendns_1': '1.1.1.1',
    'opendns_2':  '1.0.0.1'
}

import socket
import dns.resolver
from dns.resolver import NXDOMAIN, NoAnswer, Timeout
# from dns.exception import Timeout


def doWork():
    while True:
        cname_service_domain = q.get()
        ns_lookup_test(cname_service_domain)
        q.task_done()


def ns_lookup_test(domainname):

    ns_resolver = dns.resolver.Resolver(configure=False)
    ns_resolver.timeout = 20
    ns_resolver.lifetime = 20

    
    for ns in test_nameserver:
        ns_resolver.nameservers=[test_nameserver[ns]]
        info = ' '.join([ns, test_nameserver[ns], domainname ])
        r_address = []

        try:
            rdata = ns_resolver.query(domainname, 'A', raise_on_no_answer=True)
            
            for rr in rdata:
                r_address.append(rr.address)    
            # print(info,'PASS', '"' + ', '.join(r_address) + '"')
            report_message = ' '.join([info, 'A', 'PASS', '"' + ', '.join(r_address) + '"'])

        
        except NXDOMAIN:
            # print(info,'FAILED','NXDOMAIN')
            report_message = ' '.join([info,'A', 'FAILED','NXDOMAIN'])
            pass

        except NoAnswer:
            # print(info,'FAILED','NoAnswer')
            try:
                rdata = ns_resolver.query(domainname, 'CNAME', raise_on_no_answer=False)

                for rr in rdata:
                    r_address.append(rr.to_text())

                report_message = ' '.join([info, 'CNAME', 'PASS', '"' + ', '.join(r_address) + '"'])
                

            except:
                report_message = ' '.join([info,'CNAME','FAILED','NoAnswer'])
                pass

        except Timeout:
            # print(info,'FAILED','Timeout')
            report_message = ' '.join([info,'A','FAILED','Timeout'])
            pass

        with open(filename, 'a', 1) as f:
                    f.write(report_message + os.linesep)


if __name__== "__main__":
    concurrent = 25
    success = 0
    errors = 0

    q = Queue(concurrent * 2)
    filename = 'report.csv'

    with open(filename, 'w') as f:
        f.write('Nameserver IP Domain Type Test result' + os.linesep)

    for i in range(concurrent):
        t = Thread(target=doWork)
        t.daemon = True
        t.start()

    try:
        #Location of your CSV containing one domain per line
        parser = argparse.ArgumentParser(description='Process something.')
        parser.add_argument('strings', metavar='FILENAME', type=str, nargs='?')
        args = parser.parse_args()
        test_filename = ''.join(args.strings)

        for cname_service_domain in open(test_filename):  
            q.put(cname_service_domain.strip())
        q.join()


    except KeyboardInterrupt:
        sys.exit(1)

