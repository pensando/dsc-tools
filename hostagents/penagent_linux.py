#!/usr/bin/env python3

import sys
import os
import subprocess
import re
import argparse
import ast

# This script is a wrapper over Penctl to fetch all the DSCs in the server
# as they can be in different slots on different slots and execute commands
# in parallel.


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


def get_dsc_ip_list():
    dsc_ip_list = []
    cmd = 'lspci -d 1dd8:1004'
    output = run_command(cmd)
    match_list = re.findall( '([0-9a-f]+)\:[0-9a-f]+\.[0-9a-f]', output, re.I )
    for hex_bus in match_list:
        dsc_ip = '169.254.' + str( int( hex_bus, 16) ) + '.1'
        dsc_ip_list.append(dsc_ip)
    return dsc_ip_list



parser = argparse.ArgumentParser(description = "penagent" )
parser.add_argument('--cmd', dest='cmd', required=True )
parser.add_argument('--penctl_path', dest='penctl_path', default='/root/penctl.linux' )
parser.add_argument('--output_type', dest='output_type', default='json' )
parser.add_argument('--cert_file', dest='cert_file', default=None )
args, sys.argv[1:] = parser.parse_known_args(sys.argv[1:])

cmd = args.cmd
penctl_path = args.penctl_path


output = {}
for dsc_ip in get_dsc_ip_list():
    #print(dsc_ip)
    if args.cert_file is None or args.cert_file == "None":
       penctl_cmd = "export DSC_URL=http://{};{} {}".format(dsc_ip,penctl_path,cmd)
    else:
       penctl_cmd = "export DSC_URL=http://{};{} {} -a {}".format(dsc_ip,penctl_path,cmd,args.cert_file)
    if re.search( 'json', args.output_type, re.I ):
       output[dsc_ip] = ast.literal_eval(run_command(penctl_cmd))
    else:
       output[dsc_ip] = run_command(penctl_cmd)

print(output)
