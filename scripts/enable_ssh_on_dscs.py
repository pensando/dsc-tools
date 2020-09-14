#!/usr/bin/env python3


from __future__ import print_function
from pssh.clients import ParallelSSHClient
import sys
import os
import re
import logging
import json

sys.path.append('../lib')
import parallel_ssh_lib
import penctl_lib
import dsc_oper_lib
import generator_lib
from html_builder_lib import *



input_file           = '../input/network_managed_input.json'

# For PSM managed DSCs Penctl will require a cert file to access the DSCs
# Generate the Cert file to access DSCs from PSM and copy it to the location
# you specify below on the server where we are executing this script
cert_file               = '/home/venksrin/.ssh/psm_token.pem'


# Pensando Penctl binary path on script execution server
# Penctl will be made available as part of every Pensando firmware release
# Copy the penctl binary under the location you decide to use below on
# the server from where you execute this script
penctl_exe              = './penctl.linux'


# Script Log file 
log_file = '/tmp/network_ssh_enable.log'

logging.basicConfig( level=logging.INFO, filename=log_file, filemode='w')
logging.root.setLevel(logging.INFO)
log = logging.getLogger("nwmgmt")

with open( input_file ) as fr:
     input_dict = json.load(fr)


dsc_config = input_dict['dsc_dict']

print(dsc_config)

dsc_ip_list = []
for dsc_id in dsc_config.keys():
    dsc_ip_list.append( dsc_config[dsc_id]['mgmt_ip'] )




# Enable ssh access to DSCs and Connect to DSCs via Network using PSM cert
dsc_oper_lib.enable_ssh_to_dscs( log, dsc_ip_list, cert_file, penctl_exe )

