#!/usr/bin/env python3

import sys
import os
import re
import logging
import json
import parallel_ssh_lib
import time
import ast

# Most of the methods in this lib use parallel execution to all DSCs..
# phdl is the parallel hdl to all DSCs


def enable_ssh_to_dscs( log, dsc_ip_list, cert_file, penctl_exe ):
    for dsc_ip in dsc_ip_list:
        log.info('Enable ssh access to DSC ' + dsc_ip )
        cmd = 'export DSC_URL=http://{0};{1} -a {2} update ssh-pub-key -f ~/.ssh/id_rsa.pub;{1} system enable-sshd -a {2}'.format( dsc_ip, penctl_exe, cert_file )
        print(cmd)
        os.system(cmd)
 


# Use this for cmds which generate JSON Output on DSCs ..
# The command will return output as a recursive dict with key as dsc_ip,
# followed by k,v pairs of output
def get_dscs_cmd_out_dict( log, phdl, cmd ):
    output_dict = {}
    #print(cmd)
    dsc_cmd = 'export PATH=/bin:/sbin:/usr/bin:/usr/sbin:/platform/bin:/nic/bin:/platform/tools:/nic/tools;' +  'export LD_LIBRARY_PATH=/platform/lib:/nic/lib;' + cmd
    print(dsc_cmd)
    output = phdl.run_command(dsc_cmd)
    for dsc_ip, dsc_output in output.items():
        output_dict[dsc_ip] = {}
        cmd_out_str = '' 
        for line in dsc_output.stdout:
            #print(line)
            cmd_out_str = cmd_out_str + line.replace( '\t', '   ')
        #output_dict[dsc_ip] = ast.literal_eval(cmd_out_str)
        output_dict[dsc_ip] = json.loads(cmd_out_str)
    return output_dict
 



# Use this for cmds which generate regular line by line string Output on DSCs ..
# The command will return output as a dict with key as dsc_ip
def get_dscs_cmd_out_str( log, phdl, cmd ):
    output_dict = {}
    print(cmd)
    dsc_cmd = 'export PATH=/bin:/sbin:/usr/bin:/usr/sbin:/platform/bin:/nic/bin:/platform/tools:/nic/tools;' +  'export LD_LIBRARY_PATH=/platform/lib:/nic/lib;' + cmd
    print(dsc_cmd)
    output = phdl.run_command(dsc_cmd)
    for dsc_ip, dsc_output in output.items():
        output_dict[dsc_ip] = {}
        cmd_out_str = '' 
        for line in dsc_output.stdout:
            print(line)
            cmd_out_str = cmd_out_str + line + '\n'
        print(cmd_out_str)
        output_dict[dsc_ip] = cmd_out_str
    print(type(output_dict))
    return output_dict



def get_halctl_show_session_dict( log, phdl ):
    flow_records_dict=get_dscs_cmd_out_str( log, phdl, 'halctl show session | grep IPv4')
    return flow_records_dict



def get_dscs_intf_bw_stats( log, phdl ):
    bw_dict = {}
    cmd = "halctl show system statistics bw | grep [0-9]"
    out_dict = get_dscs_cmd_out_str( log, phdl, cmd )
    for dsc_ip in out_dict.keys():
        bw_dict[dsc_ip] = {}
    for dsc_ip in out_dict.keys():
        for line in out_dict[dsc_ip].split("\n"):
            #if re.search( '[0-9]+', line, re.I ):
            if re.search( '([a-zA-Z\/\_\-0-9]+)[\s]+([0-9]+)[\s]+([0-9]+)[\s]+\|[\s]+([0-9]+)[\s]+([0-9]+)', line, re.I ):
               match = re.search( '([a-zA-Z\/\_\-0-9]+)[\s]+([0-9]+)[\s]+([0-9]+)[\s]+\|[\s]+([0-9]+)[\s]+([0-9]+)', line )
               intf = match.group(1)
               tx_pps = int(match.group(2))
               tx_bps = int(match.group(3))
               rx_pps = int(match.group(4))
               rx_bps = int(match.group(5))
               bw_dict[dsc_ip][intf] = {}
               bw_dict[dsc_ip][intf]['tx_pps'] = tx_pps
               bw_dict[dsc_ip][intf]['tx_bps'] = tx_bps
               bw_dict[dsc_ip][intf]['rx_pps'] = rx_pps
               bw_dict[dsc_ip][intf]['rx_bps'] = rx_bps
    print(bw_dict)
    return bw_dict
            
        

