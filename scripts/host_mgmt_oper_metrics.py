#!/usr/bin/python3

import sys
import os
import re
import logging
import json
import ast

sys.path.append('../lib')
import parallel_ssh_lib
import penctl_lib
import generator_lib
from html_builder_lib import *


# Change the web directory to the required web-server directory where
# the files under pen-apps/web have been installed
WEB_DIR = '../dashboard'

# Input file which has details on host, dscs
input_file = '../input/host_managed_input.json'


# Cert file will be None for Host Managed cases
cert_file  = '/root/venky_venice_token_auth.pem'
#cert_file  = None

logfile = '/tmp/host_mgmt.log'

with open( input_file ) as fr:
     input_dict = json.load(fr)

host_config = input_dict['host_dict']


logging.basicConfig( level=logging.INFO, filename=logfile, filemode='w')
logging.root.setLevel(logging.INFO)
log = logging.getLogger("hostmgmt")





# Connect to all Hosts in parallel
phdl = parallel_ssh_lib.ParallelSessions( log, host_config )


# Collect statistics and generate Html reports for dashboard
html_file = WEB_DIR + '/' + 'host_dsc_summary.html'
generator_lib.generate_host_dsc_summary_page( log, phdl, html_file, cert_file=cert_file )


html_file = WEB_DIR + '/' + 'host_port_summary.html'
generator_lib.generate_host_dsc_port_page( log, phdl, html_file, cert_file=cert_file )


html_file = WEB_DIR + '/' + 'host_temperature.html'
generator_lib.generate_dsc_temp_page( log, phdl, html_file, cert_file=cert_file )


html_file = WEB_DIR + '/' + 'host_power.html'
generator_lib.generate_dsc_power_page( log, phdl, html_file, cert_file=cert_file )

html_file = WEB_DIR + '/' + 'host_interface_stats_summary.html'
generator_lib.generate_host_interface_stats_page( log, phdl, html_file, cert_file=cert_file )


html_file = WEB_DIR + '/' + 'host_lldp_summary.html'
generator_lib.generate_host_lldp_neighor_page( log, phdl, html_file )

