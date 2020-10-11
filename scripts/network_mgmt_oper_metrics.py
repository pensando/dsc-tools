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



# Change it to your webserver directory where the dashboard html files have to be saved
# under /var/www/html
WEB_DIR                 = '../dashboard'
input_file           = '../input/network_managed_input.json'

# For PSM managed DSCs Penctl will require a cert file to access the DSCs
# Generate the Cert file to access DSCs from PSM and copy it to the location
# you specify below on the server where we are executing this script
cert_file               = '/home/venksrin/.ssh/psm_token.pem'

# Private key file to ssh to dsc
private_key_file         = '/home/venksrin/.ssh/id_rsa'

# Duration of logs to analyze for firewall logs in minutes
fw_log_duration         = 60


# Pensando Penctl binary path on script execution server
# Penctl will be made available as part of every Pensando firmware release
# Copy the penctl binary under the location you decide to use below on
# the server from where you execute this script
penctl_exe              = './penctl.linux'


# Output data generated for flow sessions
flow_dict_file          = '../DATA/flow_data.json'
fw_log_analysis_file    = '../DATA/fwlog_data.json'

# Script Log file 
log_file = '/tmp/network_dsc_mgmt.log'

logging.basicConfig( level=logging.INFO, filename=log_file, filemode='w')
logging.root.setLevel(logging.INFO)
log = logging.getLogger("nwmgmt")

with open( input_file ) as fr:
     input_dict = json.load(fr)


dsc_config = input_dict['dsc_dict']
syslog_config = input_dict['syslog_server_dict']

# Syslog server Credentials to access firewall logs
syslog_server           = syslog_config['ip_address']
syslog_server_username  = syslog_config['username']
syslog_server_password  = syslog_config['password']


print(dsc_config)

dsc_ip_list = []
for dsc_id in dsc_config.keys():
    dsc_ip_list.append( dsc_config[dsc_id]['mgmt_ip'] )



# Connect to the DSCs via ssh in parallel
phdl = ParallelSSHClient(dsc_ip_list, user='root', pkey=private_key_file )



# Collect all Information from DSCs and Build Dictionaries ..
dscs_dict               = dsc_oper_lib.get_dscs_detail_dict(log, phdl )
arm_intf_dict           = dsc_oper_lib.get_dscs_arm_interfaces_dict(log, phdl )
dscs_ep_dict            = dsc_oper_lib.get_dscs_workload_dict(log, phdl, arm_intf_dict )
dscs_lif_dict           = dsc_oper_lib.get_dscs_lif_interfaces_dict( log, phdl )
dscs_intf_obj_dict      = dsc_oper_lib.get_dscs_int_obj_dict( log, phdl )
dscs_mac_stats_dict     = dsc_oper_lib.get_dscs_mac_metrics_dict( log, phdl, )
dscs_session_dict       = dsc_oper_lib.get_dscs_session_metrics( log, phdl )
dscs_drops_dict         = dsc_oper_lib.get_dscs_drop_metrics( log, phdl )
dscs_stats_dict         = dsc_oper_lib.get_dscs_uplink_bw_pps_dict(log, phdl, dscs_intf_obj_dict )
dscs_sessions_dict      = dsc_oper_lib.get_dscs_session_metrics( log, phdl )
dscs_cps_dict           = dsc_oper_lib.get_dscs_cps_dict( log, phdl )
dscs_bw_dict            = dsc_oper_lib.get_dscs_intf_bw_stats( log, phdl )

# Generate main DSC summary page for NW managed
html_file = WEB_DIR + '/' + 'dscs_nw_summary.html'
generator_lib.generate_dscs_nw_summary_page( log, phdl, html_file, dscs_dict, cert_file=cert_file )


# Generate per DSC Detailed page under dsc-db
with open( flow_dict_file, 'r' ) as fp:
     dscs_flow_dict = json.load(fp)
generator_lib.generate_dscs_detailed_page( log, phdl, WEB_DIR, dscs_dict, arm_intf_dict, dscs_ep_dict, \
     dscs_flow_dict, dscs_session_dict, dscs_drops_dict, dscs_bw_dict, \
     cert_file=cert_file )

html_file = WEB_DIR + '/' + 'link_utilization.html'
generator_lib.generate_link_utilization_page( log, phdl, html_file, dscs_stats_dict )


html_file = WEB_DIR + '/' + 'dscs_cps.html'
generator_lib.generate_fte_cps_page( log, phdl, html_file, dscs_cps_dict, dscs_dict )


parallel_ssh_lib.scp( '{}:/root/FWLOG/fwlog_data.json'.format(syslog_server), fw_log_analysis_file, syslog_server_username, syslog_server_password )

with open( fw_log_analysis_file ) as fwl:
     fw_log_dict = json.load(fwl)

fw_summary_dict = fw_log_dict['summary_dict']
fw_ep_dict = fw_log_dict['endpoint_dict']
html_file = WEB_DIR + '/' + 'fw_log_analysis.html'

generator_lib.generate_fwlog_analysis_page( log, phdl, html_file, fw_summary_dict, fw_ep_dict, fw_log_duration, cert_file=cert_file )