def convert_flow_record_to_dict( log, flow_records ):
    flow_dict = {}
    for line in flow_records.split("\n"):
        if re.search( 'IPv4', line, re.I ):
           print(line)
           match = re.search( '([0-9\.]+)\:\[[0-9\/]+\]\s+([0-9\.]+)\:\[[0-9\/]+\]\s+([a-zA-Z0-9\-]+)', line, re.I )
           src_ip = match.group(1)
           dst_ip = match.group(2)
           protocol = match.group(3)
           key =  src_ip + "_" + dst_ip + "_" + protocol
           if key not in flow_dict:
              flow_dict[key] = 1
           else:
              flow_dict[key] += 1

    return flow_dict 


def get_dscs_flow_dict( log, phdl ):
    dscs_flow_dict = {}
    flow_records = get_halctl_show_session_dict( log, phdl )
    for dsc_ip in flow_records.keys():
        dscs_flow_dict[dsc_ip] = convert_flow_record_to_dict( log, flow_records[dsc_ip] )
    return dscs_flow_dict 



def get_profiles_dict( log, phdl ):
    profiles_dict = {}
    out_dict = get_dscs_cmd_out_str( log, phdl, 'halctl show system mode')
    print(out_dict)
    for dsc_ip in out_dict.keys():
        print(dsc_ip)
        profiles_dict[dsc_ip] = {}
        for line in out_dict[dsc_ip].split("\n"):
            if re.search( 'Forwarding Mode: ([A-Za-z\_\-]+)', line, re.I ):
               match = re.search( 'Forwarding Mode: ([A-Za-z\_\-]+)', line, re.I )
               profiles_dict[dsc_ip]['fwd-mode'] = match.group(1)
            if re.search( 'Policy Mode: ([A-Za-z\_\-]+)', line, re.I ):
               match = re.search( 'Policy Mode: ([A-Za-z\_\-]+)', line, re.I )
               profiles_dict[dsc_ip]['policy-mode'] = match.group(1)
    return profiles_dict

def get_dscs_detail_dict( log, phdl ):
    dscs_dict = {}
    system_dict = get_dscs_cmd_out_dict( log, phdl, 'curl localhost:9007/api/mode/')
    #profiles_dict_t = get_dscs_cmd_out_dict( log, phdl, 'curl localhost:9007/api/profiles/')
    profiles_dict = get_profiles_dict( log, phdl )
    version_dict = get_dscs_cmd_out_dict( log, phdl, 'cat /nic/etc/VERSION.json')
    fru_dict = get_dscs_cmd_out_dict( log, phdl, 'cat /tmp/fru.json')
    ifconfig_dict = get_dscs_cmd_out_str( log, phdl, 'ifconfig oob_mnic0')

    for dsc_ip in version_dict.keys():
        dscs_dict[dsc_ip] = {}

    for dsc_ip in version_dict.keys():
        if system_dict[dsc_ip]['is-connected-to-venice'] is False:
           dsc_id = fru_dict[dsc_ip]['mac-address']
           if re.search( 'inet addr:([0-9\.]+)', ifconfig_dict[dsc_ip], re.I ):
              match = re.search( 'inet addr:([0-9\.]+)', ifconfig_dict[dsc_ip], re.I )
              mgmt_ip = match.group(1)
           else:
              mgmt_ip = 'None'
        else:
           dsc_id = system_dict[dsc_ip]['dsc-id']
           mgmt_ip = system_dict[dsc_ip]['mgmt-ip']
        dscs_dict[dsc_ip]['fw-version'] = version_dict[dsc_ip]['sw']['version']
        dscs_dict[dsc_ip]['dsc-id'] = dsc_id
        dscs_dict[dsc_ip]['mgmt-ip'] = mgmt_ip
        dscs_dict[dsc_ip]['product-name'] = fru_dict[dsc_ip]['product-name']
        dscs_dict[dsc_ip]['mac-address'] = fru_dict[dsc_ip]['mac-address']
        dscs_dict[dsc_ip]['part-number']=fru_dict[dsc_ip]['part-number']
        dscs_dict[dsc_ip]['serial-number']=fru_dict[dsc_ip]['serial-number']
        dscs_dict[dsc_ip]['fwd-mode'] = profiles_dict[dsc_ip]['fwd-mode']
        dscs_dict[dsc_ip]['policy-mode'] = profiles_dict[dsc_ip]['policy-mode']

    print(dscs_dict)
    return dscs_dict
        

