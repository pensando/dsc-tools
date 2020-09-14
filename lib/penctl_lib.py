#!/usr/bin/env python3

import sys
import os
import re
import logging
import json
import parallel_ssh_lib
import ast
import time


def get_host_cmd_out_str( phdl, cmd, ):
    hosts_config = phdl.host_config
    output_dict = {}
    output = phdl.exec(cmd)
    for host in phdl.hosts:
        output_dict[host] = str(output[host])
    print(output_dict)
    return output_dict

def get_host_cmd_out_dict( phdl, cmd ):
    hosts_config = phdl.host_config
    output_dict = {}
    output = phdl.exec(cmd)
    for host in phdl.hosts:
        #print(type(output[host]))
        print(output[host])
        output_dict[host] = json.loads(output[host].strip("\n").replace("'", '"'))
    return output_dict
 
 
def get_penctl_cmd_out_dict( phdl, cmd, cert_file=None, ):
    hosts_config = phdl.host_config
    output = json.dumps(phdl.penctl_exec( cmd, output_type='json', cert_file=cert_file, ))
    #print(type(output))
    output_dict = json.loads(output)
    return output_dict




def get_penctl_cmd_out_string( phdl, cmd, cert_file=None, ):
    hosts_config = phdl.host_config
    output_dict = {}
    output = json.dumps(phdl.penctl_exec( cmd, output_type='string', cert_file=cert_file, ))
    print(output)
    #print(type(output))
    return json.loads(output)


def add_keys_enable_ssh( phdl, cert_file=None ):
    cmd = "system enable-sshd -a /root/penctl.token"
    phdl.penctl_exec( cmd, output_type='string', cert_file=cert_file )
    cmd = "update ssh-pub-key -f /root/.ssh/id_rsa.pub -a /root/penctl.token"
    phdl.penctl_exec( cmd, output_type='string', cert_file=cert_file )

def get_dsc_dict( phdl, cert_file=None ):
    dsc_dict = {}
    cmd = "show dsc"
    out_dict = get_penctl_cmd_out_dict( phdl, cmd, cert_file=cert_file )
    print(out_dict)
    cmd = "show firmware-version"
    fw_dict = get_penctl_cmd_out_dict( phdl, cmd, cert_file=cert_file )
    for host_name in out_dict.keys():
        print(host_name)
        for dsc_ip in out_dict[host_name].keys():
            dsc_id = out_dict[host_name][dsc_ip]['status']['fru']['mac-string']
            dsc_dict[dsc_id] = {}
            dsc_dict[dsc_id]['host_name'] = host_name
            dsc_dict[dsc_id]['product_name'] = out_dict[host_name][dsc_ip]['status']['fru']['product-name']
            dsc_dict[dsc_id]['part_no'] = out_dict[host_name][dsc_ip]['status']['fru']['part-number']
            dsc_dict[dsc_id]['serial_no'] = out_dict[host_name][dsc_ip]['status']['fru']['serial-number']
            dsc_dict[dsc_id]['managed_mode'] = out_dict[host_name][dsc_ip]['status']['mode']
            dsc_dict[dsc_id]['dsc_profile'] = out_dict[host_name][dsc_ip]['spec']['device-profile']  
            dsc_dict[dsc_id]['dsc_name'] = out_dict[host_name][dsc_ip]['status']['dsc-name']
            dsc_dict[dsc_id]['fw_version'] = fw_dict[host_name][dsc_ip]['running-fw-version']
            dsc_dict[dsc_id]['uboot_version'] = fw_dict[host_name][dsc_ip]['running-uboot']
    print(dsc_dict)
    return dsc_dict



def get_penctl_temperature( phdl, cert_file=None ):
    hosts_config = phdl.host_config
    temp_dict = {}
    cmd = "show metrics system temp"
    temp_dict = get_penctl_cmd_out_dict( phdl, cmd, cert_file=cert_file )
    print(temp_dict)
    return temp_dict


def get_penctl_power( phdl, cert_file=None ):
    hosts_config = phdl.host_config
    power_dict = {}
    cmd = "show metrics system power"
    power_dict = get_penctl_cmd_out_dict( phdl, cmd, cert_file=cert_file )
    return power_dict


def get_penctl_firmware_version( phdl, cert_file=None, ):
    hosts_config = phdl.host_config
    power_dict = {}
    cmd = "show firmware-version"
    firmware_dict = get_penctl_cmd_out_dict( phdl, cmd, cert_file=cert_file, )
    return firmware_dict


