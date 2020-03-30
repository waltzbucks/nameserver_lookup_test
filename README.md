# nameserver_lookup_test
multiple domain lookup test for specific nameservers.
# Usage
make up test domain list to file

    www.google.com
    www.waltzbox.com

testing

    ~$ ./lookup.py domains.csv
    
test result to report.csv file

    ~$ cat report.csv
    Nameserver IP Domain Type Test result
    google_1 8.8.8.8 www.google.com A PASS "172.217.24.196"
    google_1 8.8.8.8 www.waltzbox.com A PASS "14.0.101.149"
    google_2 8.8.4.4 www.google.com A PASS "172.217.24.196"
    opendns_1 1.1.1.1 www.google.com A PASS "172.217.175.100"
    opendns_2 1.0.0.1 www.google.com A PASS "172.217.175.100"
    google_2 8.8.4.4 www.waltzbox.com A PASS "14.0.101.149"
    opendns_1 1.1.1.1 www.waltzbox.com A PASS "14.0.101.149"
    opendns_2 1.0.0.1 www.waltzbox.com A PASS "14.0.101.149"