def get_dscs_arm_interfaces_dict( log, phdl):

    arm_intf_dict = {}
    ifconfig_show_dict = get_dscs_cmd_out_str( log, phdl, 'ifconfig -a | grep -A 2 00:AE:CD' )

    for dsc_ip in ifconfig_show_dict.keys():
        arm_intf_dict[dsc_ip] = {}
        intf_list = re.findall( '([a-zA-Z\_0-9]+)[\s]+Link encap:Ethernet', ifconfig_show_dict[dsc_ip] )
        for intf in intf_list:
            arm_intf_dict[dsc_ip][intf] = {}

    for dsc_ip in arm_intf_dict.keys():
        for line in ifconfig_show_dict[dsc_ip].split("\n"):
            print(line)
            if re.search( '([a-zA-Z\_0-9]+)[\s]+Link encap:Ethernet\s+HWaddr ([0-9a-fA-F\:]+)', line, re.I ):
               match = re.search( '([a-zA-Z\_0-9]+)[\s]+Link encap:Ethernet\s+HWaddr ([0-9a-fA-F\:]+)', line, re.I )
               intf_name = str(match.group(1))
               print(intf_name)
               arm_intf_dict[dsc_ip][intf_name]['mac_addr'] = str(match.group(2))
            if re.search( 'inet addr:([0-9\.]+)', line, re.I ):
               match = re.search( 'inet addr:([0-9\.]+)', line, re.I )
               arm_intf_dict[dsc_ip][intf_name]['ip_addr'] = str(match.group(1))

    for dsc_ip in arm_intf_dict.keys():
        for intf_name in arm_intf_dict[dsc_ip].keys():
            if 'ip_addr' not in arm_intf_dict[dsc_ip][intf_name].keys():
               arm_intf_dict[dsc_ip][intf_name]['ip_addr'] = None
    #print(arm_intf_dict)
    return arm_intf_dict 
            



# Get Network wide Workload dictionary - Only MACs available
def get_dscs_workload_dict( log, phdl, arm_intf_dict ):
    dscs_workload_dict = {}
    endpoint_show_dict=get_dscs_cmd_out_str( log, phdl, 'halctl show endpoint | grep Enic- | grep true')
    for dsc_ip in endpoint_show_dict.keys():
        arm_mac_list = []
        for intf_name in arm_intf_dict[dsc_ip].keys():
            arm_mac_list.append(arm_intf_dict[dsc_ip][intf_name]['mac_addr'])
        dscs_workload_dict[dsc_ip] = {}
        for line in endpoint_show_dict[dsc_ip].split("\n"):
            if re.search('[0-9a-f\.]+', line, re.I ):
               match = re.search( '([0-9]+)\s+([0-9]+)\s+([0-9a-f\.]+)\s+(Enic-[0-9]+)', line, re.I )
               workload_mac = match.group(3)
               if workload_mac not in arm_mac_list:
                  dscs_workload_dict[dsc_ip][workload_mac] = {}
                  dscs_workload_dict[dsc_ip][workload_mac]['enic-intf'] = match.group(4)
                  dscs_workload_dict[dsc_ip][workload_mac]['enic-hdl'] = match.group(1)
                  dscs_workload_dict[dsc_ip][workload_mac]['l2seg'] = match.group(2)
    #print(dscs_workload_dict)
    return dscs_workload_dict
     