def upgrade_dsc_firmware( phdl, image_file, cert_file=None ):
    hosts_config = phdl.host_config
    cmd = "system firmware-install -f {}".format(image_file )
    output = json.dumps(phdl.penctl_exec( cmd, output_type='string', cert_file=cert_file ))
    output_dict = json.loads(output)
    #print(type(output_dict))
    for host in output_dict.keys():
        print('#=================================================#')
        print('Upgrade logs for host {}'.format(host))
        print('#=================================================#')
        for dsc_ip in output_dict[host].keys():
            print('\n#-----------------------------#')
            print('DSC IP - {}'.format(dsc_ip))
            print('#-----------------------------#')
            #print(type(output_dict[host][dsc_ip]))
            for line in output_dict[host][dsc_ip].split("\n"):
                print(line)
                print("\n")
    return output_dict

    
 

def get_lldp_neigh_dict( phdl, ):
    # Get interface list for all hosts
    phdl.exec('/usr/sbin/lldpad -d')
    phdl.exec('/root/PENAGENT/enable_lldp.sh')
    lldp_dict = {}
    time.sleep(1)
    lldp_str_dict =  get_host_cmd_out_str( phdl, '/root/PENAGENT/get_lldp_neighbors.sh' )
    for host in lldp_str_dict.keys():
        lldp_dict[host]={}

    for host in lldp_str_dict.keys():
        lldp_out = lldp_str_dict[host]
        for line in lldp_out.split("\n"):
            if re.search( ',', line ):
               (intf,peer_mgmt_ip,peer_name,peer_intf,peer_desc) = line.rstrip("\n").split(",")
               lldp_dict[host][intf]={}
               lldp_dict[host][intf]['peer_name'] = peer_name
               lldp_dict[host][intf]['peer_mgmt_ip'] = peer_mgmt_ip
               lldp_dict[host][intf]['peer_desc'] = peer_desc
               lldp_dict[host][intf]['peer_intf'] = peer_intf
    return lldp_dict



def get_penctl_port( phdl, cert_file=None ):

    port_dict = {}
    cmd = "show port"
    out_dict = get_penctl_cmd_out_string( phdl, cmd, cert_file=cert_file )

    for host in out_dict.keys():
        port_dict[host] = {}
        for dsc_ip in out_dict[host].keys():
            port_dict[host][dsc_ip] = {}

    for host in out_dict.keys():
        for dsc_ip in out_dict[host].keys():
            for line in out_dict[host][dsc_ip].split('\n'):
                if re.search('Eth', line, re.I ):
                   pat = '(Eth[0-9]\/[0-9])\s+([0-9]+G)\s+([0-9]\/[0-9]\/[0-9])\s+([A-Za-z\-]+)\s+([A-Za-z\-]+)\s+([a-z]+)\s+([a-z]+)\s+([0-9]+)\s+([a-z]+)\s+([a-z]+)\s+([a-z]+)\s+([0-9]+)\s+([A-Za-z\_]+)\s+([A-Za-z\_]+)\s+([0-9]+)\s+([A-Za-z\_]+)\s+'
                   match = re.search( pat, line )
                   print(line)
                   port = match.group(1)
                   port_dict[host][dsc_ip][port] = {}
                   port_dict[host][dsc_ip][port]['name'] = port
                   port_dict[host][dsc_ip][port]['speed'] = match.group(2)
                   port_dict[host][dsc_ip][port]['fec_cfg'] = match.group(4)
                   port_dict[host][dsc_ip][port]['fec_oper'] = match.group(5)
                   port_dict[host][dsc_ip][port]['auto_cfg'] = match.group(6)
                   port_dict[host][dsc_ip][port]['auto_oper'] = match.group(7)
                   port_dict[host][dsc_ip][port]['mtu'] = match.group(8)
                   port_dict[host][dsc_ip][port]['link_pause'] = match.group(9)
                   port_dict[host][dsc_ip][port]['tx_pause'] = match.group(10)
                   port_dict[host][dsc_ip][port]['rx_pause'] = match.group(11)
                   port_dict[host][dsc_ip][port]['debounce'] = match.group(12)
                   port_dict[host][dsc_ip][port]['admin_status'] = match.group(13)
                   port_dict[host][dsc_ip][port]['oper_status'] = match.group(13)
                   port_dict[host][dsc_ip][port]['link_sm'] = match.group(15)
    cmd = "show port status"
    out_dict = get_penctl_cmd_out_string( phdl, cmd, cert_file=cert_file )
    for host in out_dict.keys():
        for dsc_ip in out_dict[host].keys():
            for line in out_dict[host][dsc_ip].split('\n'):
                if re.search('Eth', line, re.I ):
                   pat = '(Eth[0-9]\/[0-9])\s+([A-Z]+)\s+([A-Z]+)\s+([A-Z0-9\-]+)'
                   match = re.search( pat, line )
                   port = match.group(1)
                   print(host)
                   print(dsc_ip)
                   port_dict[host][dsc_ip][port]['transceiver'] = match.group(4)
    print(port_dict)
    return port_dict






