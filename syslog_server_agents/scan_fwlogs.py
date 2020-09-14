#!/usr/bin/python3

import os
import sys
import subprocess
import re
import itertools
import json

# Copy this script to your syslog server which has been configured to be used as syslog server for
# the DSCs which will have the firewall log records as syslogs. You can put it in a cronjob on your
# syslog server to run every 60 mins or the duration you decide to scan.

# This script scans the firewall logs for the last x mins duration given and converts that data to
# a json file which will be used by the script network_mgmt_oper_metrics.py to generate Graphical Reports
# 

fwlog_file = './fwlog_of_interest.log'
duration_in_min = 60
output_file = './fwlog_data.json'
syslog_file = '/var/log/syslog'
#syslog_file = '/var/log/messages'



cmd = "sed -n \"/^$(date --date='{0} minutes ago' '+%b %_d %H:%M')/,\$p\" {1} | grep destaddr > {2}".format(duration_in_min, syslog_file, fwlog_file)
os.system(cmd)
print('Collected logs of Interest .. Working on Generating Json Report')


def to_ranges(iterable):
    iterable = sorted(set(iterable))
    for key, group in itertools.groupby(enumerate(iterable), lambda t: t[1] - t[0]):
        group = list(group)
        yield group[0][1], group[-1][1]

def convert_port_list_to_range(l):
    range_str = ''
    tup_list = to_ranges(l)
    for tup_item in tup_list:
        if tup_item[0] == tup_item[1]:
           range_str = range_str + str(tup_item[0]) + ','
        else:
           range_str = range_str + str(tup_item[0]) + '-' + str(tup_item[1]) + ','
    print(range_str)
    return range_str

def get_linux_output( cmd ):
    output = subprocess.getoutput(cmd)
    return output



def get_total_records( fwlog_file ):
    cmd = "wc -l {}".format(fwlog_file)
    output = get_linux_output(cmd)
    match = re.search( '([0-9]+) {}'.format(fwlog_file), output )
    return int(match.group(1))


def get_total_flows_created( fwlog_file ):
    cmd = "cat {} | grep '\"session-state\":\"flow_create\"' | wc -l".format(fwlog_file)
    total_out = get_linux_output(cmd)
    match = re.search( '([0-9]+)', total_out, re.I )
    return int(match.group(1))



def get_total_flows_deleted( fwlog_file ):
    cmd = "cat {} | grep '\"session-state\":\"flow_delete\"' | wc -l".format(fwlog_file)
    total_out = get_linux_output(cmd)
    match = re.search( '([0-9]+)', total_out, re.I )
    return int(match.group(1))


def get_total_flows_denied_rejected( fwlog_file ):
    cmd = "cat {} | grep deny | wc -l".format(fwlog_file)
    total_out = get_linux_output(cmd)
    match = re.search( '([0-9]+)', total_out, re.I )
    deny_count = int(match.group(1))
    cmd = "cat {} | grep reject | wc -l".format(fwlog_file)
    total_out = get_linux_output(cmd)
    match = re.search( '([0-9]+)', total_out, re.I )
    reject_count = int(match.group(1))
    return (deny_count+reject_count) 


def get_summary_dict( fwlog_file, duration_in_min ):
    summary_dict = {}
    summary_dict['total_fw_records'] = get_total_records(fwlog_file)
    summary_dict['total_flows_created'] = get_total_flows_created(fwlog_file)
    summary_dict['total_flows_deleted'] = get_total_flows_deleted(fwlog_file)
    summary_dict['total_flows_denied'] = get_total_flows_denied_rejected( fwlog_file )
    summary_dict['avg_new_flows_per_sec'] = int(summary_dict['total_flows_created']/(duration_in_min*60))
    print(summary_dict)
    return summary_dict


def get_endpoint_list( fwlog_file ):
    endpoint_list = []
    cmd = "grep -oP '\"srcaddr\":\"[0-9\.]+\"' {} | sort | uniq".format(fwlog_file)
    output = get_linux_output(cmd)
    src_endpoint_list = re.findall( '\"srcaddr\":\"([0-9\.]+)\"', output )
    cmd = "grep -oP '\"destaddr\":\"[0-9\.]+\"' {} | sort | uniq".format(fwlog_file)
    output = get_linux_output(cmd)
    dst_endpoint_list = re.findall( '\"destaddr\":\"([0-9\.]+)\"', output )
    endpoint_list_t = set(src_endpoint_list + dst_endpoint_list)
    endpoint_list = list(endpoint_list_t)
    return endpoint_list


