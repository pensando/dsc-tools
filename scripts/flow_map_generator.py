#!/usr/bin/python3


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


log_file       = '/tmp/flow_map_gen.log'

topology_file  = '../input/all_dscs_file.json'
penctl_exe     = './penctl.linux'
cert_file      = '/home/venksrin/.ssh/psm_token.pem'

private_key_file         = '/home/venksrin/.ssh/id_rsa'

# This script uses the 
output_file    = '../DATA/flow_data.json'
tmp_file       = '../DATA/tmp_flow_data.json'




logging.basicConfig( level=logging.INFO, filename=log_file, filemode='w')
logging.root.setLevel(logging.INFO)
log = logging.getLogger("flowmap")


with open( topology_file ) as fr:
     input_dict = json.load(fr)



dsc_config = input_dict['dsc_dict']

dsc_ip_list = []
for dsc_id in dsc_config.keys():
    dsc_ip_list.append( dsc_config[dsc_id]['mgmt_ip'] )

# Create Parallel sessions ..
phdl = ParallelSSHClient(dsc_ip_list, user='root', pkey=private_key_file )

# Generate flow_map_dict per DSC ..
flow_dict = dsc_oper_lib.get_dscs_flow_dict(log, phdl )
print(flow_dict)

with open( tmp_file, 'w' ) as fw:
    json.dump(flow_dict, fw)

os.system( 'cp {} {}'.format( tmp_file, output_file ))