def get_dscs_lif_interfaces_dict( log, phdl):
    dscs_lif_dict = {}
    lif_show_dict=get_dscs_cmd_out_str( log, phdl, 'halctl show lif | grep Up | grep -v PUplink | grep -v dsc')
    for dsc_ip in lif_show_dict.keys():
        print(dsc_ip)
        dscs_lif_dict[dsc_ip] = {}
        for line in lif_show_dict[dsc_ip].split("\n"):
            print(line)
            if re.search( '[a-zA-Z]+', line ):
               match = re.search( '([0-9]+)\s+([a-zA-Z0-9\_]+)\s+([a-zA-Z0-9\-]+)\s+([a-zA-Z]+)', line )
               lif_intf = match.group(2)
               dscs_lif_dict[dsc_ip][lif_intf] = {}
               dscs_lif_dict[dsc_ip][lif_intf]['id'] = match.group(1)
               dscs_lif_dict[dsc_ip][lif_intf]['type'] = match.group(3) 
               dscs_lif_dict[dsc_ip][lif_intf]['admin'] = match.group(4) 
    print(dscs_lif_dict)
    return dscs_lif_dict



def get_dscs_delphi_metric_dict( log, phdl, metrics_table ):
    delphi_dict = {}
    cmd = 'delphictl metrics list ' + metrics_table
    delphi_dict = get_dscs_cmd_out_dict( log, phdl, cmd )
    return delphi_dict




def get_dscs_int_obj_dict( log, phdl ):
    dscs_int_obj_dict = {}
    cmd = 'curl localhost:9007/api/interfaces/'
    dscs_out_dict = get_dscs_cmd_out_dict( log, phdl, cmd )
    for dsc_ip in dscs_out_dict:
        dscs_out_list = dscs_out_dict[dsc_ip]
        dscs_int_obj_dict[dsc_ip] = {}
        for intf_dict in dscs_out_list:
            intf_name = intf_dict['meta']['name']
            dscs_int_obj_dict[dsc_ip][intf_name] = {}
            dscs_int_obj_dict[dsc_ip][intf_name]['uuid'] = intf_dict['meta']['uuid']
            dscs_int_obj_dict[dsc_ip][intf_name]['type'] = intf_dict['spec']['type']
            dscs_int_obj_dict[dsc_ip][intf_name]['id'] = intf_dict['status']['id']
            dscs_int_obj_dict[dsc_ip][intf_name]['mirror_sessions'] = intf_dict['spec']['mirror-sessions']
            dscs_int_obj_dict[dsc_ip][intf_name]['oper_status'] = intf_dict['status']['oper-status']
            dscs_int_obj_dict[dsc_ip][intf_name]['if_host_status'] = intf_dict['status']['if-host-status']
    #print(dscs_int_obj_dict)
    return dscs_int_obj_dict


def get_dscs_drop_metrics( log, phdl ):
    dscs_drop_dict = {}
    cmd = 'delphictl metrics list DropMetrics'
    dscs_drop_dict = get_dscs_cmd_out_dict( log, phdl, cmd )
    return dscs_drop_dict