def get_penctl_port_stats( phdl, cert_file=None ):

    port_dict = {}
    port_list = [ 'Eth1/1', 'Eth1/2' ]

    host_dsc_dict = get_host_dsc_dict( phdl )

    for host in phdl.hosts:
        port_dict[host] = {}
        for dsc_ip in host_dsc_dict[host]:
            port_dict[host][dsc_ip] = {}
            for port in port_list:
                port_dict[host][dsc_ip][port]={}

    for port in port_list:
        cmd = "/nic/bin/halctl show port statistics --port {}".format(port)
        out_dict = get_penctl_cmd_out_string( phdl, cmd, cert_file=cert_file )
        print(out_dict)

        for host in out_dict.keys():
            for dsc_ip in out_dict[host].keys():
                port_cmd_out = out_dict[host][dsc_ip]
                for line in port_cmd_out.split("\n"):
                    print(line)
                    if re.search( 'FRAMES RX OK', line ):
                       match = re.search( 'FRAMES RX OK\s+([0-9]+)', line )
                       port_dict[host][dsc_ip][port]['rx_ok'] = match.group(1)
                    elif re.search( 'FRAMES RX ALL', line ):
                       match = re.search( 'FRAMES RX ALL\s+([0-9]+)', line )
                       port_dict[host][dsc_ip][port]['rx_all'] = match.group(1)
                    elif re.search( 'FRAMES RX BAD ALL', line ):
                       match = re.search( 'FRAMES RX BAD ALL\s+([0-9]+)', line )
                       port_dict[host][dsc_ip][port]['rx_bad_all'] = match.group(1)
                    elif re.search( 'FRAMES TX OK', line ):
                       match = re.search( 'FRAMES TX OK\s+([0-9]+)', line )
                       port_dict[host][dsc_ip][port]['tx_ok'] = match.group(1)
                    elif re.search( 'FRAMES TX ALL', line ):
                       match = re.search( 'FRAMES TX ALL\s+([0-9]+)', line )
                       port_dict[host][dsc_ip][port]['tx_all'] = match.group(1)
                    elif re.search( 'FRAMES TX BAD', line ):
                       match = re.search( 'FRAMES TX BAD\s+([0-9]+)', line )
                       port_dict[host][dsc_ip][port]['tx_bad'] = match.group(1)

    print(port_dict)
    return port_dict




def get_host_dsc_dict( phdl ):
    dsc_dict = {}
    for host in phdl.hosts:
        dsc_dict[host] = []
    cmd = 'lspci -d 1dd8:1004'
    output = phdl.client.run_command(cmd )
    for host, host_output in output.items():
        for line in host_output.stdout:
            if re.search( '([0-9a-f][0-9a-f])\:[0-9]+\.', line ):
               match = re.search( '([0-9a-f][0-9a-f])\:[0-9]+\.', line, re.I )
               hex_bus = match.group(1)
               dsc_ip = '169.254.' + str( int( hex_bus, 16) ) + '.1'
               dsc_dict[host].append(dsc_ip)
    return dsc_dict
 
        

def get_linux_interfaces( phdl ):
    cmd = 'lspci -d 1dd8:1002'
    output = phdl.client.run_command(cmd )
    host_intf_dict = {}
    for host in phdl.hosts:
        #host_intf_dict[host] = {}
        host_intf_dict[host] = []
    for host, host_output in output.items():
        for line in host_output.stdout:
            if re.search( '([0-9a-f][0-9a-f])\:[0-9]+\.', line ):
               match = re.search( '([0-9a-f][0-9a-f])\:[0-9]+\.', line, re.I )
               hex_bus = match.group(1)
               intf = 'enp' + str( int( hex_bus, 16) ) + 's0'
               host_intf_dict[host].append(intf)
    return host_intf_dict
        


def get_linux_interface_stats( log, phdl, cert_file=None ):

    cmd = '/root/PENAGENT/get_interface_counters.sh'
    intf_stats_dict = get_host_cmd_out_dict( phdl, cmd)
    return intf_stats_dict




def get_linux_interface_bandwidth( phdl ):

    cmd = 'lspci -d 1dd8:1002'
    output = phdl.client.run_command(cmd )
    host_intf_dict = {}
    for host in phdl.hosts:
        host_intf_dict[host] = {}
        host_intf_dict[host]['interface_list'] = []
        host_intf_dict[host]['interface_stats'] = {}
    for host, host_output in output.items():
        for line in host_output.stdout:
            if re.search( '([0-9a-f][0-9a-f])\:[0-9]+\.', line ):
               match = re.search( '([0-9a-f][0-9a-f])\:[0-9]+\.', line, re.I )
               hex_bus = match.group(1)
               intf = 'enp' + str( int( hex_bus, 16) ) + 's0'
               host_intf_dict[host]['interface_list'].append(intf)
               host_intf_dict[host]['interface_stats'][intf] = {}