def get_endpoint_detailed_dict( fwlog_file, endpoint_list ):
    print('Total ')
    ep_dict = {}
    for ep in endpoint_list:
        ep_dict[ep] = {}
        ep_dict[ep]['dsc-id'] = ''
        ep_dict[ep]['peer-endpoint-list'] = []
        ep_dict[ep]['protocol-dict'] = { 'TCP': [], 'UDP': [], 'ICMP': [ False ] }
        #ep_dict[ep]['app-list'] = []
        ep_dict[ep]['tx_bytes'] = 0
        ep_dict[ep]['rx_bytes'] = 0
        ep_dict[ep]['rule-list'] = []
        ep_dict[ep]['flows_created'] = 0
        ep_dict[ep]['flows_deleted'] = 0
        ep_dict[ep]['action_allowed'] = 0
        ep_dict[ep]['action_denied'] = 0
        ep_dict[ep]['action_rejected'] = 0
        ep_dict[ep]['action_none'] = 0

    rec_pat = "{\"time\":\"[0-9\-\:A-Z]+\",\"destaddr\":\"([0-9\.]+)\",\"destport\":([0-9]+),\"srcaddr\":\"([0-9\.]+)\",\"srcport\":([0-9]+),\"protocol\":\"([a-zA-Z0-9]+)\",\"action\":\"([a-zA-Z\-\_]+)\",\"direction\":\"([a-z\-]+)\",\"rule-id\":([0-9]+),\"session-id\":([0-9]+),\"session-state\":\"([a-z\_\-]+)\""
    old_pat = "([0-9a-zA-Z\:\.\-\_]+)\[[0-9]+\]\: \[\{\"time\":\"[0-9\-\:A-Z]+\",\"destaddr\":\"([0-9\.]+)\",\"destport\":([0-9]+),\"srcaddr\":\"([0-9\.]+)\",\"srcport\":([0-9]+),\"protocol\":\"([a-zA-Z0-9]+)\",\"action\":\"([a-zA-Z\-\_]+)\",\"direction\":\"([a-z\-]+)\",\"rule-id\":([0-9]+),\"session-id\":([0-9]+),\"session-state\":\"([a-z\_\-]+)\",\"app-id\":\"([0-9a-zA-Z]+)\""
    pat = "([0-9a-zA-Z\:\.\-\_]+)\[[0-9]+\]\: \[\{\"time\":\"[0-9\-\:A-Z]+\",\"destaddr\":\"([0-9\.]+)\",\"destport\":([0-9]+),\"srcaddr\":\"([0-9\.]+)\",\"srcport\":([0-9]+),\"protocol\":\"([a-zA-Z0-9]+)\",\"action\":\"([a-zA-Z\-\_]+)\",\"direction\":\"([a-z\-]+)\",\"rule-id\":([0-9]+),\"session-id\":([0-9]+),\"session-state\":\"([a-z\_\-]+)\""
    with open( fwlog_file, 'r') as fp:
        for line in fp:
          print(line)
          match_list = re.findall( rec_pat, line )
          for match_item in match_list:
            #print('%%% match_item = {}'.format(match_item))
            #dsc_id = match.group(1)
            dst_addr = match_item[0]
            dst_port = int(match_item[1])
            ep = match_item[2]
            src_port = int(match_item[3])
            protocol = match_item[4]
            action = match_item[5]
            direction = match_item[6]
            rule_id = int(match_item[7])
            session_state = match_item[8]
            #app_id = match.group(12)
        
            #ep_dict[ep]['dsc_id'] = dsc_id
            if dst_addr not in ep_dict[ep]['peer-endpoint-list']:
               ep_dict[ep]['peer-endpoint-list'].append(dst_addr)
            if dst_port not in ep_dict[ep]['protocol-dict'][protocol]:
               if re.search( 'ICMP', protocol, re.I ):
                  ep_dict[ep]['protocol-dict'][protocol]=True
               else:
                  ep_dict[ep]['protocol-dict'][protocol].append(dst_port)
            #if app_id not in ep_dict[ep]['app-list']:
            #   ep_dict[ep]['app-list'].append(app_id)
            if rule_id != 0 and rule_id not in ep_dict[ep]['rule-list']: 
               ep_dict[ep]['rule-list'].append(rule_id)
            if session_state == "flow_create":
               ep_dict[ep]['flows_created'] = ep_dict[ep]['flows_created'] + 1
            if session_state == "flow_delete":
               ep_dict[ep]['flows_deleted'] = ep_dict[ep]['flows_deleted'] + 1
            if re.search( 'allow', action, re.I ):
               ep_dict[ep]['action_allowed'] = ep_dict[ep]['action_allowed'] + 1
            elif re.search( 'deny', action, re.I ):
               ep_dict[ep]['action_denied'] = ep_dict[ep]['action_denied'] + 1
            elif re.search( 'reject', action, re.I ):
               ep_dict[ep]['action_rejected'] = ep_dict[ep]['action_rejected'] + 1
            elif re.search( 'none', action, re.I ):
               ep_dict[ep]['action_none'] = ep_dict[ep]['action_none'] + 1

    # Delete eps which don't have source addr records
    # Either they are behind non-Naples or Naples in BASENET mode
    for ep in endpoint_list:
        for protocol in ep_dict[ep]['protocol-dict'].keys():
            if not re.search( 'icmp' , protocol, re.I ):
               sorted_port_list = convert_port_list_to_range(ep_dict[ep]['protocol-dict'][protocol])
               ep_dict[ep]['protocol-dict'][protocol] = sorted_port_list

    for ep in endpoint_list:
        if not ep_dict[ep]['peer-endpoint-list']:
           del(ep_dict[ep])

    print(ep_dict)
    return ep_dict



ep_list = get_endpoint_list( fwlog_file)
summary_dict = get_summary_dict( fwlog_file, duration_in_min)
detailed_dict=get_endpoint_detailed_dict( fwlog_file, ep_list )

fw = open( output_file, 'w')
fw.write( '{ "summary_dict":' )

fw.write(json.dumps(summary_dict))
fw.write( ',')

fw.write( '"endpoint_dict":')
fw.write(json.dumps(detailed_dict))
fw.write( "}")

fw.close()