def get_dscs_session_metrics( log, phdl ):
    dscs_session_dict = {}
    cmd = 'delphictl metrics list SessionSummaryMetrics'
    dscs_out_dict = get_dscs_cmd_out_dict( log, phdl, cmd )
    for dsc_ip in dscs_out_dict.keys():
        dscs_session_dict[dsc_ip] = {}
    for dsc_ip in dscs_out_dict.keys():
        sess_dict = dscs_out_dict[dsc_ip]['SessionSummaryMetrics']
        dscs_session_dict[dsc_ip] = sess_dict
    return dscs_session_dict


def get_dscs_cps_dict( log, phdl ):
    dscs_cps_dict = {}
    cmd = 'delphictl metrics list FteCPSMetrics'
    dscs_cps_dict = get_dscs_cmd_out_dict( log, phdl, cmd )
    return dscs_cps_dict


# Use this with RuleMetrices ..
# Also add table for Rules that match with workload ..
def get_nwsec_policy_dict( log, phdl ):
    dscs_nwsec_policy_dict = {}
    cmd = 'curl localhost:9007/api/security/policies/'
    dscs_out_dict = get_dscs_cmd_out_dict( log, phdl, cmd )
   
    for dsc_ip in dscs_out_dict:
        dscs_nwsec_policy_dict[dsc_ip] = {}
        dscs_nwsec_policy_dict[dsc_ip]['policy-rules'] = []
        
    for dsc_ip in dscs_out_dict:
        policy_rules_list = dscs_out_dict[dsc_ip][0]['spec']['policy-rules']
        dscs_nwsec_policy_dict[dsc_ip]['policy-rules'] = policy_rules_list
    #    dscs_out_list = dscs_out_dict[dsc_ip]
    return dscs_nwsec_policy_dict



# Have to do crazy hacks in the following method as the MacMetrics output
# from delphictl is not in proper JSON format
def get_dscs_uplink_bw_pps_dict( log, phdl, intf_obj_dict, uplink_intf_list=['Eth1/1','Eth1/2'] ):

    dscs_mac_stats_dict = {}

    for dsc_ip in phdl.hosts:
        dscs_mac_stats_dict[dsc_ip] = {}
        for intf in uplink_intf_list:
            dscs_mac_stats_dict[dsc_ip][intf] = {}

    cmd = 'delphictl metrics list MacMetrics | egrep "Key|bytesps|pps"'
    dscs_out_dict = get_dscs_cmd_out_str( log, phdl, cmd )
    cmd = 'halctl show port | grep Eth'.format(intf)
    dscs_port_dict = get_dscs_cmd_out_str( log, phdl, cmd )
    

    for dsc_ip in dscs_out_dict.keys():

        for intf_nam in intf_obj_dict[dsc_ip].keys():
            if re.search( 'uplink-1-1', intf_nam, re.I ):
               first_uplink_intf = intf_nam
               
            elif re.search( 'uplink-1-2', intf_nam, re.I ):
               second_uplink_intf = intf_nam

        first_uplink_index = intf_obj_dict[dsc_ip][first_uplink_intf]['id']
        second_uplink_index = intf_obj_dict[dsc_ip][second_uplink_intf]['id']

        for line in dscs_out_dict[dsc_ip].split("\n"):
            if re.search( '\"Key\": ([0-9]+)', line, re.I ):
               match = re.search( '\"Key\": ([0-9]+)', line, re.I )
               key_id = int(match.group(1))
               if key_id == first_uplink_index:
                  intf = uplink_intf_list[0]
               elif key_id == second_uplink_index:
                  intf = uplink_intf_list[1]
               print(intf)
               for port_line in dscs_port_dict[dsc_ip].split("\n"):
                   pat = '{}\s+([0-9]+)G'.format(intf)
                   if re.search( pat, port_line, re.I ):
                      match = re.search( pat, port_line, re.I )
                      dscs_mac_stats_dict[dsc_ip][intf]['speed'] = int(match.group(1))
            if re.search( '\"tx_pps\": ([0-9]+)', line, re.I ):
               match = re.search( '\"tx_pps\": ([0-9]+)', line, re.I )
               dscs_mac_stats_dict[dsc_ip][intf]['txpps'] = int(match.group(1))
            elif re.search( '\"rx_pps\": ([0-9]+)', line, re.I ):
               match = re.search( '\"rx_pps\": ([0-9]+)', line, re.I )
               dscs_mac_stats_dict[dsc_ip][intf]['rxpps'] = int(match.group(1))
            elif re.search( '\"tx_bytesps\": ([0-9]+)', line, re.I ):
               match = re.search( '\"tx_bytesps\": ([0-9]+)', line, re.I )
               dscs_mac_stats_dict[dsc_ip][intf]['txbps'] =  int(match.group(1))*8
               dscs_mac_stats_dict[dsc_ip][intf]['txgbps'] = '{:.2f}'.format(dscs_mac_stats_dict[dsc_ip][intf]['txbps']/1000000000)
            elif re.search( '\"rx_bytesps\": ([0-9]+)', line, re.I ):
               match = re.search( '\"rx_bytesps\": ([0-9]+)', line, re.I )
               dscs_mac_stats_dict[dsc_ip][intf]['rxbps'] =  int(match.group(1))*8
               dscs_mac_stats_dict[dsc_ip][intf]['rxgbps'] = '{:.2f}'.format(dscs_mac_stats_dict[dsc_ip][intf]['rxbps']/1000000000)

    print(dscs_mac_stats_dict)
    return dscs_mac_stats_dict



