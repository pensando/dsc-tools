#!/usr/bin/env python3


import sys
import os
import subprocess
import re
import argparse
import ast



def run_command(cmd):
    output = subprocess.getoutput(cmd)
    #print(output)
    return output

def run_command_no_output(cmd):
    FNULL = open(os.devnull, 'w')
    output = subprocess.getoutput(cmd, stdout=FNULL, stderr=subprocess.STDOUT)
    #print(output)
    FNULL.close() 
    return output


def get_interface_list( intf_prefix='enp', intf_suffix='s0'):
    interface_list = []
    cmd = 'lspci -d 1dd8:1002'
    output = run_command(cmd)
    match_list = re.findall( '([0-9a-f]+)\:[0-9a-f]+\.[0-9a-f]', output, re.I )
    for hex_bus in match_list:
        intf = intf_prefix + str( int( hex_bus, 16) ) + intf_suffix
        interface_list.append(intf)
    return interface_list


def get_intf_dict( intf_list ):
    host_intf_dict={}
    for intf in intf_list:
        host_intf_dict[intf] = {}
        output = run_command('ifconfig {}'.format(intf))
        for line in output.split("\n"):
            if not re.search( 'error fetching', line ):
               if re.search( 'RX packets', line, re.I ):
                  match = re.search( 'RX packets ([0-9]+)\s+bytes ([0-9]+) ', line, re.I )
                  host_intf_dict[intf]['rx_pkts'] = match.group(1)
                  host_intf_dict[intf]['rx_bytes'] = match.group(2)
               elif re.search( 'RX errors', line, re.I ):
                  match = re.search( 'RX errors ([0-9]+)\s+dropped ([0-9]+) ', line, re.I )
                  host_intf_dict[intf]['rx_errors'] = match.group(1)
                  host_intf_dict[intf]['rx_dropped'] = match.group(2)
               elif re.search( 'TX packets', line, re.I ):
                  match = re.search( 'TX packets ([0-9]+)\s+bytes ([0-9]+) ', line, re.I )
                  host_intf_dict[intf]['tx_pkts'] = match.group(1)
                  host_intf_dict[intf]['tx_bytes'] = match.group(2)
               elif re.search( 'TX errors', line, re.I ):
                  match = re.search( 'TX errors ([0-9]+)\s+dropped ([0-9]+) ', line, re.I )
                  host_intf_dict[intf]['tx_errors'] = match.group(1)
                  host_intf_dict[intf]['tx_dropped'] = match.group(2)
    print(host_intf_dict)



intf_list = get_interface_list()
get_intf_dict(intf_list)