# Use for Uplink Statistics graphs ..
def get_dscs_mac_metrics_dict( log, phdl, uplink_intf_list=['Eth1/1','Eth1/2'] ):

    dscs_mac_stats_dict = {}

    for dsc_ip in phdl.hosts:
        dscs_mac_stats_dict[dsc_ip] = {}
        for port in uplink_intf_list:
            dscs_mac_stats_dict[dsc_ip][port] = {}
        
    for port in uplink_intf_list:
        cmd = "halctl show port statistics --port {}".format(port)
        out_dict = get_dscs_cmd_out_str( log, phdl, cmd )
        cmd = "halctl show port --port {}".format(port)
        show_port_dict = get_dscs_cmd_out_str( log, phdl, cmd )
        for dsc_ip in out_dict.keys():
            for line in out_dict[dsc_ip].split("\n"):
                if re.search( 'FRAMES RX OK', line ):
                   match = re.search( 'FRAMES RX OK\s+([0-9]+)', line )
                   dscs_mac_stats_dict[dsc_ip][port]['rx_ok'] = match.group(1)
                elif re.search( 'FRAMES RX ALL', line ):
                   match = re.search( 'FRAMES RX ALL\s+([0-9]+)', line )
                   dscs_mac_stats_dict[dsc_ip][port]['rx_all'] = match.group(1)
                elif re.search( 'FRAMES RX BAD ALL', line ):
                   match = re.search( 'FRAMES RX BAD ALL\s+([0-9]+)', line )
                   dscs_mac_stats_dict[dsc_ip][port]['rx_bad_all'] = match.group(1)
                elif re.search( 'FRAMES TX OK', line ):
                   match = re.search( 'FRAMES TX OK\s+([0-9]+)', line )
                   dscs_mac_stats_dict[dsc_ip][port]['tx_ok'] = match.group(1)
                elif re.search( 'FRAMES TX ALL', line ):
                   match = re.search( 'FRAMES TX ALL\s+([0-9]+)', line )
                   dscs_mac_stats_dict[dsc_ip][port]['tx_all'] = match.group(1)
                elif re.search( 'FRAMES TX BAD', line ):
                   match = re.search( 'FRAMES TX BAD\s+([0-9]+)', line )
                   dscs_mac_stats_dict[dsc_ip][port]['tx_bad'] = match.group(1)    
    print(dscs_mac_stats_dict)
    return dscs_mac_stats_dict
